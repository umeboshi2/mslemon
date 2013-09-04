import os
from datetime import datetime, timedelta

import transaction
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import desc
from sqlalchemy import func

from mslemon.managers.util import convert_range_to_datetime

from trumpet.models.sitecontent import SiteText

#FIXME: better module name
from mslemon.models.misslemon import Description
from mslemon.models.misslemon import Ticket, TicketCurrentStatus
from mslemon.models.misslemon import TicketStatusChange
from mslemon.models.misslemon import TicketDocument

class WikiManager(object):
    def __init__(self, session):
        self.session = session

    def query(self):
        return self.session.query(SiteText).filter_by(type='tutwiki')

    def get(self, id):
        return self.session.query(SiteText).get(id)

    def getbyname(self, name):
        q = self.query()
        q = q.filter_by(name=name)
        try:
            return q.one()
        except NoResultFound:
            return None
        
    def add_page(self, name, content):
        now = datetime.now()
        page = SiteText(name, content, type='tutwiki')
        page.created = now
        page.modified = now
        with transaction.manager:
            self.session.add(page)
        return self.session.merge(page)
    
    def update_page(self, id, content):
        with transaction.manager:
            now = datetime.now()
            page = self.get(id)
            page.content = content
            page.modified = now
            self.session.add(page)
        return self.session.merge(page)

    def list_pages(self):
        return self.query().all()
