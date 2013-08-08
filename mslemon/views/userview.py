from datetime import datetime

import transaction
from formencode.htmlgen import html
from sqlalchemy.orm.exc import NoResultFound

from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.security import authenticated_userid

from trumpet.security import check_password
from trumpet.security import encrypt_password

from mslemon.managers.admin.users import UserManager
from mslemon.views.base import BaseViewer

from mslemon.models.base import DBSession
from mslemon.models.consultant import Contact
from mslemon.models.usergroup import User, Password
from mslemon.models.usergroup import UserConfig

#########################
#[main]
#sms_email_address = 6015551212@vtext.com
#
#[phonecall_views]
#received = agendaDay
#assigned = agendaWeek
#delegated = agendaWeek
#unread = agendaWeek
#pending = agendaWeek
#closed = month
#
#########################

def get_option(db, user_id, section, option):
    q = db.query(UserOption).filter_by(user_id=user_id)
    q = q.filter_by(section=section).filter_by(option=option)
    return q.one().value

import colander
import deform

def deferred_choices(node, kw):
    choices = kw['choices']
    return deform.widget.SelectWidget(values=choices)

def make_select_widget(choices):
    return deform.widget.SelectWidget(values=choices)


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


#_view_choices = ['agendaDay', 'agendaWeek', 'month']
_view_choices = [(0, 'agendaDay'), (1, 'agendaWeek'), (2, 'month')]

ViewChoices = dict(_view_choices)
ViewChoiceLookup = dict([(v, k) for k,v in ViewChoices.items()])
PhoneCallViews = ['received', 'assigned', 'delegated', 'unread',
                  'pending', 'closed']


class PhoneCallViewOptionsSchema(colander.Schema):
    received = colander.SchemaNode(
        colander.String(),
        title='Received',
        widget=deferred_choices,
        )
    assigned = colander.SchemaNode(
        colander.String(),
        title='Assigned',
        widget=deferred_choices,
        )
    delegated = colander.SchemaNode(
        colander.String(),
        title='Delegated',
        widget=deferred_choices,
        )
    unread = colander.SchemaNode(
        colander.String(),
        title='Unread',
        widget=deferred_choices,
        )
    pending = colander.SchemaNode(
        colander.String(),
        title='Pending',
        widget=deferred_choices,
        )
    closed = colander.SchemaNode(
        colander.String(),
        title='Closed',
        widget=deferred_choices,
        )
    


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
        self.users = UserManager(self.request.db)
        self.context = self.request.matchdict['context']
        self.layout.header = "User Preferences"
        self.layout.title = "User Preferences"
        # make left menu
        entries = []
        url = request.route_url('user', context='chpasswd')
        entries.append(('Change Password', url))
        url = request.route_url('user', context='status')
        entries.append(('Status', url))
        url = request.route_url('user', context='phonecallprefs')
        entries.append(('Phone Call Prefs', url))
        menu = self.layout.ctx_menu
        menu.set_new_entries(entries, header='Preferences')
        # make dispatch table
        self._cntxt_meth = dict(
            chpasswd=self.change_password,
            phonecallprefs=self.phone_call_preferences,
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

    def phone_call_preferences(self):
        schema = PhoneCallViewOptionsSchema()
        choices = _view_choices
        for key in PhoneCallViews:
            schema[key].widget = make_select_widget(choices)
        form = deform.Form(schema, buttons=('submit',))
        self.layout.resources.deform_auto_need(form)
        if 'submit' in self.request.POST:
            self._phone_call_pref_form_submitted(form)
        else:
            user = self.get_current_user()
            if user.config is not None:
                cfg = user.config.get_config()
                data = dict(cfg.items('phonecall_views'))
                data = dict(((k, ViewChoiceLookup[data[k]]) for k in data))
            else:
                data = {}
            self.layout.content = form.render(data)

    def _phone_call_pref_form_submitted(self, form):
        db = self.request.db
        controls = self.request.POST.items()
        try:
            data = form.validate(controls)
        except deform.ValidationFailure, e:
            self.layout.content = e.render()
            return
        fields = PhoneCallViews
        section = 'phonecall_views'
        values = [ViewChoices[int(data[f])] for f in fields]
        options = dict(zip(fields, values))
        user = self.get_current_user()
        if user.config is None:
            self.users.Make_default_config(user.id)
            user = self.get_current_user()
        #import pdb ; pdb.set_trace()
        cfg = user.config.get_config()
        for o in options:
            cfg.set(section, o, options[o])
        user.config.set_config(cfg)
        with transaction.manager:
            db.add(user.config)
        
                
        
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
        
    
        

