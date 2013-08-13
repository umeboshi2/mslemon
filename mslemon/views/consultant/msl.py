import urlparse
from datetime import datetime

import colander
import deform

from mslemon.views.base import prepare_layout
from mslemon.views.base import BaseViewer
from trumpet.views.base import render_rst

#FIXME: better module name
from mslemon.managers.consultant.mslll import TicketManager
from mslemon.managers.consultant.clients import ClientManager
from mslemon.managers.consultant.contacts import ContactManager

from mslemon.views.consultant.base import prepare_base_layout

from mslemon.models.usergroup import User
#FIXME: better module name
from mslemon.managers.consultant.mslll import PhoneCallManager

from mslemon.util import send_email_through_smtp_server, make_email_message



def deferred_choices(node, kw):
    choices = kw['choices']
    return deform.widget.SelectWidget(values=choices)

def make_select_widget(choices):
    return deform.widget.SelectWidget(values=choices)


class TakePhoneCallSchema(colander.Schema):
    caller = colander.SchemaNode(
        colander.String(),
        title='Caller',
        )
    callee = colander.SchemaNode(
        colander.Integer(),
        title='Called for',
        widget=deferred_choices,
        )
    number = colander.SchemaNode(
        colander.String(),
        title='Call Back Number',
        widget=deform.widget.TextInputWidget(mask='(999)-999-9999',
                                      mask_placeholder='0'),
        )
    text = colander.SchemaNode(
        colander.String(),
        title='Text',
        widget=deform.widget.TextAreaWidget(rows=10, cols=60),
        missing=colander.null,
        )
    received = colander.SchemaNode(
        colander.DateTime(),
        title='Call received',
        widget=deform.widget.DateTimeInputWidget(),
        )
    send_textmsg = colander.SchemaNode(
        colander.Boolean(),
        title='Send text message to cellphone',
        widget=deform.widget.CheckboxWidget(),
        )

reason_description = """\
You can instruct another user to handle the phone call by
 changing the handler of this call and typing the instructions
 in this area.
"""

class UpdatePhoneCallSchema(colander.Schema):
    status = colander.SchemaNode(
        colander.Integer(),
        title='New Status',
        widget=deferred_choices,
        )
    handler = colander.SchemaNode(
        colander.Integer(),
        title='Handler',
        widget=deferred_choices,
        description='This is the user that will handle this call',
        )
    reason = colander.SchemaNode(
        colander.String(),
        title='Reason',
        description=reason_description,
        widget=deform.widget.TextAreaWidget(rows=10, cols=60),
        )
    
    

def prepare_main_layout(request):
    prepare_base_layout(request)
    layout = request.layout_manager.layout
    layout.title = 'Phone Calls'
    layout.header = 'Phone Calls'
    layout.subheader = 'Telephone Area'


