from datetime import datetime, timedelta

import colander
import deform

from mslemon.views.base import prepare_layout
from mslemon.views.base import BaseViewer


from mslemon.managers.clients import ClientManager
from mslemon.managers.contacts import ContactManager
from mslemon.managers.events import EventManager

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
    start = colander.SchemaNode(
        colander.DateTime(),
        title='Start Date/Time',
        widget=deform.widget.DateTimeInputWidget()
        )
    end = colander.SchemaNode(
        colander.DateTime(),
        title='End Date/Time',
        widget=deform.widget.DateTimeInputWidget()
        )
    all_day = colander.SchemaNode(
        colander.Boolean(),
        title='All Day',
        widget=deform.widget.CheckboxWidget(),
        )

    
class CalendarJSONViewer(BaseViewer):
    def __init__(self, request):
        super(CalendarJSONViewer, self).__init__(request)
        self.events = EventManager(self.request.db)

        self.render_events()


    def _get_start_end_userid(self):
        start = self.request.GET['start']
        end = self.request.GET['end']
        user_id = self.request.session['user'].id
        return start, end, user_id

    def serialize_event(self, event):
        url = self.request.route_url('consult_calendar',
                                     context='view',
                                     id=event.id)
        start = event.start
        end = event.end
        thirty_minutes = timedelta(minutes=30)
        if end - start < thirty_minutes:
            end = start + thirty_minutes
        title = event.title
        id = event.id
        data = dict(id=str(id), title=title,
                    start=start.isoformat(),
                    end=end.isoformat(), url=url)
        return data
    

    def render_events(self):
        start, end, user_id = self._get_start_end_userid()
        serialize = self.serialize_event
        context = self.request.matchdict['context']
        events = self.events.get_events(user_id, start, end, timestamps=True)
        self.response = [serialize(e) for e in events]
        


def prepare_main_layout(request):
    prepare_base_layout(request)
    layout = request.layout_manager.layout
    layout.title = 'Calendar'
    layout.header = 'Calendar'
    layout.subheader = 'Calendar Area'
    

    

class CalendarViewer(BaseViewer):
    def __init__(self, request):
        BaseViewer.__init__(self, request)
        prepare_main_layout(self.request)
        self.clients = ClientManager(self.request.db)
        self.contacts = ContactManager(self.request.db)
        self.events = EventManager(self.request.db)
        self._dispatch_table = dict(
            list=self.list_events,
            add=self.add_event,
            delete=self.delete_event,
            confirmdelete=self.confirm_delete_event,
            view=self.view_event,
            export=self.export_event)
        self.context = self.request.matchdict['context']
        self._view = self.context

        self.dispatch()

    def list_events(self):
        # setup widgetbox
        template = 'mslemon:templates/msl/draggable-event-widget.mako'
        env = dict()
        self.layout.widgetbox = self.render(template, env)
        
        template = 'mslemon:templates/consult/calendar-main.mako'
        env = dict()
        self.layout.content = self.render(template, env)
        self.layout.resources.planevent_calendar_view.need()
        self.layout.resources.azure3.need()
        #self.layout.resources.cornsilk.need()

    def _add_event_form_submitted(self, form):
        controls = self.request.POST.items()
        self.layout.subheader = "add event form submitted"
        try:
            data = form.validate(controls)
        except deform.ValidationFailure, e:
            self.layout.content = e.render()
            return
        user_id = self.get_current_user_id()
        if data['description'] is colander.null:
            data['description'] = ''
        title = data['title']
        start = data['start']
        end = data['end']
        description = data['description']
        all_day = data['all_day']
        self.events.add_event(title, start, end, description, all_day, user_id)
        self.layout.content = 'Event Created!'
        
    def add_event(self):
        schema = AddEventSchema()
        form = deform.Form(schema, buttons=('submit',))
        self.layout.resources.deform_auto_need(form)
        self.layout.resources.azure3.need()
        if 'submit' in self.request.POST:
            self._add_event_form_submitted(form)
        else:
            formdata = dict()
            formdata.update(self.request.POST)
            dtformat = '%Y-%m-%d %H:%M:%S'
            start = None
            if 'start' in formdata:
                start = datetime.strptime(formdata['start'], dtformat)
                formdata['start'] = start
            if 'end' in formdata:
                # sometimes end is null
                try:
                    end = datetime.strptime(formdata['end'], dtformat)
                    formdata['end'] = end
                except ValueError:
                    formdata['end'] = start + timedelta(hours=1)
            all_day = self.request.POST['allDay']
            if all_day == 'false':
                formdata['all_day'] = False
            else:
                formdata['all_day'] = True
            self.layout.footer = all_day
            rendered = form.render(formdata)
            self.layout.content = rendered
            self.layout.subheader = 'Add an Event'
            
        
            
    def view_event(self):
        id = int(self.request.matchdict['id'])
        event = self.events.get(id)
        template = 'mslemon:templates/msl/view-calendar-event.mako'
        env = dict(event=event)
        rendered = self.render(template, env)
        self.layout.content = rendered
        

    def export_event(self):
        id = int(self.request.matchdict['id'])
        ical = self.events.export_ical(id)
        r = Response(content_type='text/calendar',
                     body=ical.serialize())
        filename = 'event-%04d.ics' % id
        r.content_disposition = 'attachment; filename="%s"' % filename
        self.response = r
        
    

    def delete_event(self):
        pass

    def confirm_delete_event(self):
        pass
    
