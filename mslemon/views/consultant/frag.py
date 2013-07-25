import string

import colander
import deform
import vobject

from sqlalchemy.exc import IntegrityError

from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound

from mslemon.views.base import prepare_layout
from mslemon.views.base import BaseViewer


from mslemon.managers.consultant.contacts import ContactManager

from mslemon.views.consultant.base import prepare_base_layout

phone_re = '\((?P<areacode>[1-9][0-9][0-9])\)-(?P<prefix>[0-9][0-9][0-9])-(?P<suffix>[0-9][0-9][0-9][0-9])'
letters = string.ascii_letters[26:]

    
class FragViewer(BaseViewer):
    def __init__(self, request):
        BaseViewer.__init__(self, request)
        self.contacts = ContactManager(self.request.db)
        
        self._dispatch_table = dict(
            contactlist=self.list_contacts,)
        self.context = self.request.matchdict['context']
        self._view = self.context
        #self.response = "NOTHING HAPPENED"
        self.dispatch()
        
    def list_contacts(self):
        id = self.request.matchdict['id']
        q = self.contacts.query()
        Contact = self.contacts.base
        if id != 'ALL':
            q = q.filter(Contact.lastname.like('%s%%' % id))
        q = q.order_by(Contact.lastname)
        contacts = q.all()
        env = dict(contacts=contacts)
        template = 'mslemon:templates/consult/contact-list.mako'
        self.response = self.render(template, env)
        
        