class PhoneCallFrag(BaseViewer):
    def __init__(self, request):
        super(PhoneCallFrag, self).__init__(request)
        self.phonecalls = PhoneCallManager(self.request.db)
        calltypes = ['received', 'assigned', 'delegated', 'unread',
                     'pending', 'closed']
        self.dtformat = '%A - %B %d %H:%m'
        self._dispatch_table = {}
        for calltype in calltypes:
            key = 'all_%scalls' % calltype
            method = 'get_all_%s_calls' % calltype
            self._dispatch_table[key] = getattr(self, method)
        self.context = self.request.matchdict['context']
        self._view = self.context
        self.dispatch()

    def get_all_received_calls(self):
        user_id = self.request.session['user'].id
        calls = self.phonecalls.get_all_received_calls(user_id)
        env = dict(calls=calls, dtformat=self.dtformat)
        template = 'mslemon:templates/consult/listphonecalls.mako'
        self.response = self.render(template, env)
        

    def get_all_assigned_calls(self):
        user_id = self.request.session['user'].id
        clist = self.phonecalls.get_all_assigned_calls(user_id)
        env = dict(clist=clist, dtformat=self.dtformat)
        template = 'mslemon:templates/consult/listphonecallsstatus.mako'
        self.response = self.render(template, env)
        
    def get_all_delegated_calls(self):
        user_id = self.request.session['user'].id
        clist = self.phonecalls.get_all_delegated_calls(user_id)
        env = dict(clist=clist, dtformat=self.dtformat)
        template = 'mslemon:templates/consult/listphonecallsstatus.mako'
        self.response = self.render(template, env)

    def get_all_unread_calls(self):
        user_id = self.request.session['user'].id
        clist = self.phonecalls.get_all_unread_calls(user_id)
        env = dict(clist=clist, dtformat=self.dtformat)
        template = 'mslemon:templates/consult/listphonecallsstatus.mako'
        self.response = self.render(template, env)

    def get_all_pending_calls(self):
        user_id = self.request.session['user'].id
        clist = self.phonecalls.get_all_pending_calls(user_id)
        env = dict(clist=clist, dtformat=self.dtformat)
        template = 'mslemon:templates/consult/listphonecallsstatus.mako'
        self.response = self.render(template, env)

    def get_all_closed_calls(self):
        user_id = self.request.session['user'].id
        clist = self.phonecalls.get_all_closed_calls(user_id)
        env = dict(clist=clist, dtformat=self.dtformat)
        template = 'mslemon:templates/consult/listphonecallsstatus.mako'
        self.response = self.render(template, env)

    

