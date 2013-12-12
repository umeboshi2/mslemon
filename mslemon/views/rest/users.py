from cornice.resource import resource, view


from trumpet.models.usergroup import User, Group, Password
from trumpet.models.usergroup import UserGroup

from trumpet.managers.admin.users import UserManager

from trumpet.security import encrypt_password

from mslemon.views.rest.base import BaseResource

# FIXME: this needs to be in manager
import transaction

@resource(collection_path='/rest/users', path='/rest/users/{id}',
          permission='admin')
class UserResource(BaseResource):
    dbmodel = User

    def __init__(self, request):
        super(UserResource, self).__init__(request)
        self.mgr = UserManager(self.db)
        
    
    def collection_get(self):
        q = self.mgr.user_query()
        return dict(data=[o.serialize() for o in q])

    def collection_post(self):
        name = self.request.json['name']
        password = self.request.json['password']
        obj = self.mgr.add_user(name, password)
        data = dict(obj=obj.serialize(), result='success')
        return data

    def delete(self):
        id = int(self.request.matchdict['id'])
        self.mgr.delete_user(id)
        return dict(result='success')


@resource(collection_path='/rest/groups', path='/rest/groups/{id}',
          permission='admin')
class GroupResource(BaseResource):
    dbmodel = Group

    def __init__(self, request):
        super(GroupResource, self).__init__(request)
        self.mgr = UserManager(self.db)

    def collection_get(self):
        q = self.mgr.group_query()
        return dict(data=[o.serialize() for o in q])

    def collection_post(self):
        name = self.request.json['name']
        g = self.mgr.add_group(name)
        return dict(obj=g.serialize(), result='success')

    def delete(self):
        id = int(self.request.matchdict['id'])
        self.mgr.delete_group(id)
        return dict(result='success')

@resource(collection_path='/rest/user/{uid}/groups', path='/rest/user/{uid}/groups/{id}',
          permission='admin')
class UserGroupResource(BaseResource):
    dbmodel = UserGroup
    
    def __init__(self, request):
        super(GroupResource, self).__init__(request)
        self.mgr = UserManager(self.db)

    def collection_get(self):
        q = self.mgr.group_query()
        return dict(data=[o.serialize() for o in q])

    def collection_post(self):
        name = self.request.json['name']
        g = self.mgr.add_group(name)
        return dict(obj=g.serialize(), result='success')

    def delete(self):
        id = int(self.request.matchdict['id'])
        self.mgr.delete_group(id)
        return dict(result='success')
    
