from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Unicode
from sqlalchemy import ForeignKey


from sqlalchemy.orm import relationship

from base import Base

# imports for populate()
import transaction
from sqlalchemy.exc import IntegrityError
from base import DBSession


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(Unicode(50), unique=True)
    email = Column(Unicode(50), unique=True)
    pw = relationship('Password', uselist=False)

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return self.username

    def get_groups(self):
        return [g.name for g in self.groups]


class Password(Base):
    __tablename__ = 'passwords'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    password = Column(Unicode(150))

    def __init__(self, user_id, password):
        self.user_id = user_id
        self.password = password


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(50), unique=True)

    def __init__(self, name):
        self.name = name


class UserGroup(Base):
    __tablename__ = 'group_user'
    group_id = Column(Integer, ForeignKey('groups.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)

    def __init__(self, gid, uid):
        self.group_id = gid
        self.user_id = uid


User.groups = relationship(Group, secondary='group_user')
Group.users = relationship(User, secondary='group_user')



def populate_groups():
    session = DBSession()
    groups = ['user', 'admin', 'guest', 'manager']
    with transaction.manager:
        for gname in groups:
            group = Group(gname)
            session.add(group)


def populate_users(admin_username):
    from trumpet.security import encrypt_password
    session = DBSession()
    with transaction.manager:
        users = [admin_username]
        # Using id_count to presume
        # the user's id, which should work
        # when filling an empty database.
        id_count = 0
        for uname in users:
            id_count += 1
            user = User(uname)
            password = encrypt_password(uname)
            session.add(user)
            pw = Password(id_count, password)
            session.add(pw)

def populate_usergroups():
    session = DBSession()
    with transaction.manager:
        users = [(1, 1)]  # admin user should be 1
        admins = [(2, 1)]  # admin user should be 1
        all = users + admins
        for gid, uid in all:
            row = UserGroup(gid, uid)
            session.add(row)


def populate(admin_username):
    try:
        populate_groups()
    except IntegrityError:
        transaction.abort()
    try:
        populate_users(admin_username)
    except IntegrityError:
        transaction.abort()
    try:
        populate_usergroups()
    except IntegrityError:
        transaction.abort()
