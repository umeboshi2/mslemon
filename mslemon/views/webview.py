import os

from mako.template import Template

from pyramid.renderers import render
from pyramid.response import Response, FileResponse

from pyramid.path import AssetResolver

from pyramid.httpexceptions import HTTPNotFound

from trumpet.views.webview import BaseWebView
from trumpet.views.webview import WebAppView

from trumpet.managers.admin.sitewebview import SiteWebviewManager


LOADER_TEMPLATE = """\
define(['cs!../stdlib/coffee/config', 'cs!${loader}'], function (AppName){
    console.log("Running ${loader}");
    AppName();
});
"""

def static_asset_response(request, asset):
    resolver = AssetResolver()
    descriptor = resolver.resolve(asset)
    if not descriptor.exists():
        raise HTTPNotFound(request.url)
    response = FileResponse(descriptor.abspath(), request)
    zip_response = False
    for ending in ['.css', '.js', '.coffee', '.html']:
        zip_response = True
    if zip_response:
        response.encode_content()
    return response


class WebView(WebAppView):
    def __init__(self, request):
        super(WebView, self).__init__(request)
        #resources = self.request.root.static_resources
        #resources.initialize_webview_layout.need()
        #resources.favicon.need()
        #resources.fullcalendar.need()
        #resources.backbone.need()
        #resources.require.need()
        #resources.require.main.need()
        view_name = request.view_name
        print "view_name", view_name
        nextdir = request.subpath[0]
        subpath = os.path.join(*request.subpath)
        print "request.subpath", request.subpath
        #import pdb ; pdb.set_trace()
        if nextdir == 'apples':
            subpath = os.path.join(*request.subpath[1:])
            js = self.mgr.get_js_by_name(subpath)
            print "SUBPATH", subpath
            print "JS", js
            template = 'trumpet:templates/webview-main.mako'
        
            env = dict(datamain='loader')
            
            content = render(template, env)
            self.response = Response(body=content)            
        elif nextdir == 'stdlib':
            asset = 'haberdashery:%s' % '/'.join(request.subpath)
            self.response = static_asset_response(request, asset)
        elif len(request.subpath) > 1 and request.subpath[1] == 'stdlib':
            asset = 'haberdashery:%s' % '/'.join(request.subpath)
            self.response = static_asset_response(request, asset)
        elif request.subpath[-1] == 'loader.js':
            appname = request.subpath[0]
            #js = self.mgr.get_js_by_name(appname)
        
            print "LOADER!!!!!!", appname, request.subpath
            print "WE MADE IT THIS FAR"
            template = Template(LOADER_TEMPLATE)
            #env = dict(loader='stdlib/coffee/config')
            loader = os.path.join('../', 'app', appname)
            print "loader", loader, request.path
            env = dict(loader=loader)
            #import pdb ; pdb.set_trace()
            content = template.render(**env)
            self.response = Response(body=content,
                                content_type='text/javascript')
        elif request.subpath[-1] in ['cs.js', 'coffee-script.js']:
            asset = 'haberdashery:/stdlib/%s' % request.subpath[-1]
            self.response = static_asset_response(request, asset)
        elif nextdir == 'app':
            name = os.path.join(*request.subpath[1:])
            filetype = 'text/html'
            if name.endswith('.js'):
                name = name[:-3]
                filetype = 'text/javascript'
            elif name.endswith('.coffee'):
                name = name[:-7]
                filetype = 'text/coffeescript'
                
            js = self.mgr.get_js_by_name(name)
            response = Response(body=js.content,
                                content_type=filetype)
            response.encode_content()
            self.response = response
        else:
            self.data = dict(datamain=subpath)
            subpath = os.path.join(*request.subpath)
            print "SSSSSSSSSSSSUBPATH", subpath
            template = 'trumpet:templates/webview-main.mako'
            env = dict(datamain='%s/loader' % subpath)
            content = render(template, env)
            self.response = Response(body=content)

        self.context = self.request.context
        
        
        
