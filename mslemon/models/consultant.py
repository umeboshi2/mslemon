from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Unicode, UnicodeText
from sqlalchemy import ForeignKey, Boolean
from sqlalchemy import Date, Time, DateTime
from sqlalchemy import Enum
from sqlalchemy import PickleType

from sqlalchemy.exc import IntegrityError

from sqlalchemy.orm import relationship, backref

from mslemon.models.base import Base, DBSession
from mslemon.models.usergroup import User


import transaction


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
    address = Column(UnicodeText)
    email = Column(Unicode(50), unique=True)
    phone = Column(Unicode(20))
    
    def __init__(self, firstname, lastname='', email=None, phone=None):
        if firstname:
            self.firstname = firstname
        if lastname:
            self.lastname = lastname
        if email:
            self.email = email
        if phone:
            self.phone = phone
            
class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(50), unique=True)
    contact_id = Column(Integer, ForeignKey('contacts.id'))
    address = Column(UnicodeText)
    description = Column(UnicodeText)
    
    def __init__(self, name, contact_id, address='', description=''):
        self.name = name
        self.contact_id = contact_id
        self.address = address
        self.description = description
            
class ClientContact(Base):
    __tablename__ = 'client_contact'
    client_id = Column(Integer, ForeignKey('clients.id'), primary_key=True)
    contact_id = Column(Integer, ForeignKey('contacts.id'), primary_key=True)
    

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
    ext = Column(PickleType)

    def __init__(self, title):
        self.title = title

        
class Ticket(Base):
    __tablename__ = 'tickets'
    id = Column(Integer, primary_key=True)
    created = Column(DateTime)
    title = Column(Unicode(255))
    description = Column(UnicodeText)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)


class TicketStatusType(Base):
    __tablename__ = 'ticket_status_types'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(50), unique=True)

    def __init__(self, name):
        self.name = name
        
class TicketStatus(Base):
    __tablename__ = 'ticket_status'
    id = Column(Integer, primary_key=True)
    ticket_id = Column(Integer, ForeignKey('tickets.id'), nullable=False)
    status = Column(Integer, ForeignKey('ticket_status_types.id'),
                    nullable=False)
    reason = Column(UnicodeText)
    changed = Column(DateTime)
    changed_by_id = Column(Integer, ForeignKey('users.id'), nullable=False)


class TicketCurrentStatus(Base):
    __tablename__ = 'ticket_current_status'
    ticket_id = Column(Integer, ForeignKey('tickets.id'), primary_key=True)
    created = Column(DateTime)
    last_change = Column(DateTime)
    status = Column(Integer, ForeignKey('ticket_status_types.id'))



class PhoneCall(Base):
    __tablename__ = 'phone_calls'
    id = Column(Integer, primary_key=True)
    received = Column(DateTime)
    caller = Column(UnicodeText)
    number = Column(UnicodeText)
    text = Column(UnicodeText)
    callee = Column(Integer, ForeignKey('users.id'), nullable=False)
    received_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    
class PhoneCallStatusType(Base): 
    __tablename__ = 'phonecall_status_types'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(50), unique=True)

    def __init__(self, name):
        self.name = name

class PhoneCallStatus(Base):
    __tablename__ = 'phonecall_status'
    id = Column(Integer, primary_key=True)
    call_id = Column(Integer, ForeignKey('phone_calls.id'), nullable=False)
    status = Column(Integer, ForeignKey('phonecall_status_types.id'),
                    nullable=False)
    reason = Column(UnicodeText)
    changed = Column(DateTime)
    changed_by_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    handler = Column(Integer, ForeignKey('users.id'), nullable=False)
    
class PhoneCallCurrentStatus(Base):
    __tablename__ = 'phonecall_current_status'
    call_id = Column(Integer, ForeignKey('phone_calls.id'), primary_key=True)
    created = Column(DateTime)
    last_change = Column(DateTime)
    status = Column(Integer, ForeignKey('phonecall_status_types.id'))
    handler = Column(Integer, ForeignKey('users.id'), nullable=False)


class PhoneCallTicket(Base):
    __tablename__ = 'phonecall_tickets'
    call_id = Column(Integer, ForeignKey('phone_calls.id'), primary_key=True)
    ticket_id = Column(Integer, ForeignKey('tickets.id'), primary_key=True)

class ContactCall(Base):
    __tablename__ = 'contact_phone_calls'
    contact_id = Column(Integer, ForeignKey('contacts.id'), primary_key=True)
    call_id = Column(Integer, ForeignKey('phone_calls.id'), primary_key=True)

class ClientCall(Base):
    __tablename__ = 'client_phone_calls'
    client_id = Column(Integer, ForeignKey('clients.id'), primary_key=True)
    call_id = Column(Integer, ForeignKey('phone_calls.id'), primary_key=True)
    
    
    

# relationships    
Ticket.history = relationship(TicketStatus, order_by=TicketStatus.changed)
TicketStatus.user = relationship(User)
TicketCurrentStatus.ticket = relationship(Ticket)

PhoneCall.history = relationship(PhoneCallStatus,
                                 order_by=PhoneCallStatus.changed)
PhoneCall.status = relationship(PhoneCallCurrentStatus)

PhoneCallCurrentStatus.phone_call = relationship(PhoneCall)

# populate db

def populate_ticket_status():
    session = DBSession()
    tslist = ['opened',
              'started',
              'troubleshooting',
              'waiting parts',
              'waiting service',
              'writing code',
              'waiting client',
              'closed']
    try:
        with transaction.manager:
            for status in tslist:
                ts = TicketStatusType(status)
                session.add(ts)
    except IntegrityError:
        transaction.abort()
        

def populate_phonecall_status():
    session = DBSession()
    pcslist = ['opened',
              'pending',
              'closed']
    try:
        with transaction.manager:
            for status in pcslist:
                pcs = PhoneCallStatusType(status)
                session.add(pcs)
    except IntegrityError:
        transaction.abort()
    
