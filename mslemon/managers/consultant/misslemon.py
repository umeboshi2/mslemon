import os
from datetime import datetime, timedelta

import transaction
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import desc
from sqlalchemy import func

from mslemon.util import datetime_from_pdf_filename
from mslemon.util import get_scanned_filenames

from mslemon.managers.util import convert_range_to_datetime

#FIXME: better module name
from mslemon.models.misslemon import Description
from mslemon.models.misslemon import Ticket, TicketCurrentStatus
from mslemon.models.misslemon import TicketStatusChange
from mslemon.models.misslemon import PhoneCall
from mslemon.models.misslemon import File, ScannedDocument

class DescriptionManager(object):
    def __init__(self, session):
        self.session = session

    def query(self):
        return self.session.query(Description)

    def new(self, text):
        with transaction.manager:
            d = Description()
            d.text = text
            self.session.add(d)
        return self.session.merge(d)

    def get(self, id):
        return self.query().get(id)
    
    def update(self, text):
        with transaction.manager:
            try:
                d = self.session.query(Description).filter_by(text=text).one()
            except NoResultFound:
                d = Description()
                d.text = text
                self.session.add(d)
                d = self.session.merge(d)
        return d
    
class TicketManager(object):
    def __init__(self, session):
        self.session = session
        self.descriptions = DescriptionManager(self.session)

    def query(self):
        return self.session.query(Ticket)

    def get(self, id):
        return self.query().get(id)
    
    def open(self, user_id, title, description, handler_id=None):
        if handler_id is None:
            handler_id = user_id
        with transaction.manager:
            now = datetime.now()
            d = self.descriptions.new(description)
            t = Ticket()
            t.title = title
            t.description_id = d.id
            t.created = now
            self.session.add(t)
            ticket = self.session.merge(t)
            change = TicketStatusChange()
            change.ticket_id = ticket.id
            change.status = 'opened'
            change.reason = "New Ticket"
            change.description_id = d.id
            change.changed = now
            change.changed_by_id = user_id
            change.handler_id = handler_id
            self.session.add(change)
            change = self.session.merge(change)
            current = TicketCurrentStatus()
            current.ticket_id = ticket.id
            current.last_change_id = change.id
            current.created = ticket.created
            current.last_change = change.changed
            current.status = change.status
            current.changed_by_id = user_id
            current.handler_id = handler_id
            self.session.add(current)
        return self.session.merge(ticket)
    


    def update_ticket(self, ticket_id, user_id, status, reason, handler_id,
                      description=None):
        now = datetime.now()
        with transaction.manager:
            ticket = self.get(ticket_id)
            change = TicketStatusChange()
            change.ticket_id = ticket_id
            change.status = status
            change.reason = reason
            change.changed = now
            change.changed_by_id = user_id
            change.handler_id = handler_id
            if description is None:
                change.description_id = ticket.description_id
            self.session.add(change)
            change = self.session.merge(change)
            current = self.session.query(TicketCurrentStatus).get(ticket_id)
            current.last_change = now
            current.last_change_id = change.id
            current.status = status
            current.changed_by_id = user_id
            current.handler_id = handler_id
            current = self.session.merge(current)
        return self.session.merge(change)

    def all(self):
        return self.query().all()

    def status(self, ticket_id):
        q = self.session.query(TicketCurrentStatus)
        q = q.filter_by(ticket_id=ticket_id)
        return q.one()

    def get_status(self, ticket_id):
        s = self.status(ticket_id)
        return s.status
    
    def _range_filter(self, query, start, end):
        "start and end are datetime objects"
        query = query.filter(TicketCurrentStatus.last_change >= start)
        query = query.filter(TicketCurrentStatus.last_change <= end)
        return query
    
    def get_current_status_range(self, start, end, timestamps=False):
        if timestamps:
            start, end = convert_range_to_datetime(start, end)
        q = self.session.query(TicketCurrentStatus)
        q = self._range_filter(q, start, end)
        return q.all()
    
    def get_current_status_range_ts(self, start, end):
        return self.get_current_status_range(start, end, timestamps=True)

    def _basic_query(self, user_id, 
                     start=None, end=None, timestamps=False):
        q = self.session.query(TicketCurrentStatus)
        q = q.filter_by(handler_id=user_id)
        if start is not None:
            if timestamps:
                start, end = convert_range_to_datetime(start, end)
            q = self._range_filter(q, start, end)
        return q
    

    def get_assigned_query(self, user_id,
                           start=None, end=None, timestamps=False):
        q = self._basic_query(user_id, start=start, end=end,
                              timestamps=timestamps)
        q = q.filter(TicketCurrentStatus.status != 'closed')
        return q

    def get_assigned(self, user_id,
                     start=None, end=None, timestamps=False):
        q = self.get_assigned_query(user_id, start=start, end=end,
                                    timestamps=timestamps)
        q = q.filter(TicketCurrentStatus.status != 'closed')
        return q.all()

    def get_delegated_query(self, user_id,
                            start=None, end=None, timestamps=False):
        q = self.session.query(TicketCurrentStatus)
        q = q.filter_by(changed_by_id=user_id)
        if start is not None:
            if timestamps:
                start, end = convert_range_to_datetime(start, end)
            q = self._range_filter(q, start, end)
        q = q.filter(TicketCurrentStatus.status != 'closed')
        q = q.filter(TicketCurrentStatus.handler_id != user_id)
        return q

    def get_delegated(self, user_id,
                      start=None, end=None, timestamps=False):
        q = self.get_delegated_query(user_id, start=start, end=end,
                                     timestamps=timestamps)
        q = q.filter(TicketCurrentStatus.status != 'closed')
        return q.all()

    def _get_by_status_query(self, user_id, status,
                             start=None, end=None, timestamps=False):
        q = self._basic_query(user_id, start=start, end=end,
                              timestamps=timestamps)
        q = q.filter_by(status=status)
        return q
    
    def _get_by_status(self, user_id, status,
                       start=None, end=None, timestamps=False):
        q = self._get_by_status_query(user_id, status, start=start, end=end,
                                      timestamps=timestamps)
        return q.all()

    def get_unread(self, user_id,
                   start=None, end=None, timestamps=False):
        return self._get_by_status(user_id, 'opened',
                                   start=start, end=end, timestamps=timestamps)

    def get_pending(self, user_id,
                   start=None, end=None, timestamps=False):
        return self._get_by_status(user_id, 'pending',
                                   start=start, end=end, timestamps=timestamps)
    
    def get_closed(self, user_id,
                   start=None, end=None, timestamps=False):
        return self._get_by_status(user_id, 'closed',
                                   start=start, end=end, timestamps=timestamps)
    



