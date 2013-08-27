import urlparse
from datetime import datetime, timedelta
from ConfigParser import NoSectionError, DuplicateSectionError

from pyramid.httpexceptions import HTTPFound

import colander
import deform

from mslemon.views.base import prepare_layout
from mslemon.views.base import BaseViewer
from trumpet.views.base import render_rst


from mslemon.managers.cases import CaseManager
from mslemon.managers.clients import ClientManager

from mslemon.views.consultant.base import prepare_base_layout

from mslemon.models.usergroup import User

from mslemon.util import send_email_through_smtp_server, make_email_message
from mslemon.util import get_regular_users



def deferred_choices(node, kw):
    choices = kw['choices']
    return deform.widget.SelectWidget(values=choices)

def make_select_widget(choices):
    return deform.widget.SelectWidget(values=choices)

class NewCaseSchema(colander.Schema):
    handler = colander.SchemaNode(
        colander.Integer(),
        title='Handler',
        widget=deferred_choices,
        description='This is the user that will handle this case',
        )
    client = colander.SchemaNode(
        colander.Integer(),
        title='Client',
        widget=deferred_choices,
        description='This is the client that this case is for',
        )
    name = colander.SchemaNode(
        colander.String(),
        title='Name',
        description='This is a short title or style for the case',
        )
    description = colander.SchemaNode(
        colander.String(),
        title='Description',
        widget=deform.widget.TextAreaWidget(rows=10, cols=60),
        missing=colander.null,
        description='This is a description of the case',
        )

reason_description = """\
You can instruct another user to handle the case by
 changing the handler of this case and typing the instructions
 in this area.
"""

class UpdateCaseSchema(colander.Schema):
    status = colander.SchemaNode(
        colander.Integer(),
        title='New Status',
        widget=deferred_choices,
        )
    handler = colander.SchemaNode(
        colander.Integer(),
        title='Handler',
        widget=deferred_choices,
        description='This is the user that will handle this case',
        )
    reason = colander.SchemaNode(
        colander.String(),
        title='Reason',
        description=reason_description,
        widget=deform.widget.TextAreaWidget(rows=10, cols=60),
        )
    
class AddUserToCaseSchema(colander.Schema):
    user = colander.SchemaNode(
        colander.Integer(),
        title="User",
        widget=deferred_choices,
        description="User to add to case",
        )
    
    
def prepare_main_layout(request):
    prepare_base_layout(request)
    layout = request.layout_manager.layout
    layout.title = 'MSL Cases'
    layout.header = 'MSL Cases'
    layout.subheader = 'MSL Case Management Area'



class CaseFrag(BaseViewer):
    def __init__(self, request):
        super(CaseFrag, self).__init__(request)
        self._template = 'mslemon:templates/consult/msl-list-cases.mako'
        self.cases = CaseManager(self.request.db)
        self.dtformat = '%A - %B %d %H:%m'
        self.env = dict(dtformat=self.dtformat)
        self.render_case_list()
        
    def _getuserid(self):
        return self.request.session['user'].id

    def _render_cases(self, case_type):
        user_id = self._getuserid()
        method = getattr(self.cases, 'get_%s' % case_type)
        clist = method(user_id)
        env = self.env.update(clist=clist)
        self.response = self.render(self._template, self.env)
        
    def render_case_list(self):
        context = self.request.matchdict['context']
        self._render_cases(context)
        
class CaseJSONViewer(BaseViewer):
    def __init__(self, request):
        super(CaseJSONViewer, self).__init__(request)
        self.cases = CaseManager(self.request.db)
        self.render_cases()

    def serialize_case_for_calendar(self, cstatus):
        case = cstatus.case
        url = self.request.route_url('msl_cases',
                                     context='view',
                                     id=case.id)
        start = case.created
        end = cstatus.last_change
        thirty_minutes = timedelta(minutes=30)
        if end - start < thirty_minutes:
            end = start + thirty_minutes
            
        title = cstatus.case.name
        data = dict(id=case.id, start=start.isoformat(),
                    end=end.isoformat(),
                    title=title, url=url)
        if cstatus.status == 'pending':
            data['color'] = 'blue'
        return data

    def _get_start_end_userid(self):
        start = self.request.GET['start']
        end = self.request.GET['end']
        user_id = self.request.session['user'].id
        return start, end, user_id

    def render_cases(self):
        start, end, user_id = self._get_start_end_userid()
        serialize = self.serialize_case_for_calendar
        context = self.request.matchdict['context']
        method = getattr(self.cases, 'get_%s' % context)
        clist = method(user_id, start, end, timestamps=True)
        #import pdb ; pdb.set_trace()
        self.response = [serialize(cstatus) for cstatus in clist]
        
