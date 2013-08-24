import urlparse
from datetime import datetime, timedelta
from ConfigParser import NoSectionError, DuplicateSectionError

from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response

import colander
import deform

from mslemon.views.base import prepare_layout
from mslemon.views.base import BaseViewer
from trumpet.views.base import render_rst

#FIXME: better module name
from mslemon.managers.consultant.misslemon import ScannedDocumentsManager

from mslemon.views.consultant.base import prepare_base_layout

from mslemon.models.usergroup import User

from mslemon.util import send_email_through_smtp_server, make_email_message



def deferred_choices(node, kw):
    choices = kw['choices']
    return deform.widget.SelectWidget(values=choices)

def make_select_widget(choices):
    return deform.widget.SelectWidget(values=choices)

        

def prepare_main_layout(request):
    prepare_base_layout(request)
    layout = request.layout_manager.layout
    layout.title = 'MSL'
    layout.header = 'MSL'
    layout.subheader = 'MSL Scanned Documents'




class ScannedDocumentsFrag(BaseViewer):
    def __init__(self, request):
        super(ScannedDocumentsFrag, self).__init__(request)
        self._template = 'mslemon:templates/consult/msl-list-phonecalls.mako'
        self.sdm = ScannedDocumentsManager(self.request.db)
        self.dtformat = '%A - %B %d %H:%m'
        self.env = dict(dtformat=self.dtformat)
        #self.render_call_list()
        
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
        
                                         
class ScannedDocumentsJSONViewer(BaseViewer):
    def __init__(self, request):
        super(ScannedDocumentsJSONViewer, self).__init__(request)
        self.sdm = ScannedDocumentsManager(self.request.db)
        self.render_docs()
        
    def serialize_scandoc_for_calendar(self, sdoc):
        url = self.request.route_url('msl_scandocs',
                                     context='export',
                                     id=sdoc.created.isoformat())
        start = sdoc.created
        end = start + timedelta(minutes=60)
        data = dict(id=start.isoformat(),
                    start=start.isoformat(),
                    end=end.isoformat(),
                    title='PDF',
                    url=url)
        return data
    
        
    def _get_start_end_userid(self):
        start = self.request.GET['start']
        end = self.request.GET['end']
        user_id = self.request.session['user'].id
        return start, end, user_id

    def render_docs(self):
        start, end, user_id = self._get_start_end_userid()
        serialize = self.serialize_scandoc_for_calendar
        dlist = self.sdm.get_documents(start, end, timestamps=True)
        self.response = [serialize(doc) for doc in dlist]

        



class ScannedDocumentsViewer(BaseViewer):
    def __init__(self, request):
        super(ScannedDocumentsViewer, self).__init__(request)
        prepare_main_layout(self.request)
        self.sdm = ScannedDocumentsManager(self.request.db)
        dirname = self.request.registry.settings['mslemon.scans.directory']
        self.sdm.set_scans_directory(dirname)
        self.sdm.update_database()
        self.dtformat = '%A - %B %d %H:%m'
        
        self._dispatch_table = dict(
            main=self.main_view,
            export=self.export_document,
            view=self.view_document,)
        self.context = self.request.matchdict['context']
        self._view = self.context

        self.dispatch()

    def main_view(self):
        template = 'mslemon:templates/consult/msl-main-scandoc-view.mako'
        default_view = 'agendaDay'
        env = dict()
        content = self.render(template, env)
        self.layout.content = content
        #self.layout.resources.phone_calendar.need()
        self.layout.resources.main_scandoc_view.need()
        self.layout.resources.cornsilk.need()



    def view_document(self):
        id = int(self.request.matchdict['id'])
        sdoc = self.sdm.get(id)
        template = 'mslemon:templates/consult/msl-view-scandoc.mako'
        rst = render_rst
        db = self.request.db
        pcm = self.pcm
        env = dict(pcall=pcall, rst=rst, db=db, User=User, pcm=pcm)
        content = self.render(template, env)
        self.layout.content = content

    def export_document(self):
        id = self.request.matchdict['id']
        doc = self.sdm.get(id)
        r = Response(content_type='application/pdf',
                     body=doc.file.content)
        filename = doc.name
        r.content_disposition = 'attachment; filename="%s"' % filename
        self.response = r
        
                     
        
        
    
    

        