class PhoneCallManager(object):
    def __init__(self, session):
        self.session = session
        self.tickets = TicketManager(self.session)
        
    def query(self):
        q = self.session.query(PhoneCall, TicketCurrentStatus)
        q = q.filter(PhoneCall.ticket_id == TicketCurrentStatus.ticket_id)
        return q
    
    def get(self, id):
        return self.session.query(PhoneCall).get(id)

    def get_status(self, id):
        q = self.query().filter(PhoneCall.id == id)
        return q.one()
    

    
    def new_call(self, received, caller, number,
                 callee_id, received_by_id, title, description):
        with transaction.manager:
            now = datetime.now()
            # the ticket is opened by the receiver
            # and then handled by the callee
            ticket = self.tickets.open(received_by_id,
                                       title, description, callee_id)
            pc = PhoneCall()
            pc.received = received
            pc.caller = caller
            pc.number = number
            pc.callee_id = callee_id
            pc.received_by_id = received_by_id
            pc.ticket_id = ticket.id
            self.session.add(pc)
        return self.session.merge(pc)

    def _received_range_filter(self, query, start, end):
        query = query.filter(PhoneCall.received >= start)
        query = query.filter(PhoneCall.received <= end)
        return query

    def _lastchange_range_filter(self, query, start, end):
        query = query.filter(TicketCurrentStatus.last_change >= start)
        query = query.filter(TicketCurrentStatus.last_change <= end)
        return query
    
    def get_taken_calls(self, user_id, start=None,
                        end=None, timestamps=False):
        q = self.query()
        q = q.filter(PhoneCall.received_by_id == user_id)
        if start is not None:
            if timestamps:
                start, end = convert_range_to_datetime(start, end)
            q = self._received_range_filter(q, start, end)
        q = q.filter(TicketCurrentStatus.status != 'closed')
        return q.all()

    def get_received_calls(self, user_id, start=None,
                           end=None, timestamps=False):
        q = self.query()
        q = q.filter(PhoneCall.callee_id == user_id)
        if start is not None:
            if timestamps:
                start, end = convert_range_to_datetime(start, end)
            q = self._received_range_filter(q, start, end)
        q = q.filter(TicketCurrentStatus.status != 'closed')
        return q.all()

    def get_assigned_calls(self, user_id, start=None,
                           end=None, timestamps=False):
        q = self.query()
        q = q.filter(TicketCurrentStatus.handler_id == user_id)
        if start is not None:
            if timestamps:
                start, end = convert_range_to_datetime(start, end)
            q = self._received_range_filter(q, start, end)
        q = q.filter(TicketCurrentStatus.status != 'closed')
        return q.all()

    def get_unread_calls(self, user_id, start=None,
                           end=None, timestamps=False):
        q = self.query()
        q = q.filter(TicketCurrentStatus.handler_id == user_id)
        if start is not None:
            if timestamps:
                start, end = convert_range_to_datetime(start, end)
            q = self._received_range_filter(q, start, end)
        q = q.filter(TicketCurrentStatus.status == 'opened')
        return q.all()

    def get_pending_calls(self, user_id, start=None,
                           end=None, timestamps=False):
        q = self.query()
        q = q.filter(TicketCurrentStatus.handler_id == user_id)
        if start is not None:
            if timestamps:
                start, end = convert_range_to_datetime(start, end)
            q = self._received_range_filter(q, start, end)
        q = q.filter(TicketCurrentStatus.status == 'pending')
        return q.all()
    
    def get_closed_calls(self, user_id, start=None,
                           end=None, timestamps=False):
        q = self.query()
        q = q.filter(TicketCurrentStatus.handler_id == user_id)
        if start is not None:
            if timestamps:
                start, end = convert_range_to_datetime(start, end)
            q = self._received_range_filter(q, start, end)
        q = q.filter(TicketCurrentStatus.status == 'closed')
        return q.all()
    

    def get_delegated_calls(self, user_id, start=None,
                           end=None, timestamps=False):
        q = self.query()
        q = q.filter(PhoneCall.callee_id == user_id)
        if start is not None:
            if timestamps:
                start, end = convert_range_to_datetime(start, end)
            q = self._received_range_filter(q, start, end)
        q = q.filter(TicketCurrentStatus.status == 'pending')
        q = q.filter(TicketCurrentStatus.changed_by_id != user_id)
        return q.all()
                            

