import urlparse
from datetime import datetime
from ConfigParser import NoSectionError, DuplicateSectionError

import colander
import deform

from mslemon.views.base import prepare_layout
from mslemon.views.base import BaseViewer
from trumpet.views.base import render_rst

#FIXME: better module name
from mslemon.managers.consultant.misslemon import TicketManager
from mslemon.managers.consultant.misslemon import PhoneCallManager

from mslemon.views.consultant.base import prepare_base_layout

from mslemon.models.usergroup import User

from mslemon.util import send_email_through_smtp_server, make_email_message



def deferred_choices(node, kw):
    choices = kw['choices']
    return deform.widget.SelectWidget(values=choices)

def make_select_widget(choices):
    return deform.widget.SelectWidget(values=choices)

class NewTicketSchema(colander.Schema):
    handler = colander.SchemaNode(
        colander.Integer(),
        title='Handler',
        widget=deferred_choices,
        description='This is the user that will handle this ticket',
        )
    title = colander.SchemaNode(
        colander.String(),
        title='Title',
        )
    description = colander.SchemaNode(
        colander.String(),
        title='Description',
        widget=deform.widget.TextAreaWidget(rows=10, cols=60),
        missing=colander.null,
        )
    send_textmsg = colander.SchemaNode(
        colander.Boolean(),
        title="Send text message to handler's cellphone",
        widget=deform.widget.CheckboxWidget(),
        )
    