class MainCaseViewer(BaseViewer):
    def __init__(self, request):
        super(MainCaseViewer, self).__init__(request)
        prepare_main_layout(self.request)
        
        self.cases = CaseManager(self.request.db)
        self.clients = ClientManager(self.request.db)
        
        self.dtformat = '%A - %B %d %H:%m'
        
        self._dispatch_table = dict(
            main=self.main_view,
            add=self.open_case,
            view=self.view_case,
            update=self.update_case,
            manageusers=self.manage_users,
            detachuser=self.detach_user,)
        self.context = self.request.matchdict['context']
        self._view = self.context

        url = self.url(context='add', id='something')
        self.layout.ctx_menu.append_new_entry('New Case', url)
        
        self.dispatch()
        
    def _make_text_message(self, ticket):
        settings = self.request.registry.settings
        url = self.url(context='view', id=ticket.id)
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
    
    
    def main_view(self):
        template = 'mslemon:templates/consult/msl-main-cases-view.mako'
        default_view = 'month'
        case_types = ['accessible', 'assigned', 'delegated', 'unread',
                      'pending', 'closed']
        calendar_urls = {}
        list_urls = {}
        c = 'cases'
        for case_type in case_types:
            route = 'msl_casesjson'
            context = '%s' % case_type
            url = self.request.route_url(route, context=context, id=c)
            calendar_urls[case_type] = url
            route = 'msl_casesfrag'
            context = case_type
            url = self.request.route_url(route, context=context, id=c)
            list_urls[case_type] = url
        user = self.get_current_user()
        cfg = user.config.get_config()
        cfgsection = 'case_views'
        try:
            calviews = dict(cfg.items(cfgsection))
        except NoSectionError:
            calviews = dict(((k, default_view) for k in case_types))
            cfg.add_section(cfgsection)
            for k in calviews:
                cfg.set(cfgsection, k, calviews[k])
        env = dict(calendar_urls=calendar_urls,
                   list_urls=list_urls,
                   calviews=calviews,
                   casetypes=case_types)
        content = self.render(template, env)
        self.layout.content = content
        self.layout.resources.main_cases_view.need()
        self.layout.resources.cornsilk.need()

    def _open_case_form_submitted(self, form):
        controls = self.request.POST.items()
        self.layout.subheader = "New case submitted to database"
        try:
            data = form.validate(controls)
        except deform.ValidationFailure, e:
            self.layout.content = e.render()
            return
        handler_id = data['handler']
        user_id = self.request.session['user'].id
        client_id = data['client']
        name = data['name']
        description = data['description']
        case = self.cases.open_case(name, description, client_id,
                                    user_id, handler_id=handler_id)
        self.response = HTTPFound(self.url(context='view', id=case.id))

    def _update_case_form_submitted(self, form):
        controls = self.request.POST.items()
        self.layout.subheader = "Ticket update submitted to database"
        try:
            data = form.validate(controls)
        except deform.ValidationFailure, e:
            self.layout.content = e.render()
            return
        case_id = int(self.request.matchdict['id'])
        user_id = self.request.session['user'].id
        reason = data['reason']
        handler_id = int(data['handler'])
        sdict = dict(enumerate(['pending', 'closed']))
        status = sdict[data['status']]
        change = self.cases.update_case(case_id, user_id,
                                            status, reason, handler_id)
        content = '<p>Case updated. %d</p>' % change.id
        self.layout.content = content
        self.response = HTTPFound(self.url(context='view', id=case_id))
        
    
        
    def open_case(self):
        schema = NewCaseSchema()
        users = get_regular_users(self.request)
        choices = [(u.id, u.username) for u in users]
        schema['handler'].widget = make_select_widget(choices)
        choices = [(c.id, c.name) for c in self.clients.all()]
        schema['client'].widget = make_select_widget(choices)
        form = deform.Form(schema, buttons=('submit',))
        self.layout.resources.deform_auto_need(form)
        if 'submit' in self.request.POST:
            self._open_case_form_submitted(form)
        else:
            formdata = dict(handler=self.request.session['user'].id)
            rendered = form.render(formdata)
            self.layout.content = rendered

    def _check_authorized(self, case):
        user_id = self.request.session['user'].id
        case_user_ids = [u.user_id for u in case.users]
        return user_id in case_user_ids
    
    def view_case(self):
        id = int(self.request.matchdict['id'])
        case = self.cases.query().get(id)
        if self._check_authorized(case):
            template = 'mslemon:templates/consult/msl-view-case.mako'
            rst = render_rst
            env = dict(case=case, rst=rst)
            content = self.render(template, env)
            self.layout.content = content
        else:
            self.layout.content = "Unavailable"
            
    def update_case(self):
        case_id = int(self.request.matchdict['id'])
        case = self.cases.query().get(case_id)
        if not self._check_authorized(case):
            self.layout.content = 'unavailable'
            return
        schema = UpdateCaseSchema()
        choices = enumerate(['pending', 'closed'])
        schema['status'].widget = make_select_widget(choices)
        users = get_regular_users(self.request)
        choices = [(u.id, u.username) for u in users]
        schema['handler'].widget = make_select_widget(choices)
        form = deform.Form(schema, buttons=('submit',))
        self.layout.resources.deform_auto_need(form)
        if 'submit' in self.request.POST:
            self._update_case_form_submitted(form)
        else:
            case = self.cases.query().get(case_id)
            dstatus = dict(enumerate(['pending', 'closed']))
            revstat = dict([(v,k) for k,v in dstatus.items()])
            # here we force ticket with 'opened' status
            # to default to 'pending' on the form, but
            # can be closed to.  The goal is to record
            # acknowledgement, and allow for delegation
            # before closure.
            if case.current_status.status != 'opened':
                cstatus = revstat[case.current_status.status]
            else:
                cstatus = revstat['pending']
            formdata = dict(status=cstatus,
                            handler=case.current_status.handler_id)
            self.layout.content = form.render(formdata)
            self.layout.subheader = 'Update status of case'
        

        def attach_document_submitted(self):
            pass
        
        def attach_document(self):
            pass

    def manage_users(self):
        id = int(self.request.matchdict['id'])
        case = self.cases.get(id)
        if not self._check_authorized(case):
            self.layout.content = "unavailable"
            return
        users = case.users
        case_user_ids = [u.user_id for u in users]
        template = 'mslemon:templates/consult/msl-view-case-users.mako'
        rst = render_rst
        schema = AddUserToCaseSchema()
        all_users = get_regular_users(self.request)
        available = [u for u in all_users if u.id not in case_user_ids]
        choices = [(u.id, u.username) for u in available]
        schema['user'].widget = make_select_widget(choices)
        form = deform.Form(schema, buttons=('submit',))
        if 'submit' in self.request.POST:
            self._manage_users_form_submitted(form)
        else:
            formdata = dict()
            env = dict(users=users, form=form, rst=rst)
            content = self.render(template, env)
            self.layout.content = content
            
    def _manage_users_form_submitted(self, form):
        case_id = int(self.request.matchdict['id'])
        controls = self.request.POST.items()
        self.layout.subheader = "Case user submitted to database"
        try:
            data = form.validate(controls)
        except deform.ValidationFailure, e:
            self.layout.content = e.render()
            return
        user_id = data['user']
        self.cases.attach_user(case_id, user_id)
        self.response = HTTPFound(self.url(context='manageusers', id=case_id))
        
    def detach_user(self):
        case_id, user_id = self.request.matchdict['id'].split('_')
        case_id = int(case_id)
        user_id = int(user_id)
        case = self.cases.get(case_id)
        if not self._check_authorized(case):
            self.layout.content = "unavailable"
            return
        self.cases.detach_user(case_id, user_id)
        self.response = HTTPFound(self.url(context='manageusers', id=case_id))
        
        

