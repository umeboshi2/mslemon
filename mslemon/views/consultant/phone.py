import colander
import deform

from mslemon.views.base import prepare_layout
from mslemon.views.base import BaseViewer
from trumpet.views.base import render_rst

from mslemon.managers.consultant.tickets import TicketManager
from mslemon.managers.consultant.clients import ClientManager
from mslemon.managers.consultant.contacts import ContactManager

from mslemon.views.consultant.base import prepare_base_layout


def deferred_choices(node, kw):
    choices = kw['choices']
    return deform.widget.SelectWidget(values=choices)

def make_select_widget(choices):
    return deform.widget.SelectWidget(values=choices)


class TakePhoneCallSchema(colander.Schema):
    pass


class OpenTicketSchema(colander.Schema):
    title = colander.SchemaNode(
        colander.String(),
        title='Title',
        )
    client = colander.SchemaNode(
        colander.Integer(),
        title='Client',
        widget=deferred_choices,
        )
    description = colander.SchemaNode(
        colander.String(),
        title='Description',
        widget=deform.widget.TextAreaWidget(rows=10, cols=60),
        missing=colander.null,
        )

class UpdateTicketSchema(colander.Schema):
    status = colander.SchemaNode(
        colander.Integer(),
        title='New Status',
        widget=deferred_choices,
        )
    reason = colander.SchemaNode(
        colander.String(),
        title='Reason',
        widget=deform.widget.TextAreaWidget(rows=10, cols=60),
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
        
        self._dispatch_table = dict(
            list=self.list_calls,
            add=self.take_call,
            phonecal=self.phone_calendar,)
        self.context = self.request.matchdict['context']
        self._view = self.context

        url = self.url(context='add', id='somebody')
        self.layout.ctx_menu.append_new_entry("Take Call", url)

        url = self.url(context='phonecal', id='today')
        self.layout.ctx_menu.append_new_entry("Phone Calendar", url)
        
        self.dispatch()

    def take_call(self):
        self.layout.content = 'Take a phone call.'
    
    def list_calls(self):
        self.layout.content = 'List the calls here.'

    def phone_calendar(self):
        self.layout.content = '<div id="maincalendar"></div>'
        self.layout.resources.maincalendar.need()
        self.layout.resources.cornsilk.need()
        
