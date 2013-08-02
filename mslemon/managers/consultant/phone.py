from datetime import datetime

import transaction

from mslemon.models.consultant import PhoneCall
from mslemon.models.consultant import PhoneCallStatusType
from mslemon.models.consultant import PhoneCallStatus
from mslemon.models.consultant import PhoneCallCurrentStatus

from mslemon.managers.util import convert_range_to_datetime

class StatusTypeManager(object):
    def __init__(self, session):
        self.session = session

    def query(self):
        return self.session.query(PhoneCallStatusType)

    def get(self, id):
        return self.query().get(id)

    def get_id(self, status):
        return self.query().filter_by(name=status).one().id

    def all(self):
        return self.query().all()
    
        


class PhoneCallManager(object):
    def __init__(self, session):
        self.session = session
        self.stypes = StatusTypeManager(self.session)

    def query(self):
        return self.session.query(PhoneCall)

    def get(self, id):
        return self.query().get(id)

    def new_call(self, received, caller, number,
                 text, callee, received_by):
        with transaction.manager:
            now = datetime.now()
            pc = PhoneCall()
            pc.received = received
            pc.caller = caller
            pc.number = number
            pc.text = text
            pc.callee = callee
            pc.received_by = received_by
            self.session.add(pc)
            pc = self.session.merge(pc)
            status_type_id = self.stypes.get_id('opened')
            status = PhoneCallStatus()
            status.call_id = pc.id
            status.status = status_type_id
            status.reason = "New Phone Call"
            status.changed = now
            status.changed_by_id = received_by
            status.handler = callee
            self.session.add(status)
            cstatus = PhoneCallCurrentStatus()
            cstatus.call_id = pc.id
            cstatus.created = received
            cstatus.last_change = now
            cstatus.status = status_type_id
            cstatus.handler = callee
            self.session.add(cstatus)
        return self.session.merge(pc)
    
            
    def update_call(self, call_id, user_id, status_id, reason, handler):
        now = datetime.now()
        with transaction.manager:
            status = PhoneCallStatus()
            status.call_id = call_id
            status.status = status_id
            status.reason = reason
            status.changed = now
            status.changed_by_id = user_id
            status.handler = handler
            self.session.add(status)
            cstatus = self.session.query(PhoneCallCurrentStatus).get(call_id)
            cstatus.handler = handler
            cstatus.status = status_id
            cstatus.last_change = now
            cstatus = self.session.merge(cstatus)
        return self.session.merge(status)

    def status(self, call_id):
        q = self.session.query(PhoneCallCurrentStatus)
        q = q.filter_by(call_id=call_id)
        return q.one()

    def get_status(call_id):
        s = self.status(call_id)
        st = self.stypes.get(s.status)
        return st.name
    
    def _range_filter(self, query, start, end):
        # start, end are datetime objects
        query = query.filter(PhoneCall.received >= start)
        query = query.filter(PhoneCall.received <= end)
        return query

    def _last_change_range(self, query, start, end):
        query = query.filter(PhoneCallCurrentStatus.last_change >= start)
        query = query.filter(PhoneCallCurrentStatus.last_change <= end)
        return query

    def get_calls_range(self, start, end, timestamps=False):
        if timestamps:
            start, end = convert_range_to_datetime(start, end)
        q = self.query()
        q = self._range_filter(q, start, end)
        return q.all()

    def get_calls_range_ts(self, start, end):
        return self.get_calls_range(start, end, timestamps=True)
    
    def get_calls_for_user(self, user_id, start, end, timestamps=False):
        closed_id = self.stypes.get_id('closed')
        if timestamps:
            start, end = convert_range_to_datetime(start, end)
        q = self.query().filter_by(callee=user_id)
        q = self._range_filter(q, start, end)
        #q = q.filter(PhoneCallCurrentStatus.status != closed_id)
        calls = [c for c in q.all() if c.status[0].status != closed_id]
        return calls
    

    def get_all_calls_for_user(self, user_id):
        q = self.query().filter_by(received_by=user_id)
        return q.all()
    
    def get_open_and_pending_calls(self,
                                   user_id, start, end, timestamps=False):
        closed_id = self.stypes.get_id('closed')
        if timestamps:
            start, end = convert_range_to_datetime(start, end)
        q = self.session.query(PhoneCallCurrentStatus)
        q = q.filter_by(handler=user_id)
        q = self._last_change_range(q, start, end)
        q = q.filter(PhoneCallCurrentStatus.status != closed_id)
        return q.all()

    def _get_by_status_id(self,
                          user_id, start, end, timestamps, status):
        status_id = self.stypes.get_id(status)
        if timestamps:
            start, end = convert_range_to_datetime(start, end)
        q = self.session.query(PhoneCallCurrentStatus)
        q = q.filter_by(handler=user_id)
        q = self._last_change_range(q, start, end)
        q = q.filter(PhoneCallCurrentStatus.status == status_id)
        return q.all()
    
    
    def get_closed_calls(self,
                         user_id, start, end, timestamps=False):
        return self._get_by_status_id(
            user_id, start, end, timestamps, 'closed')

    def get_newly_opened_calls(self,
                               user_id, start, end, timestamps=False):
        return self._get_by_status_id(
            user_id, start, end, timestamps, 'opened')

    def get_pending_calls(self,
                          user_id, start, end, timestamps=False):
        return self._get_by_status_id(
            user_id, start, end, timestamps, 'pending')

    def get_delegated_calls(self, user_id, start, end, timestamps=False):
        status_id = self.stypes.get_id('pending')
        if timestamps:
            start, end = convert_range_to_datetime(start, end)
        q = self.session.query(PhoneCallCurrentStatus)
        q = self._last_change_range(q, start, end)
        q = q.filter(PhoneCallCurrentStatus.status == status_id)
        q = q.filter(PhoneCallCurrentStatus.handler != user_id)
        return [r for r in q if r.phone_call.callee == user_id]

