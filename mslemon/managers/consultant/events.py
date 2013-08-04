from datetime import datetime

import transaction

from mslemon.models.consultant import Event, User

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
    
        


class EventManager(object):
    def __init__(self, session):
        self.session = session

    def query(self):
        return self.session.query(Event)

    def get(self, id):
        return self.query().get(id)

    
    def _range_filter(self, query, start, end):
        # start, end are datetime objects
        query = query.filter(Event.start_date >= start)
        query = query.filter(Event.start_date <= end)
        return query

    def ranged_events(self, start, end, timestamps=False):
        if timestamps:
            start, end = convert_range_to_datetime(start, end)
        q = self.query()
        q = self._range_filter(q, start, end)
        return q.all()