reason_description = """\
You can instruct another user to handle the ticket by
 changing the handler of this ticket and typing the instructions
 in this area.
"""
class UpdateTicketSchema(colander.Schema):
    status = colander.SchemaNode(
        colander.Integer(),
        title='New Status',
        widget=deferred_choices,
        )
    handler = colander.SchemaNode(
        colander.Integer(),
        title='Handler',
        widget=deferred_choices,
        description='This is the user that will handle this ticket',
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
    layout.title = 'MSL'
    layout.header = 'MSL'
    layout.subheader = 'MSL Ticket Area'



class TicketFrag(BaseViewer):
    def __init__(self, request):
        super(TicketFrag, self).__init__(request)
        self._template = 'mslemon:templates/consult/msl-list-tickets.mako'
        self.tickets = TicketManager(self.request.db)
        tkt_types = ['assigned', 'delegated', 'unread',
                     'pending', 'closed']
        self.dtformat = '%A - %B %d %H:%m'
        self.env = dict(dtformat=self.dtformat)
        self.render_ticket_list()
        
    def _getuserid(self):
        return self.request.session['user'].id

    def _render_tickets(self, tkt_type):
        user_id = self._getuserid()
        method = getattr(self.tickets, 'get_%s' % tkt_type)
        tlist = method(user_id)
        env = self.env.update(tlist=tlist)
        self.response = self.render(self._template, self.env)
        
    def render_ticket_list(self):
        context = self.request.matchdict['context']
        self._render_tickets(context)
        
class BaseJSONViewer(BaseViewer):
    def __init__(self, request):
        super(BaseJSONViewer, self).__init__(request)
        self.tickets = TicketManager(self.request.db)
        self.context = None
        self._dispatch_table = dict(
            assigned_tickets=self.get_assigned_tickets,
            delegated_tickets=self.get_delegated_tickets,
            unread_tickets=self.get_unread_tickets,
            pending_tickets=self.get_pending_tickets,
            closed_tickets=self.get_closed_tickets,
            )

        self.context = self.request.matchdict['context']
        self._view = self.context
        self.dispatch()

    def serialize_ticket_current_status_for_calendar(self, cstatus):
        url = self.request.route_url('msl_tickets',
                                     context='viewticket',
                                     id=cstatus.ticket_id)
        status = cstatus.status
        title = cstatus.ticket.title
        data = dict(id=cstatus.ticket_id,
                    #start=cstatus.last_change.isoformat(),
                    start=cstatus.ticket.created.isoformat(),
                    end=cstatus.last_change.isoformat(),
                    title=title,
                    url=url)
        if status == 'pending':
            data['color'] = 'blue'
        return data

    def _get_start_end_userid(self):
        start = self.request.GET['start']
        end = self.request.GET['end']
        user_id = self.request.session['user'].id
        return start, end, user_id
    
    def get_assigned_tickets(self):
        start, end, user_id = self._get_start_end_userid()
        serialize = self.serialize_ticket_current_status_for_calendar
        tickets = self.tickets.get_assigned(user_id, start=start, end=end,
                                            timestamps=True)
        tlist = []
        for cstatus in tickets:
            tdata = serialize(cstatus)
            tlist.append(tdata)
        self.response = tlist
        
    def get_delegated_tickets(self):
        start, end, user_id = self._get_start_end_userid()
        serialize = self.serialize_ticket_current_status_for_calendar
        tickets = self.tickets.get_delegated(user_id, start=start, end=end,
                                            timestamps=True)
        tlist = []
        for cstatus in tickets:
            tdata = serialize(cstatus)
            tlist.append(tdata)
        self.response = tlist
        
    def get_unread_tickets(self):
        start, end, user_id = self._get_start_end_userid()
        serialize = self.serialize_ticket_current_status_for_calendar
        tickets = self.tickets.get_unread(user_id, start=start, end=end,
                                            timestamps=True)
        tlist = []
        for cstatus in tickets:
            tdata = serialize(cstatus)
            tlist.append(tdata)
        self.response = tlist

    def get_pending_tickets(self):
        start, end, user_id = self._get_start_end_userid()
        serialize = self.serialize_ticket_current_status_for_calendar
        tickets = self.tickets.get_pending(user_id, start=start, end=end,
                                            timestamps=True)
        tlist = []
        for cstatus in tickets:
            tdata = serialize(cstatus)
            tlist.append(tdata)
        self.response = tlist

    def get_closed_tickets(self):
        start, end, user_id = self._get_start_end_userid()
        serialize = self.serialize_ticket_current_status_for_calendar
        tickets = self.tickets.get_closed(user_id, start=start, end=end,
                                            timestamps=True)
        tlist = []
        for cstatus in tickets:
            tdata = serialize(cstatus)
            tlist.append(tdata)
        self.response = tlist

class TicketJSONViewer(BaseJSONViewer):
    def __init__(self, request):
        super(TicketJSONViewer, self).__init__(request)
        
class BaseTicketViewer(BaseViewer):
    def __init__(self, request):
        super(BaseTicketViewer, self).__init__(request)
        prepare_main_layout(self.request)
        self.tickets = TicketManager(self.request.db)
        
        self.dtformat = '%A - %B %d %H:%m'
        
        self._dispatch_table = dict(
            main=self.main_tickets_view,
            add=self.open_ticket,
            viewticket=self.view_ticket,
            updateticket=self.update_ticket,)
        self.context = self.request.matchdict['context']
        self._view = self.context

        #user_id = self.request.session['user'].id
        #url = self.url(context='takencalls', id=user_id)
        #label = "Calls I've taken"
        #self.layout.ctx_menu.append_new_entry(label, url)

        self.dispatch()
        #import pdb ; pdb.set_trace()
        
    def _make_text_message(self, ticket):
        settings = self.request.registry.settings
        url = self.url(context='viewticket', id=ticket.id)
        path = urlparse.urlparse(url).path
        url = settings['mslemon.public_url'] + path 
        text = "%s\n\n" % url
        return text
    
    def _send_text_notification(self, ticket):
        #callee = self.request.db.query(User).get(pcall.callee)
        settings = self.request.registry.settings
        cfg = ticket.current_status.handler.config.get_config()
        if cfg.get('main', 'sms_email_address'):
            prefix = 'mslemon.smtp.'
            server = settings[prefix + 'server']
            port = int(settings[prefix + 'port'])
            login = settings[prefix + 'login']
            password = settings[prefix + 'password']
            cstatus = ticket.current_status
            subject = "%s created a new ticket" % cstatus.changed_by.username
            message = self._make_text_message(ticket)
            sender = login
            receiver = cfg.get('main', 'sms_email_address')
            msg = make_email_message(subject, message, sender, receiver)
            send_email_through_smtp_server(settings, msg, sender, receiver)
    
    
    def main_tickets_view(self):
        template = 'mslemon:templates/consult/main-ticket-view.mako'
        default_view = 'agendaDay'
        tkt_types = ['assigned', 'delegated', 'unread',
                     'pending', 'closed']
        calendar_urls = {}
        list_urls = {}
        t = 'tickets'
        for tkt_type in tkt_types:
            route = 'msl_tktjson'
            context = '%s_tickets' % tkt_type
            url = self.request.route_url(route, context=context, id=t)
            calendar_urls[tkt_type] = url
            route = 'msl_tktfrag'
            context = tkt_type
            url = self.request.route_url(route, context=context, id=t)
            list_urls[tkt_type] = url
        user = self.get_current_user()
        cfg = user.config.get_config()
        try:
            calviews = dict(cfg.items('ticket_views'))
        except NoSectionError:
            calviews = dict(((k, 'month') for k in tkt_types))
            cfg.add_section('ticket_views')
            for k in calviews:
                cfg.set('ticket_views', k, calviews[k])
        env = dict(calendar_urls=calendar_urls,
                   list_urls=list_urls,
                   calviews=calviews)
        content = self.render(template, env)
        self.layout.content = content
        #self.layout.resources.phone_calendar.need()
        self.layout.resources.main_ticket_view.need()
        self.layout.resources.cornsilk.need()
        #self.layout.resources.azure3.need()

    def _open_ticket_form_submitted(self, form):
        controls = self.request.POST.items()
        self.layout.subheader = "New ticket submitted to database"
        try:
            data = form.validate(controls)
        except deform.ValidationFailure, e:
            self.layout.content = e.render()
            return
        handler_id = data['handler']
        user_id = self.request.session['user'].id
        title = data['title']
        description = data['description']

        ticket = self.tickets.open(user_id, title,
                                   description, handler_id=handler_id)
        if data['send_textmsg']:
            self._send_text_notification(ticket)

    def _update_ticket_form_submitted(self, form):
        controls = self.request.POST.items()
        self.layout.subheader = "Ticket update submitted to database"
        try:
            data = form.validate(controls)
        except deform.ValidationFailure, e:
            self.layout.content = e.render()
            return
        ticket_id = int(self.request.matchdict['id'])
        user_id = self.request.session['user'].id
        reason = data['reason']
        handler_id = int(data['handler'])
        sdict = dict(enumerate(['pending', 'closed']))
        status = sdict[data['status']]
        change = self.tickets.update_ticket(ticket_id, user_id,
                                            status, reason, handler_id)
        
        content = '<p>Ticket updated. %d</p>' % change.id
        self.layout.content = content
        
    
        
    def open_ticket(self):
        schema = NewTicketSchema()
        users = self.request.db.query(User).all()
        skey = 'mslemon.admin.admin_username'
        admin_username = self.request.registry.settings.get(skey, 'admin')
        choices = [(u.id, u.username) \
                       for u in users if u.username != admin_username]
        schema['handler'].widget = make_select_widget(choices)
        form = deform.Form(schema, buttons=('submit',))
        self.layout.resources.deform_auto_need(form)
        self.layout.resources.azure3.need()
        if 'submit' in self.request.POST:
            self._open_ticket_form_submitted(form)
        else:
            formdata = dict(received=datetime.now())
            rendered = form.render(formdata)
            self.layout.content = rendered
        
    def view_ticket(self):
        id = int(self.request.matchdict['id'])
        ticket = self.tickets.query().get(id)
        template = 'mslemon:templates/consult/msl-view-ticket.mako'
        rst = render_rst
        env = dict(ticket=ticket, rst=rst)
        content = self.render(template, env)
        self.layout.content = content
        
    def update_ticket(self):
        ticket_id = int(self.request.matchdict['id'])
        schema = UpdateTicketSchema()
        choices = enumerate(['pending', 'closed'])
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
            self._update_ticket_form_submitted(form)
        else:
            ticket = self.tickets.query().get(ticket_id)
            dstatus = dict(enumerate(['pending', 'closed']))
            revstat = dict([(v,k) for k,v in dstatus.items()])
            # here we force ticket with 'opened' status
            # to default to 'pending' on the form, but
            # can be closed to.  The goal is to record
            # acknowledgement, and allow for delegation
            # before closure.
            if ticket.current_status.status != 'opened':
                cstatus = revstat[ticket.current_status.status]
            else:
                cstatus = revstat['pending']
            formdata = dict(status=cstatus,
                            handler=ticket.current_status.handler_id)
            self.layout.content = form.render(formdata)
            self.layout.subheader = 'Update status of ticket'
        
        
#######################################################        
#######################################################        
#######################################################        
# phone calls
#######################################################        
#######################################################        
#######################################################        
#######################################################        


class PhoneCallFrag(BaseViewer):
    def __init__(self, request):
        super(PhoneCallFrag, self).__init__(request)
        self._template = 'mslemon:templates/consult/msl-list-phonecalls.mako'
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
        start = pcall.received.isoformat()
        end = cstatus.last_change.isoformat()
        title = pcall.caller
        data = dict(id=pcall.id, start=start, end=end,
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

        #user_id = self.request.session['user'].id
        #url = self.url(context='takencalls', id=user_id)
        #label = "Calls I've taken"
        #self.layout.ctx_menu.append_new_entry(label, url)

        self.dispatch()
        #import pdb ; pdb.set_trace()

    def main_phonecall_view(self):
        template = 'mslemon:templates/consult/msl-main-phone-view.mako'
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
        #self.layout.resources.phone_calendar.need()
        self.layout.resources.main_phone_view.need()
        self.layout.resources.cornsilk.need()


    def _make_text_message(self, pcall):
        settings = self.request.registry.settings
        url = self.url(context='viewcall', id=pcall.id)
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
        fields = ['received', 'caller', 'number', 'text', 'callee']
        fields = ['received', 'caller', 'number', 'callee']
        values1 = [data[f] for f in fields]
        values2 = [data[f] for f in ['subject', 'text']]
        received_by = self.request.session['user'].id
        values = values1 + [received_by] + values2
        pcall = self.pcm.new_call(*values)
        if data['send_textmsg']:
            self._send_text_notification(pcall)
                

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
        template = 'mslemon:templates/consult/msl-view-phonecall.mako'
        rst = render_rst
        db = self.request.db
        pcm = self.pcm
        env = dict(pcall=pcall, rst=rst, db=db, User=User, pcm=pcm)
        content = self.render(template, env)
        self.layout.content = content

    def update_phonecall(self):
        pass

    
    

        
                          
        
        
MSLViewer = BaseTicketViewer

