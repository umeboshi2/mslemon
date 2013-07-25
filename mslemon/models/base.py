import transaction

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Unicode, UnicodeText
from sqlalchemy import ForeignKey, Boolean
from sqlalchemy import Date, Time, DateTime
from sqlalchemy import Enum
from sqlalchemy import PickleType

from sqlalchemy.exc import IntegrityError

from sqlalchemy.orm import relationship, backref

from trumpet.models.base import DBSession, Base

# these seem to be there anyway
import trumpet.models.usergroup

# sitecontent is useful
import trumpet.models.sitecontent

# some of the classes below are similar to
# trumpet consultant classes


class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    street = Column(Unicode(150))
    street2 = Column(Unicode(150), default=None)
    city = Column(Unicode(50))
    state = Column(Unicode(2))
    zip = Column(Unicode(10))

    def __init__(self, street, city=None,
                 state=None, zip=None):
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip
        
        
class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    firstname = Column(Unicode(50))
    lastname = Column(Unicode(50))
    email = Column(Unicode(50), unique=True)
    phone = Column(Unicode(20))
    users = relationship('User')
    
    def __init__(self, firstname='', lastname='', email='', phone=''):
        if firstname:
            self.firstname = firstname
        if lastname:
            self.lastname = lastname
        if email:
            self.email = email
        if phone:
            self.phone = phone
            

    
class EventType(Base):
    __tablename__ = 'event_types'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(50), unique=True)

    def __init__(self, name=None):
        self.name = name
    

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    start_date = Column(Date)
    start_time = Column(Time)
    end_date = Column(Date)
    end_time = Column(Time)
    all_day = Column(Boolean, default=False)
    title = Column(Unicode(255))
    description = Column(UnicodeText)
    originator = Column(Integer, ForeignKey('users.id'))
    event_type = Column(Integer, ForeignKey('event_types.id'))

    def __init__(self, originator):
        self.originator = originator
    
        


class LoginHistory(Base):
    __tablename__ = 'login_history'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    when = Column(DateTime, primary_key=True)
    