class PhoneCallViewer(BaseViewer):
    def __init__(self, request):
        super(PhoneCallViewer, self).__init__(request)
        prepare_main_layout(self.request)
        self.phonecalls = PhoneCallManager(self.request.db)
        self.dtformat = '%A - %B %d %H:%m'
        
        self._dispatch_table = dict(
            list=self.main_phone_view,
            takencalls=self.list_taken_calls,
            add=self.take_call,
            viewcall=self.view_call,
            updatephonecall=self.update_call,)
        self.context = self.request.matchdict['context']
        self._view = self.context

        user_id = self.request.session['user'].id
        url = self.url(context='takencalls', id=user_id)
        label = "Calls I've taken"
        self.layout.ctx_menu.append_new_entry(label, url)

        self.dispatch()

    def _take_call_form_submitted(self, form):
        controls = self.request.POST.items()
        self.layout.subheader = "Phone call submitted to database"
        try:
            data = form.validate(controls)
        except deform.ValidationFailure, e:
            self.layout.content = e.render()
            return
        # strip tzinfo that is attached by deform
        if data['received'].tzinfo is not None:
            data['received'] = data['received'].replace(tzinfo=None)
        fields = ['received', 'caller', 'number', 'text', 'callee']
        values = [data[f] for f in fields]
        received_by = self.request.session['user'].id
        values.append(received_by)
        pcall = self.phonecalls.new_call(*values)
        #self.layout.subheader = "Phone Call taken: %s" % pcall
        if data['send_textmsg']:
            self._send_text_notification(pcall)
                

    def _make_text_message(self, pcall):
        settings = self.request.registry.settings
        url = self.url(context='viewcall', id=pcall.id)
        path = urlparse.urlparse(url).path
        url = settings['mslemon.public_url'] + path 
        text = "%s\n\n" % url
        text += "%s\n\n" % pcall.number
        return text
    
    def _send_text_notification(self, pcall):
        callee = self.request.db.query(User).get(pcall.callee)
        settings = self.request.registry.settings
        cfg = callee.config.get_config()
        if cfg.get('main', 'sms_email_address'):
            prefix = 'mslemon.smtp.'
            server = settings[prefix + 'server']
            port = int(settings[prefix + 'port'])
            login = settings[prefix + 'login']
            password = settings[prefix + 'password']
            subject = "%s just called" % pcall.caller
            message = self._make_text_message(pcall)
            sender = login
            receiver = cfg.get('main', 'sms_email_address')
            msg = make_email_message(subject, message, sender, receiver)
            send_email_through_smtp_server(settings, msg, sender, receiver)
    
    
    def take_call(self):
        schema = TakePhoneCallSchema()
        users = self.request.db.query(User).all()
        skey = 'mslemon.admin.admin_username'
        admin_username = self.request.registry.settings.get(skey, 'admin')
        choices = [(u.id, u.username) \
                       for u in users if u.username != admin_username]
        schema['callee'].widget = make_select_widget(choices)
        form = deform.Form(schema, buttons=('submit',))
        self.layout.resources.deform_auto_need(form)
        self.layout.resources.azure3.need()
        if 'submit' in self.request.POST:
            self._take_call_form_submitted(form)
        else:
            formdata = dict(received=datetime.now())
            rendered = form.render(formdata)
            self.layout.content = rendered
        
    
    def list_calls(self):
        pass

    def list_taken_calls(self):
        user_id = self.request.session['user'].id
        calls = self.phonecalls.get_all_taken_calls(user_id)
        env = dict(calls=calls, dtformat=self.dtformat)
        template = 'mslemon:templates/consult/listphonecalls.mako'
        content = self.render(template, env)
        self.layout.content = content
        
    def taken_calls_calendar(self):
        pass
    
    def view_call(self):
        id = int(self.request.matchdict['id'])
        pcall = self.phonecalls.get(id)
        template = 'mslemon:templates/consult/viewphonecall.mako'
        rst = render_rst
        db = self.request.db
        pcm = self.phonecalls
        env = dict(pcall=pcall, rst=rst, db=db, User=User, pcm=pcm)
        content = self.render(template, env)
        self.layout.content = content
        
    
    def main_phone_view(self):
        template = 'mslemon:templates/consult/main-phone-view.mako'
        default_view = 'agendaDay'
        calltypes = ['received', 'assigned', 'delegated', 'unread',
                     'pending', 'closed']
        calendar_urls = {}
        list_urls = {}
        id_ = 'calls'
        for calltype in calltypes:
            route = 'consult_json'
            context = '%scalls' % calltype
            url = self.request.route_url(route, context=context, id=id_)
            calendar_urls[calltype] = url
            route = 'consultant_phonefrag'
            context = 'all_%scalls' % calltype
            url = self.request.route_url(route, context=context, id=id_)
            list_urls[calltype] = url
            user = self.get_current_user()
            cfg = user.config.get_config()
            calviews = dict(cfg.items('phonecall_views'))
        env = dict(calendar_urls=calendar_urls,
                   list_urls=list_urls,
                   calviews=calviews)
        content = self.render(template, env)
        self.layout.content = content
        self.layout.resources.phone_calendar.need()
        self.layout.resources.cornsilk.need()
        self.layout.resources.main_phone_view.need()
        
    def update_call(self):
        call_id = int(self.request.matchdict['id'])
        schema = UpdatePhoneCallSchema()
        clist = self.phonecalls.stypes.all()
        choices = [(c.id, c.name) for c in clist if c.name != 'opened']
        schema['status'].widget = make_select_widget(choices)
        users = self.request.db.query(User).all()
        skey = 'mslemon.admin.admin_username'
        admin_username = self.request.registry.settings.get(skey, 'admin')
        choices = [(u.id, u.username) \
                       for u in users if u.username != admin_username]
        schema['handler'].widget = make_select_widget(choices)
        form = deform.Form(schema, buttons=('submit',))
        self.layout.resources.deform_auto_need(form)
        if 'submit' in self.request.POST:
            controls = self.request.POST.items()
            self.layout.subheader = 'Phone Call Update Submitted'
            try:
                data = form.validate(controls)
            except deform.ValidationFailure, e:
                self.layout.content = e.render()
                return
            user_id = self.request.session['user'].id
            reason = data['reason']
            handler = int(data['handler'])
            status_id = int(data['status'])
            status = self.phonecalls.update_call(call_id, user_id,
                                                 status_id, reason,
                                                 handler)
            content = '<p>Ticket updated.</p>'
            self.layout.content = content
            return
        status = self.phonecalls.status(call_id)
        formdata = dict(handler=status.handler)
        self.layout.content = form.render(formdata)
        self.layout.subheader = 'Update status of phone call'
        
        
                          
        
        
MSLViewer = PhoneCallViewer
