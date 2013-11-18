from cStringIO import StringIO
from datetime import datetime

import transaction

from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.security import authenticated_userid
from pyramid.renderers import render


from trumpet.resources import MemoryTmpStore


from trumpet.views.menus import BaseMenu

from mslemon.views.base import AdminViewer
from mslemon.views.admin.base import make_main_menu


import colander
import deform

tmpstore = MemoryTmpStore()

def prepare_main_data(request):
    layout = request.layout_manager.layout
    layout.main_menu = make_main_menu(request)
    layout.title = 'Manage Images'
    layout.header = 'Manage Images' 


    
        
class DBAdminViewer(AdminViewer):
    def __init__(self, request):
        super(DBAdminViewer, self).__init__(request)
        prepare_main_data(self.request)

        self._dispatch_table = dict(
            list=self.list_images,
            add=self.add_image,
            delete=self.delete_image,
            confirmdelete=self.confirm_delete_image,)
        self.context = self.request.matchdict['context']
        self._view = self.context
        self.dispatch()
        
    def list_images(self):
        images = self.images.images_query().all()
        template = 'trumpet:templates/image-list.mako'
        env = dict(images=images)
        content = render(template, env, request=self.request)
        self.layout.content = content
        self.layout.resources.manage_images.need()

    def add_image(self):
        schema = AddImageSchema()
        form = deform.Form(schema, buttons=('submit',))
        self.layout.resources.deform_auto_need(form)
        if 'submit' in self.request.POST:
            controls = self.request.POST.items()
            self.layout.subheader = 'Image Submitted'
            try:
                data = form.validate(controls)
            except deform.ValidationFailure, e:
                self.layout.content = e.render()
                return
            upload = data['upload']
            fp = data['upload']['fp']
            name = data['name']
            image = self.images.add_image(name, fp)
            url = self.request.route_url('blob', filetype='thumb',
                                         id=image.id)
            content = '<img id="%d" src="%s"><br>' % (image.id, url)
            content += '<p>Image %s added.</p>' % image.name
            self.layout.content = content
            return
        rendered = form.render()
        self.layout.content = rendered
        self.layout.subheader = 'Upload an Image'

    def delete_image(self):
        id = int(self.request.matchdict['id'])
        image_url = self.request.route_url('blob', filetype='image', id=id)
        env = dict(id=id, image_url=image_url)
        template = 'trumpet:templates/delete-image.mako'
        content = render(template, env, request=self.request)
        self.layout.content = content
        self.layout.resources.manage_images.need()
        
    def confirm_delete_image(self):
        id = int(self.request.matchdict['id'])
        self.images.delete_image(id)
            
