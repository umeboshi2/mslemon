import colander
import deform

from mslemon.views.base import prepare_layout
from mslemon.views.base import BaseViewer


from mslemon.managers.consultant.clients import ClientManager
from mslemon.managers.consultant.contacts import ContactManager

from mslemon.views.consultant.base import prepare_base_layout


def deferred_choices(node, kw):
    choices = kw['choices']
    return deform.widget.SelectWidget(values=choices)

def make_select_widget(choices):
    return deform.widget.SelectWidget(values=choices)

class AddEventSchema(colander.Schema):
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

def prepare_main_layout(request):
    prepare_base_layout(request)
    layout = request.layout_manager.layout
    layout.title = 'Seneca'
    layout.header = 'Seneca'
    layout.subheader = 'Calendar Area'
    

    

class CalendarViewer(BaseViewer):
    def __init__(self, request):
        BaseViewer.__init__(self, request)
        prepare_main_layout(self.request)
        self.clients = ClientManager(self.request.db)
        self.contacts = ContactManager(self.request.db)
        self._dispatch_table = dict(
            list=self.list_events,
            add=self.add_event,
            delete=self.delete_event,
            confirmdelete=self.confirm_delete_event,)
        self.context = self.request.matchdict['context']
        self._view = self.context

        self.dispatch()

    def list_events(self):
        template = 'mslemon:templates/consult/calendar-main.mako'
        env = dict()
        self.layout.content = self.render(template, env)
        from haberdashery.resources import maincalendar
        maincalendar.need()
        self.layout.resources.azure3.need()
        #self.layout.resources.cornsilk.need()
        
    def add_event(self):
        schema = AddEventSchema()
        if 'submit' in self.request.POST:
            controls = self.request.POST.items()
            self.layout.subheader = 'Client Submitted'
            try:
                data = form.validate(controls)
            except deform.ValidationFailure, e:
                self.layout.content = e.render()
                return
            name = data['name']
            contact_id = int(data['contact'])
            address = data['address']
            description = data['description']
            c = self.clients.add(name, contact_id, address, description)
            content = '<p>Client %s added.</p>' % c.name
            self.layout.content = content
            return
        rendered = form.render()
        self.layout.content = rendered
        self.layout.subheader = 'Add an Event'
        
            
                           

    def delete_event(self):
        pass

    def confirm_delete_event(self):
        pass
    
