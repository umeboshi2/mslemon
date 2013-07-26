import transaction

from mslemon.models.consultant import PhoneCall

from mslemon.managers.util import convert_range_to_datetime

class PhoneCallManager(object):
    def __init__(self, session):
        self.session = session

    def query(self):
        return self.session.query(PhoneCall)

    def get(self, id):
        return self.query().get(id)

    def new_call(self, received, caller, number, text, callee):
        with transaction.manager:
            pc = PhoneCall()
            pc.received = received
            pc.caller = caller
            pc.number = number
            pc.text = text
            pc.callee = callee
            self.session.add(pc)
            #pc = self.session.merge(pc)
        return self.session.merge(pc)

    def _range_filter(self, query, start, end):
        # start, end are datetime objects
        query.filter(PhoneCall.received >= start)
        query.filter(PhoneCall.received <= end)
        return query
    
    def get_calls_range(self, start, end):
        "start, end are datetime objects"
        q = self.query()
        q = self._range_filter(q, start, end)
        return q.all()

    def get_calls_range_ts(self, start, end):
        "start, end are timestamps"
        start, end = convert_range_to_datetime(start, end)
        return self.get_calls_range(start, end)
    
    
