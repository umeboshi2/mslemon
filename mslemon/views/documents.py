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


from mslemon.managers.documents import DocumentManager

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
    layout.title = 'MSL Documents'
    layout.header = 'MSL Documents'
    layout.subheader = 'MSL Document Management Area'



class MainDocumentViewer(BaseViewer):
    def __init__(self, request):
        super(MainDocumentViewer, self).__init__(request)
        prepare_main_layout(self.request)
        self.docs = DocumentManager(self.request.db)
        self.dtformat = '%A - %B %d %H:%m'
        
        self._dispatch_table = dict(
            main=self.main_view,
            view=self.view_document,
            export=self.export_document,)
        self.context = self.request.matchdict['context']
        self._view = self.context

        url = request.route_url('msl_scandocs', context='main', id='all')
        self.layout.ctx_menu.append_new_entry('Scanned Docs', url)

        url = self.url(context='add', id='something')
        self.layout.ctx_menu.append_new_entry('New Document', url)
        
        self.dispatch()
        

    def main_view(self):
        self.layout.header = 'Main Document View'
        user_id = self.get_current_user_id()
        content = ''
        for ignore, doc in self.docs.get_unassigned(user_id):
            url = self.url(context='view', id=doc.id)
            anchor = '<a href="%s">%s</a>' % (url, doc.name)
            content += anchor
            content += '<br>'
        self.layout.content = content

    def view_document(self):
        id = int(self.request.matchdict['id'])
        template = 'mslemon:templates/consult/msl-unassigned-docs-view.mako'
        doc = self.docs.query().get(id)
        form = "form"
        env = dict(doc=doc, form=form)
        self.layout.content = self.render(template, env)
        
        
    def export_document(self):
        id = self.request.matchdict['id']
        doc = self.docs.get(id)
        r = Response(content_type='application/pdf',
                     body=doc.file.content)
        filename = doc.name
        r.content_disposition = 'attachment; filename="%s"' % filename
        self.response = r
        
