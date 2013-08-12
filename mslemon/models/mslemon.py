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
    __tablename__ = 'msl_addresses'
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
    __tablename__ = 'msl_contacts'
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
    __tablename__ = 'msl_clients'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(50), unique=True)
    contact_id = Column(Integer, ForeignKey('msl_contacts.id'))
    address = Column(UnicodeText)
    description = Column(UnicodeText)
    
    def __init__(self, name, contact_id, address='', description=''):
        self.name = name
        self.contact_id = contact_id
        self.address = address
        self.description = description
            
class ClientContact(Base):
    __tablename__ = 'msl_client_contact'
    client_id = Column(Integer, ForeignKey('clients.id'), primary_key=True)
    contact_id = Column(Integer, ForeignKey('contacts.id'), primary_key=True)
    

class Event(Base):
    __tablename__ = 'msl_events'
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

        
class Description(Base):
    __tablename__ = 'msl_descriptions'
    id = Column(Integer, primary_key=True)
    text = Column(UnicodeText)
    
TicketStatus = Enum('opened', 'pending', 'closed')

class Ticket(Base):
    __tablename__ = 'msl_tickets'
    id = Column(Integer, primary_key=True)
    created = Column(DateTime)
    title = Column(Unicode(255))
    description_id = Column(Integer, ForeignKey('msl_descriptions.id'),
                            nullable=False)
    

class TicketStatusChange(Base):
    __tablename__ = 'msl_ticket_status'
    id = Column(Integer, primary_key=True)
    ticket_id = Column(Integer, ForeignKey('msl_tickets.id'), nullable=False)
    status = Column('status', TicketStatus)
    reason = Column(UnicodeText)
    description_id = Column(Integer, ForeignKey('msl_descriptions.id')
                            , nullable=False)
    changed = Column(DateTime)
    changed_by_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    handler_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    

class TicketCurrentStatus(Base):
    __tablename__ = 'msl_ticket_current_status'
    ticket_id = Column(Integer, ForeignKey('msl_tickets.id'), primary_key=True)
    last_change_id = Column(Integer, ForeignKey('msl_ticket_status.id',
                                                nullable=False)
    created = Column(DateTime)
    last_change = Column(DateTime)
    status = Column('status', TicketStatus)
    changed_by_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    handler_id = Column(Integer, ForeignKey('users.id'), nullable=False)


class PhoneCall(Base):
    __tablename__ = 'msl_phone_calls'
    id = Column(Integer, primary_key=True)
    received = Column(DateTime)
    caller = Column(UnicodeText)
    number = Column(UnicodeText)
    callee_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    received_by_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    ticket_id = Column(Integer, ForeignKey('msl_tickets.id'), nullable=False)
    

class ContactCall(Base):
    __tablename__ = 'contact_phone_calls'
    contact_id = Column(Integer, ForeignKey('contacts.id'), primary_key=True)
    call_id = Column(Integer, ForeignKey('phone_calls.id'), primary_key=True)

class ClientCall(Base):
    __tablename__ = 'client_phone_calls'
    client_id = Column(Integer, ForeignKey('clients.id'), primary_key=True)
    call_id = Column(Integer, ForeignKey('phone_calls.id'), primary_key=True)
    
    
    

# relationships    
Ticket.description = relationship(Description)
Ticket.history = relationship(TicketStatus, order_by=TicketStatus.changed)
TicketStatusChange.user = relationship(User)
TicketCurrentStatus.ticket = relationship(Ticket)
TicketCurrentStatus.changed_by = relationship(User)


PhoneCall.ticket = relationship(Ticket)
PhoneCall.callee = relationship(User, foreign_keys=[PhoneCall.callee_id])
PhoneCall.received_by = relationship(User,
                                     foreign_keys=[PhoneCall.received_by_id])

