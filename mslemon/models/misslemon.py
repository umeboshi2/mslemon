from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Unicode, UnicodeText
from sqlalchemy import ForeignKey, Boolean
from sqlalchemy import Date, Time, DateTime
from sqlalchemy import Enum
from sqlalchemy import PickleType
from sqlalchemy import LargeBinary

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
            
class GlobalContact(Base):
    __tablename__ = 'msl_global_contacts'
    id = Column(Integer,
                ForeignKey('msl_contacts.id'), primary_key=True)
    def __init__(self, id):
        self.id = id

class GroupContact(Base):
    __tablename__ = 'msl_group_contacts'
    contact_id = Column(Integer,
                     ForeignKey('msl_contacts.id'), primary_key=True)
    group_id = Column(Integer,
                     ForeignKey('groups.id'), primary_key=True)

    
class UserContact(Base):
    __tablename__ = 'msl_user_contacts'
    contact_id = Column(Integer,
                     ForeignKey('msl_contacts.id'), primary_key=True)
    user_id = Column(Integer,
                     ForeignKey('users.id'), primary_key=True)
    


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
    client_id = Column(Integer,
                       ForeignKey('msl_clients.id'), primary_key=True)
    contact_id = Column(Integer,
                        ForeignKey('msl_contacts.id'), primary_key=True)


class Event(Base):
    __tablename__ = 'msl_events'
    id = Column(Integer, primary_key=True)
    start = Column(DateTime)
    end = Column(DateTime)
    # splitting dates and times makes for useful
    # queries when looking for events in a time range
    # but not a date range.
    start_date = Column(Date)
    start_time = Column(Time)
    end_date = Column(Date)
    end_time = Column(Time)
    all_day = Column(Boolean, default=False)
    title = Column(Unicode(255))
    description = Column(UnicodeText)
    created = Column(DateTime)
    created_by_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    ext = Column(PickleType)

    def __init__(self, title):
        self.title = title

class EventUser(Base):
    __tablename__ = 'msl_event_users'
    event_id = Column(Integer,
                      ForeignKey('msl_events.id'), primary_key=True)
    user_id = Column(Integer,
                     ForeignKey('users.id'), primary_key=True)
    attached = Column(DateTime)
    attached_by_id = Column(Integer, ForeignKey('users.id'), nullable=False)


class Description(Base):
    __tablename__ = 'msl_descriptions'
    id = Column(Integer, primary_key=True)
    text = Column(UnicodeText)
    
TicketStatus = Enum('opened', 'pending', 'closed', name='msl_ticket_status_types')

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
    last_change_id = Column(Integer, ForeignKey('msl_ticket_status.id'),
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
    __tablename__ = 'msl_contact_phone_calls'
    contact_id = Column(Integer,
                        ForeignKey('msl_contacts.id'), primary_key=True)
    call_id = Column(Integer,
                     ForeignKey('msl_phone_calls.id'), primary_key=True)

class ClientCall(Base):
    __tablename__ = 'msl_client_phone_calls'
    client_id = Column(Integer,
                       ForeignKey('msl_clients.id'), primary_key=True)
    call_id = Column(Integer,
                     ForeignKey('msl_phone_calls.id'), primary_key=True)
    
    
class File(Base):
    __tablename__ = 'msl_files'
    id = Column(Integer, primary_key=True)
    content = Column(LargeBinary)
    info = Column(PickleType)


class ScannedDocument(Base):
    __tablename__ = 'msl_scanned_docs'
    created = Column(DateTime, primary_key=True)
    name = Column(Unicode(255), unique=True)
    file_id = Column(Integer,
                       ForeignKey('msl_files.id'))
    info = Column(PickleType)

class NamedDocument(Base):
    __tablename__ = 'msl_named_docs'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), unique=True)
    file_id = Column(Integer,
                       ForeignKey('msl_files.id'))
    info = Column(PickleType)
    created = Column(DateTime)
    created_by_id = Column(Integer, ForeignKey('users.id'), nullable=False)

class UnassignedDocument(Base):
    __tablename__ = 'msl_unassigned_docs'
    doc_id = Column(Integer,
                    ForeignKey('msl_named_docs.id'), primary_key=True)

class ClientDocument(Base):
    __tablename__ = 'msl_client_docs'
    client_id = Column(Integer,
                       ForeignKey('msl_clients.id'), primary_key=True)
    doc_id = Column(Integer,
                    ForeignKey('msl_named_docs.id'), primary_key=True)
    info = Column(PickleType)
    created = Column(DateTime)
    created_by_id = Column(Integer, ForeignKey('users.id'), nullable=False)

class TicketDocument(Base):
    __tablename__ = 'msl_ticket_docs'
    ticket_id = Column(Integer,
                       ForeignKey('msl_tickets.id'), primary_key=True)
    doc_id = Column(Integer,
                    ForeignKey('msl_named_docs.id'), primary_key=True)
    info = Column(PickleType)
    attached = Column(DateTime)
    attached_by_id = Column(Integer, ForeignKey('users.id'), nullable=False)

CaseStatus = Enum('opened', 'pending', 'closed', name='msl_case_status_types')

class Case(Base):
    __tablename__ = 'msl_cases'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), unique=True)
    client_id = Column(Integer,
                       ForeignKey('msl_clients.id'), nullable=False)
    description_id = Column(Integer, ForeignKey('msl_descriptions.id'),
                            nullable=False)
    info = Column(PickleType)
    created = Column(DateTime)
    created_by_id = Column(Integer, ForeignKey('users.id'), nullable=False)