class PhoneCallAdminManager(PhoneCallManager):
    def __init__(self, session):
        super(PhoneCallAdminManager, self).__init__(session)

    def _filter_by_status_name(self, status):
        status_id = self.stypes.get_id(status)
        q = self.session.query(TicketCurrentStatus)
        return q.filter(TicketCurrentStatus.status == status_id)

    def _filter_by_status_name_range(self,
                                     status, start, end,
                                     timestamps=False):
        status_id = self.stypes.get_id(status)
        if timestamps:
            start, end = convert_range_to_datetime(start, end)
        q = self.session.query(TicketCurrentStatus)
        q = self._last_change_range(q, start, end)
        return q.filter(TicketCurrentStatus.status == status_id)

    def get_unread_calls(self, start, end, timestamps=False):
        q = self._filter_by_status_name_range('opened', start, end,
                                              timestamps=timestamps)
        return q.all()

    def get_all_unread_calls(self):
        q = self._filter_by_status_name('opened')
        return q.all()

    def get_pending_calls(self, start, end, timestamps=False):
        q = self._filter_by_status_name_range('pending', start, end,
                                              timestamps=timestamps)
        return q.all()

    def get_all_pending_calls(self):
        q = self._filter_by_status_name('pending')
        return q.all()

    def get_closed_calls(self, start, end, timestamps=False):
        q = self._filter_by_status_name_range('closed', start, end,
                                              timestamps=timestamps)
        return q.all()

    def get_all_closed_calls(self):
        q = self._filter_by_status_name('closed')
        return q.all()
    
    
class ScannedDocumentsManager(object):
    def __init__(self, session):
        self.session = session
        self.directory = None
        
    def query(self):
        q = self.session.query(ScannedDocument)
        return q
    
    def get(self, id):
        return self.query().get(id)

    def set_scans_directory(self, directory):
        self.directory = directory

    def insert_scanned_file(self, filename):
        fullname = os.path.join(self.directory, filename)
        # file must fit in memory
        content = file(fullname).read()
        created = datetime_from_pdf_filename(filename)
        with transaction.manager:
            f = File()
            f.content = content
            self.session.add(f)
            f = self.session.merge(f)
            s = ScannedDocument()
            s.created = created
            s.name = filename
            s.file_id = f.id
            self.session.add(s)
            s = self.session.merge(s)
        return s
    
        
    def get_latest(self):
        try:
            q = self.session.query(ScannedDocument)
            q = q.order_by(ScannedDocument.created.desc())
            return q.first()
        except NoResultFound:
            return None
        

    def update_database(self):
        filenames = get_scanned_filenames(self.directory)
        latest = self.get_latest()
        for filename in filenames:
            dt = datetime_from_pdf_filename(filename)
            if latest is None or dt > latest.created:
                self.insert_scanned_file(filename)

    def _range_filter(self, query, start, end):
        query = query.filter(ScannedDocument.created >= start)
        query = query.filter(ScannedDocument.created <= end)
        return query
    
    def get_documents(self, start, end, timestamps=False):
        if timestamps:
            start, end = convert_range_to_datetime(start, end)
        q = self.session.query(ScannedDocument)
        q = self._range_filter(q, start, end)
        return q.all()
    
                
    
