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
    layout.title = 'Consultant Tickets'
    layout.header = 'Consultant Tickets'
    layout.subheader = 'Tickets Area'
    

    

class TicketViewer(BaseViewer):
    def __init__(self, request):
        BaseViewer.__init__(self, request)
        prepare_main_layout(self.request)
        self.tickets = TicketManager(self.request.db)
        self.clients = ClientManager(self.request.db)
        self._dispatch_table = dict(
            list=self.list_tickets,
            add=self.add_ticket,
            viewticket=self.view_ticket,
            updateticket=self.update_ticket,
            ticketcal=self.ticket_calendar)
        self.context = self.request.matchdict['context']
        self._view = self.context

        url = self.url(context='add', id='somebody')
        self.layout.ctx_menu.append_new_entry("Add Ticket", url)

        url = self.url(context='ticketcal', id='today')
        self.layout.ctx_menu.append_new_entry("Ticket Calendar", url)
        
        self.dispatch()

    def list_tickets(self):
        tickets = self.tickets.all()
        env = dict(tickets=tickets, tm=self.tickets)
        template = 'mslemon:templates/consult/listtickets.mako'
        self.layout.content = self.render(template, env)
        

    def add_ticket(self):
        schema = OpenTicketSchema()
        clist = self.clients.all()
        choices = [(c.id, c.name) for c in  clist]
        schema['client'].widget = make_select_widget(choices)
        form = deform.Form(schema, buttons=('submit',))
        self.layout.resources.deform_auto_need(form)
        if 'submit' in self.request.POST:
            controls = self.request.POST.items()
            self.layout.subheader = 'Ticket Submitted'
            try:
                data = form.validate(controls)
            except deform.ValidationFailure, e:
                self.layout.content = e.render()
                return
            user_id = self.request.session['user'].id
            title = data['title']
            client_id = int(data['client'])
            description = data['description']
            c = self.tickets.open(user_id, client_id, title, description)
            content = '<p>Ticket %s added.</p>' % c.title
            self.layout.content = content
            return
        rendered = form.render()
        self.layout.content = rendered
        self.layout.subheader = 'Add a Ticket'
            
                           
    def view_ticket(self):
        template = 'mslemon:templates/consult/viewticket.mako'
        id = int(self.request.matchdict['id'])
        ticket = self.tickets.query().get(id)
        env = dict(ticket=ticket, tm=self.tickets, rst=render_rst)
        self.layout.content = self.render(template, env)

    def update_ticket(self):
        ticket_id = int(self.request.matchdict['id'])
        schema = UpdateTicketSchema()
        clist = self.tickets.stypes.all()
        choices = [(c.id, c.name) for c in  clist]
        schema['status'].widget = make_select_widget(choices)
        form = deform.Form(schema, buttons=('submit',))
        self.layout.resources.deform_auto_need(form)
        if 'submit' in self.request.POST:
            controls = self.request.POST.items()
            self.layout.subheader = 'Ticket Update Submitted'
            try:
                data = form.validate(controls)
            except deform.ValidationFailure, e:
                self.layout.content = e.render()
                return
            user_id = self.request.session['user'].id
            reason = data['reason']
            status_id = int(data['status'])
            status = self.tickets.update_ticket(ticket_id,
                                                user_id, status_id, reason)
            content = '<p>Ticket updated.</p>' 
            self.layout.content = content
            return
        rendered = form.render()
        self.layout.content = rendered
        self.layout.subheader = 'Add a Ticket'

    def ticket_calendar(self):
        template = 'mslemon:templates/consult/calendar-main.mako'
        env = dict()
        self.layout.content = self.render(template, env)
        from haberdashery.resources import ticket_calendar
        ticket_calendar.need()
        self.layout.resources.azure3.need()
        #self.layout.resources.cornsilk.need()
        
        
        
