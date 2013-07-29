from datetime import datetime

import colander
import deform

from mslemon.views.base import prepare_layout
from mslemon.views.base import BaseViewer
from trumpet.views.base import render_rst

from mslemon.managers.consultant.tickets import TicketManager
from mslemon.managers.consultant.clients import ClientManager
from mslemon.managers.consultant.contacts import ContactManager

from mslemon.views.consultant.base import prepare_base_layout

from mslemon.models.usergroup import User
from mslemon.managers.consultant.phone import PhoneCallManager


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
    


def prepare_main_layout(request):
    prepare_base_layout(request)
    layout = request.layout_manager.layout
    layout.title = 'Phone Calls'
    layout.header = 'Phone Calls'
    layout.subheader = 'Telephone Area'


class PhoneCallViewer(BaseViewer):
    def __init__(self, request):
        super(PhoneCallViewer, self).__init__(request)
        prepare_main_layout(self.request)
        self.phonecalls = PhoneCallManager(self.request.db)
        
        self._dispatch_table = dict(
            list=self.phone_calendar,
            takencalls=self.list_taken_calls,
            add=self.take_call,
            viewcall=self.view_call,)
        self.context = self.request.matchdict['context']
        self._view = self.context

        user_id = self.request.session['user'].id
        url = self.url(context='takencalls', id=user_id)
        label = "Calls I've taken"
        self.layout.ctx_menu.append_new_entry(label, url)
        
        url = self.url(context='add', id='somebody')
        self.layout.ctx_menu.append_new_entry("Take Call", url)

        self.dispatch()

    def _take_call_form_submitted(self, form):
        controls = self.request.POST.items()
        self.layout.subheader = "Phone call all submitted to database"
        try:
            data = form.validate(controls)
        except deform.ValidationFailure, e:
            self.layout.content = e.render()
            return
        fields = ['caller', 'callee', 'text', 'received', 'number']
        fields = ['received', 'caller', 'number', 'text', 'callee']
        values = [data[f] for f in fields]
        received_by = self.request.session['user'].id
        values.append(received_by)
        pcall = self.phonecalls.new_call(*values)
        self.layout.subheader = "Phone Call taken: %s" % pcall
        
        
    
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
        self.layout.footer = 'take a phone call............'
        
    
    def list_calls(self):
        pass

    def list_taken_calls(self):
        user_id = self.request.session['user'].id
        calls = self.phonecalls.get_all_calls_for_user(user_id)
        content = 'User_id: %d-----<pre>%s</pre>' % (user_id, calls)
        env = dict(calls=calls)
        template = 'mslemon:templates/consult/listphonecalls.mako'
        content = self.render(template, env)
        self.layout.content = content
        

    def view_call(self):
        id = int(self.request.matchdict['id'])
        pcall = self.phonecalls.get(id)
        template = 'mslemon:templates/consult/viewphonecall.mako'
        rst = render_rst
        env = dict(pcall=pcall, rst=rst)
        content = self.render(template, env)
        self.layout.content = content
        
    
    def phone_calendar(self):
        template = 'mslemon:templates/consult/calendar-phone.mako'
        env = {}
        content = self.render(template, env)
        self.layout.content = content
        self.layout.resources.phone_calendar.need()
        self.layout.resources.cornsilk.need()
        
