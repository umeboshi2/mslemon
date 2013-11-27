import transaction
from cornice.resource import resource, view

from trumpet.models.sitecontent import SiteText


class BaseResource(object):
    def __init__(self, request):
        self.request = request
        self.db = self.request.db
        if not hasattr(self, 'dbmodel'):
            msg = "need to set dbmodel property before __init__"
            raise RuntimeError, msg

    def _query(self):
        return self.db.query(self.dbmodel)

    def _get(self, id):
        return self._query().get(id)
    
    def collection_get(self):
        raise RuntimeError, "implement in subclass"

    def get(self):
        id = int(self.request.matchdict['id'])
        return self._get(id).serialize()
    
    def collection_post(self):
        raise RuntimeError, "implement in subclass"

    def put(self):
        raise RuntimeError, "implement in subclass"

    def delete(self):
        raise RuntimeError, "implement in subclass"
    

@resource(collection_path='/rest/sitetext', path='/rest/sitetext/{id}',
          permission='admin')
class SiteTextResource(BaseResource):
    dbmodel = SiteText
    
    def collection_get(self):
        #doc_ids = [st.id for st in self._query()]
        return dict(data=[st.serialize() for st in self._query()])

    def collection_post(self):
        request = self.request
        db = request.db
        with transaction.manager:
            st = SiteText()
            st.name = request.json['name']
            st.content = request.json['content']
            st.type = 'tutwiki'
            db.add(st)
        st = db.merge(st)
        data = st.serialize()
        data['result'] = 'success'
        return data

    def put(self):
        request = self.request
        db = request.db
        id = int(request.matchdict['id'])
        with transaction.manager:
            st = db.query(SiteText).get(id)
            if st is not None:
                st.content = request.json['content']
                st.modified = datetime.now()
                db.add(st)
                result = dict(result='success')
            else:
                result = dict(result='failure')
        st = db.merge(st)
        result['obj'] = st.serialize()
        return result

    def delete(self):
        request = self.request
        db = request.db
        id = int(request.matchdict['id'])
        with transaction.manager:
            st = db.query(SiteText).get(id)
            if st is not None:
                db.delete(st)
        return dict(result='success')
    
    