class CaseStatusChange(Base):
    __tablename__ = 'msl_case_status'
    id = Column(Integer, primary_key=True)
    case_id = Column(Integer, ForeignKey('msl_cases.id'), nullable=False)
    status = Column('status', CaseStatus)
    reason = Column(UnicodeText)
    description_id = Column(Integer, ForeignKey('msl_descriptions.id')
                            , nullable=False)
    changed = Column(DateTime)
    changed_by_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    handler_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    

class CaseCurrentStatus(Base):
    __tablename__ = 'msl_case_current_status'
    case_id = Column(Integer, ForeignKey('msl_cases.id'), primary_key=True)
    last_change_id = Column(Integer, ForeignKey('msl_case_status.id'),
                                                nullable=False)
    created = Column(DateTime)
    last_change = Column(DateTime)
    status = Column('status', CaseStatus)
    changed_by_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    handler_id = Column(Integer, ForeignKey('users.id'), nullable=False)


class CaseUser(Base):
    __tablename__ = 'msl_case_users'
    case_id = Column(Integer,
                     ForeignKey('msl_cases.id'), primary_key=True)
    user_id = Column(Integer,
                     ForeignKey('users.id'), primary_key=True)
    
class CaseTicket(Base):
    __tablename__ = 'msl_case_tickets'
    case_id = Column(Integer,
                     ForeignKey('msl_cases.id'), primary_key=True)
    ticket_id = Column(Integer,
                       ForeignKey('msl_tickets.id'), primary_key=True)
    info = Column(PickleType)
    attached = Column(DateTime)
    attached_by_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    
class CaseDocument(Base):
    __tablename__ = 'msl_case_docs'
    case_id = Column(Integer,
                     ForeignKey('msl_cases.id'), primary_key=True)
    doc_id = Column(Integer,
                    ForeignKey('msl_named_docs.id'), primary_key=True)
    info = Column(PickleType)
    attached = Column(DateTime)
    attached_by_id = Column(Integer, ForeignKey('users.id'), nullable=False)


class CaseEvent(Base):
    __tablename__ = 'msl_case_events'
    case_id = Column(Integer,
                     ForeignKey('msl_cases.id'), primary_key=True)
    info = Column(PickleType)
    attached = Column(DateTime)
    attached_by_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
#######################
# contacts
#######################
GlobalContact.contact = relationship(Contact)
GroupContact.contact = relationship(Contact)
UserContact.contact = relationship(Contact)

Contact.groups = relationship(GroupContact)
Contact.users = relationship(UserContact)
Contact.clients = relationship(ClientContact)
#######################
# tickets
#######################
# relationships    
Ticket.description = relationship(Description)
Ticket.history = relationship(TicketStatusChange,
                              order_by=TicketStatusChange.changed)
Ticket.current_status = relationship(TicketCurrentStatus, uselist=False)

TicketStatusChange.handler = \
    relationship(User, foreign_keys=[TicketStatusChange.handler_id])
TicketStatusChange.changed_by = \
    relationship(User, foreign_keys=[TicketStatusChange.changed_by_id])
    
TicketCurrentStatus.ticket = relationship(Ticket)
TicketCurrentStatus.changed_by = \
    relationship(User, foreign_keys=[TicketCurrentStatus.changed_by_id])
TicketCurrentStatus.handler = \
    relationship(User, foreign_keys=[TicketCurrentStatus.handler_id])

#######################
# phone calls
#######################

PhoneCall.ticket = relationship(Ticket)
PhoneCall.callee = relationship(User, foreign_keys=[PhoneCall.callee_id])
PhoneCall.received_by = relationship(User,
                                     foreign_keys=[PhoneCall.received_by_id])

#######################
# documents
#######################
ScannedDocument.file = relationship(File)

NamedDocument.file = relationship(File)
NamedDocument.created_by = relationship(User)

UnassignedDocument.doc = relationship(NamedDocument)

#######################
# events
#######################
Event.created_by = relationship(User)

#######################
# cases
#######################
Case.description = relationship(Description)
Case.users = relationship(CaseUser)
Case.tickets = relationship(CaseTicket)
Case.documents = relationship(CaseDocument)
Case.created_by = relationship(User)

Case.history = relationship(CaseStatusChange,
                              order_by=CaseStatusChange.changed)
Case.current_status = relationship(CaseCurrentStatus, uselist=False)


CaseStatusChange.handler = \
    relationship(User, foreign_keys=[CaseStatusChange.handler_id])
CaseStatusChange.changed_by = \
    relationship(User, foreign_keys=[CaseStatusChange.changed_by_id])
    
CaseCurrentStatus.case = relationship(Case)
CaseCurrentStatus.changed_by = \
    relationship(User, foreign_keys=[CaseCurrentStatus.changed_by_id])
CaseCurrentStatus.handler = \
    relationship(User, foreign_keys=[CaseCurrentStatus.handler_id])

CaseUser.user = relationship(User)

CaseDocument.document = relationship(NamedDocument)

CaseTicket.ticket = relationship(Ticket)

            
def populate_sitetext():
    from trumpet.models.sitecontent import SiteText
    session = DBSession()
    try:
        with transaction.manager:
            page = SiteText('FrontPage',
                            'This is the front page.', type='tutwiki')
            session.add(page)
    except IntegrityError:
        pass
    
