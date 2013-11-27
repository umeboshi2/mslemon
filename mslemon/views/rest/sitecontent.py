from cornice.resource import resource, view

from trumpet.models.sitecontent import SiteTemplate
from trumpet.models.sitecontent import SiteCSS, SiteJS

from trumpet.managers.admin.sitecontent import SiteContentManager

from mslemon.views.rest.base import BaseResource


@resource(collection_path='/rest/sitetmpl', path='/rest/sitetmpl/{id}',
          permission='admin')
class SiteTemplateResource(BaseResource):
    dbmodel = SiteTemplate

    def __init__(self, request):
        super(SiteTemplateResource, self).__init__(request)
        self.mgr = SiteContentManager(self.db)
        
    
    def collection_get(self):
        q = self.mgr.tmpl_query()
        return dict(data=[o.serialize() for o in q])

    def collection_post(self):
        name = self.request.json['name']
        content = self.request.json['content']
        t = self.mgr.add_template(name, content)
        data = t.serialize()
        data['result'] = 'success'
        return data

    def put(self):
        content = self.request.json['content']
        id = int(self.request.matchdict['id'])
        t = self.mgr.update_template(id, content)
        data = dict(obj=t.serialize(), result='success')
        return data

    def delete(self):
        id = int(self.request.matchdict['id'])
        db = self.request.db
        with transaction.manager:
            t = self.mgr.tmpl_query().get(id)
            if t is not None:
                db.delete(t)
        return dict(result='success')


@resource(collection_path='/rest/sitecss', path='/rest/sitecss/{id}',
          permission='admin')
class SiteCSSResource(BaseResource):
    dbmodel = SiteCSS

    def __init__(self, request):
        super(SiteCSSResource, self).__init__(request)
        self.mgr = SiteContentManager(self.db)
        
    
    def collection_get(self):
        q = self.mgr.css_query()
        return dict(data=[o.serialize() for o in q])

    def collection_post(self):
        name = self.request.json['name']
        content = self.request.json['content']
        t = self.mgr.add_css(name, content)
        data = t.serialize()
        data['result'] = 'success'
        return data

    def put(self):
        content = self.request.json['content']
        id = int(self.request.matchdict['id'])
        t = self.mgr.update_css(id, content)
        data = dict(obj=t.serialize(), result='success')
        return data

    def delete(self):
        id = int(self.request.matchdict['id'])
        db = self.request.db
        with transaction.manager:
            t = self.mgr.css_query().get(id)
            if t is not None:
                db.delete(t)
        return dict(result='success')
    
@resource(collection_path='/rest/sitejs', path='/rest/sitejs/{id}',
          permission='admin')
class SiteJSResource(BaseResource):
    dbmodel = SiteJS

    def __init__(self, request):
        super(SiteJSResource, self).__init__(request)
        self.mgr = SiteContentManager(self.db)
        
    
    def collection_get(self):
        q = self.mgr.js_query()
        return dict(data=[o.serialize() for o in q])

    def collection_post(self):
        name = self.request.json['name']
        content = self.request.json['content']
        t = self.mgr.add_js(name, content)
        data = t.serialize()
        data['result'] = 'success'
        return data

    def put(self):
        content = self.request.json['content']
        id = int(self.request.matchdict['id'])
        t = self.mgr.update_js(id, content)
        data = dict(obj=t.serialize(), result='success')
        return data

    def delete(self):
        id = int(self.request.matchdict['id'])
        db = self.request.db
        with transaction.manager:
            t = self.mgr.js_query().get(id)
            if t is not None:
                db.delete(t)
        return dict(result='success')
    
