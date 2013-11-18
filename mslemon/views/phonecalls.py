import urlparse
from datetime import datetime, timedelta
from ConfigParser import NoSectionError, DuplicateSectionError

from pyramid.httpexceptions import HTTPFound

from sqlalchemy.orm.exc import NoResultFound

import colander
import deform

from mslemon.views.base import prepare_layout
from mslemon.views.base import BaseViewer
from trumpet.views.base import render_rst

from mslemon.managers.tickets import TicketManager
from mslemon.managers.phonecalls import PhoneCallManager

from mslemon.views.consultant.base import prepare_base_layout
from mslemon.views.schema import deferred_choices, make_select_widget

from mslemon.models.usergroup import User
from mslemon.models.misslemon import PhoneCall

from mslemon.util import send_email_through_smtp_server, make_email_message



def prepare_main_layout(request):
    prepare_base_layout(request)
    layout = request.layout_manager.layout
    layout.title = 'MSL Phone Calls'
    layout.header = 'MSL Phone Calls'
    layout.subheader = 'MSL Phone Call Area'



class PhoneCallFrag(BaseViewer):
    def __init__(self, request):
        super(PhoneCallFrag, self).__init__(request)
        self._template = 'mslemon:templates/msl/list-phonecalls.mako'
        self.pcm = PhoneCallManager(self.request.db)
        call_types = ['received', 'taken',
                      'assigned', 'delegated', 'unread',
                     'pending', 'closed']
        self.dtformat = '%A - %B %d %H:%m'
        self.env = dict(dtformat=self.dtformat)
        self.render_call_list()
        
    def _getuserid(self):
        return self.request.session['user'].id

    def _render_calls(self, call_type):
        user_id = self._getuserid()
        method = getattr(self.pcm, 'get_%s_calls' % call_type)
        clist = method(user_id)
        env = self.env.update(clist=clist)
        self.response = self.render(self._template, self.env)
        
    def render_call_list(self):
        context = self.request.matchdict['context']
        self._render_calls(context)
        
                                         
class PhoneCallJSONViewer(BaseViewer):
    def __init__(self, request):
        super(PhoneCallJSONViewer, self).__init__(request)
        self.pcm = PhoneCallManager(self.request.db)
        self.render_calls()

    def serialize_phonecall_for_calendar(self, pcall, cstatus):
        url = self.request.route_url('msl_phonecalls',
                                     context='view',
                                     id=pcall.id)
        start = pcall.received
        end = cstatus.last_change
        thirty_minutes = timedelta(minutes=30)
        if end - start < thirty_minutes:
            end = start + thirty_minutes
            
        title = pcall.caller
        data = dict(id=pcall.id, start=start.isoformat(),
                    end=end.isoformat(),
                    title=title, url=url)
        if cstatus.status == 'pending':
            data['color'] = 'blue'
            if pcall.callee_id != cstatus.handler_id:
                data['color'] = 'red'
        return data

    def _get_start_end_userid(self):
        start = self.request.GET['start']
        end = self.request.GET['end']
        user_id = self.request.session['user'].id
        return start, end, user_id

    def render_calls(self):
        start, end, user_id = self._get_start_end_userid()
        serialize = self.serialize_phonecall_for_calendar
        context = self.request.matchdict['context']
        method = getattr(self.pcm, 'get_%s_calls' % context)
        clist = method(user_id, start, end, timestamps=True)
        self.response = [serialize(pc, cstatus) for pc, cstatus in clist]
        





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
    subject = colander.SchemaNode(
        colander.String(),
        title='Subject',
        missing=colander.null,
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
    
        
class MSLPhoneViewer(BaseViewer):
    def __init__(self, request):
        super(MSLPhoneViewer, self).__init__(request)
        prepare_main_layout(self.request)
        self.tickets = TicketManager(self.request.db)
        self.pcm = PhoneCallManager(self.request.db)
        self.dtformat = '%A - %B %d %H:%m'
        
        self._dispatch_table = dict(
            main=self.main_phonecall_view,
            add=self.take_phonecall,
            view=self.view_phonecall,
            update=self.update_phonecall,)
        self.context = self.request.matchdict['context']
        self._view = self.context

        self.dispatch()

    def main_phonecall_view(self):
        template = 'mslemon:templates/msl/main-phone-view.mako'
        default_view = 'agendaDay'
        call_types = ['received', 'taken',
                      'assigned', 'delegated', 'unread',
                     'pending', 'closed']
        calendar_urls = {}
        list_urls = {}
        for call_type in call_types:
            route = 'msl_pcalljson'
            kw = dict(context=call_type, id='phonecalls')
            url = self.request.route_url(route, **kw)
            calendar_urls[call_type] = url
            route = 'msl_pcallfrag'
            url = self.request.route_url(route, **kw)
            list_urls[call_type] = url
        user = self.get_current_user()
        cfg = user.config.get_config()
        try:
            calviews = dict(cfg.items('phonecall_views'))
        except NoSectionError:
            calviews = dict(((k, 'month') for k in call_types))
            cfg.add_section('phonecall_views')
            for k in calviews:
                cfg.set('phonecall_views', k, calviews[k])
        env = dict(calendar_urls=calendar_urls,
                   list_urls=list_urls,
                   calviews=calviews)
        content = self.render(template, env)
        self.layout.content = content
        self.layout.resources.main_phone_view.need()
        self.layout.resources.cornsilk.need()


    def _make_text_message(self, pcall):
        settings = self.request.registry.settings
        url = self.url(context='view', id=pcall.id)
        path = urlparse.urlparse(url).path
        url = settings['mslemon.public_url'] + path 
        text = "%s\n\n" % url
        text += "%s\n\n" % pcall.number
        return text
    
    def _send_text_notification(self, pcall):
        callee = pcall.callee
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
        for field in ['subject', 'text']:
            if data[field] is colander.null:
                data[field] = ''
        fields = ['received', 'caller', 'number', 'text', 'callee']
        fields = ['received', 'caller', 'number', 'callee']
        values1 = [data[f] for f in fields]
        values2 = [data[f] for f in ['subject', 'text']]
        received_by = self.request.session['user'].id
        values = values1 + [received_by] + values2
        pcall = self.pcm.new_call(*values)
        if data['send_textmsg']:
            self._send_text_notification(pcall)
        self.response = HTTPFound(self.url(context='view', id=pcall.id))
        

    def take_phonecall(self):
        schema = TakePhoneCallSchema()
        users = self.request.db.query(User).all()
        skey = 'mslemon.admin.admin_username'
        admin_username = self.request.registry.settings.get(skey, 'admin')
        choices = [(u.id, u.username) \
                       for u in users if u.username != admin_username]
        schema['callee'].widget = make_select_widget(choices)
        form = deform.Form(schema, buttons=('submit',))
        #self.layout.resources.screen.need()
        self.layout.resources.deform_auto_need(form)
        self.layout.resources.azure3.need()
        if 'submit' in self.request.POST:
            self._take_call_form_submitted(form)
        else:
            formdata = dict(received=datetime.now())
            rendered = form.render(formdata)
            self.layout.content = rendered
        
    

    def view_phonecall(self):
        id = int(self.request.matchdict['id'])
        pcall = self.pcm.get(id)
        template = 'mslemon:templates/msl/view-phonecall.mako'
        rst = render_rst
        db = self.request.db
        pcm = self.pcm
        env = dict(pcall=pcall, rst=rst, db=db, User=User, pcm=pcm)
        content = self.render(template, env)
        self.layout.content = content

    def update_phonecall(self):
        self.response = HTTPFound(self.url(context='view', id=pcall.id))


    
    

        
                          
        
        

