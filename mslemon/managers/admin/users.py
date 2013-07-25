from sqlalchemy.orm.exc import NoResultFound
import transaction


from trumpet.models.base import DBSession
from trumpet.models.usergroup import User, Group, Password
from trumpet.models.usergroup import UserGroup

from trumpet.security import encrypt_password


class UserManager(object):
    def __init__(self, session):
        self.session = session
        
    def user_query(self):
        return self.session.query(User)

    def group_query(self):
        return self.session.query(Group)

    def get_user(self, id):
        return self.user_query().get(id)

    def get_group(self, id):
        return self.group_query().get(id)
        
    def add_user(self, name, password):
        with transaction.manager:
            user = User(name)
            self.session.add(user)
        user = self.session.merge(user)
        self.set_password(user.id, password)
        return user
    

    def set_password(self, user_id, password):
        q = self.session.query(Password).filter_by(user_id=user_id)
        encrypted = encrypt_password(password)
        with transaction.manager:
            try:
                p = q.one()
            except NoResultFound:
                p = Password(user_id, encrypted)
            p.password = encrypted
            self.session.add(p)
            
    def delete_user(self, id):
        with transaction.manager:
            p = self.session.query(Password).get(id)
            if p is not None:
                self.session.delete(p)
            user = self.session.query(User).get(id)
            if user is not None:
                self.session.delete(user)

    def add_user_to_group(self, uid, gid):
        with transaction.manager:
            ug = UserGroup(uid, gid)
            self.session.add(ug)
            

    def add_group(self, name):
        with transaction.manager:
            g = Group(name)
            self.session.add(g)
            
    def list_groups(self):
        return self.group_query().all()

    
    

