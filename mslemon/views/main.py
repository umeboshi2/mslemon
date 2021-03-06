from datetime import datetime, date, timedelta

from docutils.core import publish_parts

from sqlalchemy.exc import OperationalError, ProgrammingError
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.security import authenticated_userid
from pyramid.renderers import render
from pyramid.response import Response

import colander
import deform

from mslemon.managers.tickets import TicketManager
from mslemon.managers.phonecalls import PhoneCallManager
from mslemon.managers.cases import CaseManager
from mslemon.managers.events import EventManager
from mslemon.managers.documents import DocumentManager
from mslemon.managers.documents import ScannedDocumentsManager


from trumpet.views.menus import BaseMenu

from mslemon.models.usergroup import User

from mslemon.views.base import BaseViewer
from mslemon.views.base import make_main_menu

class MainCalJSONViewer(BaseViewer):
    def __init__(self, request):
        super(MainCalJSONViewer, self).__init__(request)
        self.events = EventManager(self.request.db)
        self.tickets = TicketManager(self.request.db)
        self.phonecalls = PhoneCallManager(self.request.db)
        self.cases = CaseManager(self.request.db)
        self.docs = DocumentManager(self.request.db)
        self.scandocs = ScannedDocumentsManager(self.request.db)

        self.get_everthing()

    def _get_start_end_userid(self, user_id=True):
        start = self.request.GET['start']
        end = self.request.GET['end']
        if user_id:
            user_id = self.request.session['user'].id
        return start, end, user_id
        
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

    def serialize_scandoc_for_calendar(self, sdoc):
        url = self.request.route_url('msl_scandocs',
                                     context='view',
                                     id=sdoc.created.isoformat())
        start = sdoc.created
        end = start + timedelta(minutes=60)
        data = dict(id=start.isoformat(),
                    start=start.isoformat(),
                    end=end.isoformat(),
                    title='PDF',
                    url=url)
        return data

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
    


    def get_tickets(self):
        start, end, user_id = self._get_start_end_userid()
        serialize = self.serialize_ticket_current_status_for_calendar
        clist = set()
        for ctype in ['assigned', 'pending', 'unread', 'delegated']:
            method = getattr(self.tickets, 'get_%s' % ctype)
            clist = clist.union(
                set(method(user_id, start, end, timestamps=True)))
        return [serialize(cstatus) for cstatus in list(clist)]
        
    def get_calls(self):
        start, end, user_id = self._get_start_end_userid()
        serialize = self.serialize_phonecall_for_calendar
        #context = self.request.matchdict['context']
        clist = set()
        for ctype in ['received', 'taken',
                      'assigned', 'pending', 'unread', 'delegated']:
            method = getattr(self.phonecalls, 'get_%s_calls' % ctype)
            clist = clist.union(
                set(method(user_id, start, end, timestamps=True)))
        return [serialize(pc, cstatus) for pc, cstatus in list(clist)]
        
    def get_cases(self):
        start, end, user_id = self._get_start_end_userid()
        serialize = self.serialize_case_for_calendar
        clist = self.cases.get_accessible(user_id, start, end, timestamps=True)

        return [serialize(cstatus) for cstatus in clist]

    def get_documents(self):
        start, end, user_id = self._get_start_end_userid()
        sdocs = self.scandocs.get_documents(start, end, timestamps=True)
        serialize = self.serialize_scandoc_for_calendar
        return [serialize(doc) for doc in sdocs]

    def get_events(self):
        start, end, user_id = self._get_start_end_userid()
        events = self.events.get_events(user_id, start, end, timestamps=True)
        return [self.serialize_event(e) for e in events]
    
    def get_everthing(self):
        tickets = self.get_tickets()
        phonecalls = self.get_calls()
        cases = self.get_cases()
        sdocs = self.get_documents()
        events = self.get_events()
        
        for t in tickets:
            t['color'] = 'green'
        for p in phonecalls:
            p['color'] = 'yellow'
            p['textColor'] = 'black'
        for c in cases:
            c['color'] = 'purple'
        for d in sdocs:
            d['color'] = '#8B7355'
        for e in events:
            e['color'] = 'RoyalBlue'
            
        self.response = tickets + phonecalls + cases + sdocs + events
        
    
class MainViewer(BaseViewer):
    def __init__(self, request):
        super(MainViewer, self).__init__(request)
        self.route = self.request.matched_route.name
        self.layout.main_menu = make_main_menu(self.request)
        self._user_query = self.request.db.query(User)

        # begin dispatch
        if self.route == 'home':
            self.main_view()
            return
        elif self.route == 'initdb':
            self.initialize_database()
            return
        if self.route == 'main':
            self.context = self.request.matchdict['context']
        

        # make dispatch table
        self._cntxt_meth = dict(
            main=self.main_view,
            viewevent=self.view_event,
            viewvenue=self.view_venue,
            viewdayevents=self.view_events_for_day,
            exportevent=self.export_event,
            )

        if self.context in self._cntxt_meth:
            self._cntxt_meth[self.context]()
        else:
            msg = 'Undefined Context: %s' % self.context
            self.layout.content = '<b>%s</b>' % msg

            
    def authenticated_view(self):
        #template = 'goout:templates/main-page.mako'
        #env = dict(dates=dates, dc=dc, dformat=dformat)
        #content = render(template, env, request=self.request)
        content = "Main Page"
        self.layout.content = content
        self.layout.subheader = 'Ms. Lemon'
        #self.layout.resources.maincalendar.need()
        self.layout.resources.main_calendar_view.need()
        #self.layout.resources.cornsilk.need()
        
        template = 'mslemon:templates/mainview-calendar.mako'
        env = {}
        content = self.render(template, env)
        self.layout.content = content
        
        
    def main_view(self):
        authn_policy = self.request.context.authn_policy
        authn = authn_policy.authenticated_userid(self.request)
        if authn is None:
            self.unauthenticated_view()
        else:
            self.authenticated_view()
            
    def unauthenticated_view(self):
        dbconn = False
        try:
            self._user_query.first()
            dbconn = True
        except OperationalError:
            dbconn = False
        except ProgrammingError:
            dbconn = False
        if not dbconn:
            mkurl = self.request.route_url
            url = mkurl('initdb', context='initialize', id='database')
            msg = "Create Database"
            anchor = '<a class="action-button" href="%s">%s</a>' % (url, msg)
            content = anchor
        else:
            url = self.request.route_url('login')
            content = '<a href="%s">Login</a>' % url
        self.layout.content = content

    def initialize_database(self):
        context = self.request.matchdict['context']
        if context != 'initialize':
            self.layout.content = "Bad Call"
            return
        id = self.request.matchdict['id']
        if id != 'database':
            self.layout.content = "Bad Call"
            return
        from mslemon.models.initialize import initialize_database
        settings = self.get_app_settings()
        initialize_database(settings)
        self.layout.content = "Database Initialized"
    
    
    def view_event(self):
        pass
    
        
    def export_event(self):
        pass
    
        
    
    def view_venue(self):
        pass

    def view_events_for_day(self):
        pass
    


        


class TraversalViewer(BaseViewer):
    def __init__(self, request):
        super(TraversalViewer, self).__init__(request)
        self.route = self.request.matched_route.name
        #self.layout.ctx_menu = make_ctx_menu(self.request).output()
        self._user_query = self.request.db.query(User)
        context = self.request.context
        self.layout.content = str(context)
            
            
