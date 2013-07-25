from datetime import datetime, timedelta

import transaction
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import desc


from trumpet.models.consultant import Client
from trumpet.models.consultant import TicketStatusType, TicketStatus
from trumpet.models.consultant import TicketCurrentStatus, Ticket


class StatusTypeManager(object):
    def __init__(self, session):
        self.session = session

    def query(self):
        return self.session.query(TicketStatusType)

    def get(self, id):
        return self.query().get(id)

    def get_id(self, status):
        return self.query().filter_by(name=status).one().id

    def all(self):
        return self.query().all()
    
        

class TicketManager(object):
    def __init__(self, session):
        self.session = session
        self.stypes = StatusTypeManager(self.session)

    def query(self):
        return self.session.query(Ticket)

    def open(self, user_id, client_id, title, description):
        with transaction.manager:
            now = datetime.now()
            t = Ticket()
            t.client_id = client_id
            t.title = title
            t.description = description
            t.created = now
            self.session.add(t)
            ticket = self.session.merge(t)
            stype_id = self.stypes.get_id('opened')
            status = TicketStatus()
            status.ticket_id = ticket.id
            status.status = stype_id
            status.reason = "New Ticket"
            status.changed = now
            status.changed_by_id = user_id
            self.session.add(status)
            cstatus = TicketCurrentStatus()
            cstatus.ticket_id = ticket.id
            cstatus.created = ticket.created
            cstatus.last_change = status.changed
            cstatus.status = stype_id
            self.session.add(cstatus)
        return self.session.merge(ticket)
    


    # There is no enforcing of workflow 
    def update_ticket(self, ticket_id, user_id, status_id, reason):
        now = datetime.now()
        with transaction.manager:
            status = TicketStatus()
            status.ticket_id = ticket_id
            status.status = status_id
            status.reason = reason
            status.changed = now
            status.changed_by_id = user_id
            self.session.add(status)
            cstatus = self.session.query(TicketCurrentStatus).get(ticket_id)
            cstatus.last_change = now
            cstatus.status = status_id
            cstatus = self.session.merge(cstatus)
        return self.session.merge(status)
    
    

    def all(self):
        return self.query().all()

    def status(self, ticket_id):
        q = self.session.query(TicketCurrentStatus)
        q = q.filter_by(ticket_id=ticket_id)
        return q.one()

    def get_status(self, ticket_id):
        s = self.status(ticket_id)
        st = self.stypes.get(s.status)
        return st.name
    
    def _convert_range(self, start, end):
        "start and end are timestamps"
        start = datetime.fromtimestamp(float(start))
        end = datetime.fromtimestamp(float(end))
        return start, end

    def _range_filter(self, query, start, end):
        "start and end are datetime objects"
        query.filter(TicketCurrentStatus.last_change >= start)
        query.filter(TicketCurrentStatus.last_change <= end)
        return query
    
    def get_current_status_range(self, start, end):
        "start and end are datetime objects"
        q = self.session.query(TicketCurrentStatus)
        q = self._range_filter(q, start, end)
        return q.all()
    
    def get_current_status_range_ts(self, start, end):
        "start and end are timestamps"
        start, end = self._convert_range(start, end)
        return self.get_current_status_range(start, end)
    
        
