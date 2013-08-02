from datetime import datetime

import transaction
from formencode.htmlgen import html
from sqlalchemy.orm.exc import NoResultFound

from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.security import authenticated_userid

from trumpet.security import check_password
from trumpet.security import encrypt_password

from mslemon.views.base import BaseViewer

from mslemon.models.base import DBSession
from mslemon.models.consultant import Contact
from mslemon.models.usergroup import User, Password

import colander
import deform

class ChangePasswordSchema(colander.Schema):
    oldpass = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(min=5, max=100),
        widget=deform.widget.PasswordWidget(size=20),
        description="Please enter your password.")
    newpass = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(min=5, max=100),
        widget=deform.widget.PasswordWidget(size=20),
        description="Please enter a new password.")
    confirm = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(min=5, max=100),
        widget=deform.widget.PasswordWidget(size=20),
        description="Please confirm the new password.")



def get_password(request):
    db = request.db
    user_id = request.session['user'].id
    return db.query(Password).filter_by(user_id=user_id).one()
    
def check_old_password(request, password):
    dbpass = get_password(request)
    return check_password(dbpass.password, password)


class MainViewer(BaseViewer):
    def __init__(self, request):
        super(MainViewer, self).__init__(request)
        self.context = self.request.matchdict['context']

        self.layout.header = "User Preferences"
        self.layout.title = "User Preferences"
        # make left menu
        entries = []
        url = request.route_url('user', context='chpasswd')
        entries.append(('Change Password', url))
        url = request.route_url('user', context='status')
        entries.append(('Status', url))
        menu = self.layout.ctx_menu
        menu.set_new_entries(entries, header='Preferences')
        # make dispatch table
        self._cntxt_meth = dict(
            chpasswd=self.change_password,
            preferences=self.preferences_view,
            )

        # dispatch context request
        if self.context in self._cntxt_meth:
            self._cntxt_meth[self.context]()
        else:
            msg = 'Undefined Context: %s' % self.context
            self.layout.content = '<b>%s</b>' % msg
        

    def preferences_view(self):
        self.layout.content = "Here are your preferences."
        
    def change_password(self):
        schema = ChangePasswordSchema()
        form = deform.Form(schema, buttons=('update',))
        self.layout.resources.deform_auto_need(form)
        if 'update' in self.request.params:
            controls = self.request.POST.items()
            try:
                data = form.validate(controls)
            except deform.ValidationFailure, e:
                self.layout.content = e.render()
                return
            user = self.request.session['user']
            if data['oldpass'] == data['newpass']:
                self.layout.content = "Password Unchanged"
                return
            if data['newpass'] != data['confirm']:
                self.layout.content = "Password Mismatch."
                return
            if check_old_password(self.request, data['oldpass']):
                newpass = data['newpass']
                dbpass = get_password(self.request)
                dbpass.password = encrypt_password(newpass)
                with transaction.manager:
                    self.request.db.add(dbpass)
                self.layout.content = "Password Changed."
                return
            else:
                self.layout.content = "Authentication Failed."
                return
        self.layout.content = form.render()
        
    
        

