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
        
    def serialize(self):
        data = dict(id=self.id, street=self.street,
                    street2=self.street2, city=self.city,
                    state=self.state, zip=self.zip)
        return data
    
    

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
            
    def serialize(self):
        data = dict(id=self.id, firstname=self.firstname,
                    lastname=self.lastname, address=self.address,
                    email=self.email, phone=self.phone)
        return data
    
class GlobalContact(Base):
    __tablename__ = 'msl_global_contacts'
    id = Column(Integer,
                ForeignKey('msl_contacts.id'), primary_key=True)
    def __init__(self, id):
        self.id = id

    def serialize(self):
        return dict(id=self.id)
    
class GroupContact(Base):
    __tablename__ = 'msl_group_contacts'
    contact_id = Column(Integer,
                     ForeignKey('msl_contacts.id'), primary_key=True)
    group_id = Column(Integer,
                     ForeignKey('groups.id'), primary_key=True)

    def serialize(self):
        data = dict(contact_id=self.contact_id,
                    group_id=self.group_id)
        return data
    
class UserContact(Base):
    __tablename__ = 'msl_user_contacts'
    contact_id = Column(Integer,
                     ForeignKey('msl_contacts.id'), primary_key=True)
    user_id = Column(Integer,
                     ForeignKey('users.id'), primary_key=True)
    
    def serialize(self):
        data = dict(contact_id=self.contact_id,
                    user_id=self.user_id)
        return data


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

    def serialize(self):
        data = dict(id=self.id, name=self.name,
                    contact_id=self.contact_id, address=self.address,
                    description=self.description)
        return data

            
class ClientContact(Base):
    __tablename__ = 'msl_client_contact'
    client_id = Column(Integer,
                       ForeignKey('msl_clients.id'), primary_key=True)
    contact_id = Column(Integer,
                        ForeignKey('msl_contacts.id'), primary_key=True)

    def serialize(self):
        data = dict(client_id=self.client_id,
                    contact_id=self.contact_id)
        return data


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

    def serialize(self):
        start = self.start.isoformat()
        end = self.end.isoformat()
        start_date = self.start_date.isoformat()
        start_time = self.start_time.isoformat()
        end_date = self.end_date.isoformat()
        end_time = self.end_time.isoformat()
        created = self.created.isoformat()
        data = dict(id=self.id, start=start, end=end,
                    start_date=start_date, start_time=start_time,
                    end_date=end_date, end_time=end_time,
                    all_day=self.all_day, title=self.title,
                    description=self.description, created=created,
                    created_by_id=self.created_by_id, ext=self.ext)
        return data

class EventUser(Base):
    __tablename__ = 'msl_event_users'
    event_id = Column(Integer,
                      ForeignKey('msl_events.id'), primary_key=True)
    user_id = Column(Integer,
                     ForeignKey('users.id'), primary_key=True)
    attached = Column(DateTime)
    attached_by_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    def serialize(self):
        attached = self.attached.isoformat()
        data = dict(event_id=self.event_id, user_id=self.user_id,
                    attached=attached,
                    attached_by_id=self.attached_by_id)
        return data
    

class Description(Base):
    __tablename__ = 'msl_descriptions'
    id = Column(Integer, primary_key=True)
    text = Column(UnicodeText)

    def serialize(self):
        return dict(id=self.id, text=self.text)
    
TicketStatus = Enum('opened', 'pending', 'closed', name='msl_ticket_status_types')

class Ticket(Base):
    __tablename__ = 'msl_tickets'
    id = Column(Integer, primary_key=True)
    created = Column(DateTime)
    title = Column(Unicode(255))
    description_id = Column(Integer, ForeignKey('msl_descriptions.id'),
                            nullable=False)
    
    def serialize(self):
        created = self.created.isoformat()
        data = dict(id=self.id, created=created, title=self.title,
                    description_id=self.description_id)
        return data
    

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
    
    def serialize(self):
        changed = self.changed.isoformat()
        data = dict(id=self.id, ticket_id=self.ticket_id,
                    status=self.status, reason=self.reason,
                    description_id=self.description_id,
                    changed=changed, changed_by_id=self.changed_by_id,
                    handler_id=self.handler_id)
        return data

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

    def serialize(self):
        created = self.created.isoformat()
        last_change = self.last_change.isoformat()
        data = dict(ticket_id=self.ticket_id,
                    last_change_id=self.last_change_id,
                    created=created, last_change=last_change,
                    status=self.status, changed_by_id=self.changed_by_id,
                    handler_id=self.handler_id)
        return data

class PhoneCall(Base):
    __tablename__ = 'msl_phone_calls'
    id = Column(Integer, primary_key=True)
    received = Column(DateTime)
    caller = Column(UnicodeText)
    number = Column(UnicodeText)
    callee_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    received_by_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    ticket_id = Column(Integer, ForeignKey('msl_tickets.id'), nullable=False)
    
    def serialize(self):
        received = self.received.isoformat()
        data = dict(id=self.id, received=received,
                    caller=self.caller, number=self.number,
                    callee_id=self.callee_id,
                    received_by_id=self.received_by_id,
                    ticket_id=self.ticket_id)
        return data


class ContactCall(Base):
    __tablename__ = 'msl_contact_phone_calls'
    contact_id = Column(Integer,
                        ForeignKey('msl_contacts.id'), primary_key=True)
    call_id = Column(Integer,
                     ForeignKey('msl_phone_calls.id'), primary_key=True)

    def serialize(self):
        data = dict(contact_id=self.contact_id,
                    call_id=self.call_id)
        return data
    
class ClientCall(Base):
    __tablename__ = 'msl_client_phone_calls'
    client_id = Column(Integer,
                       ForeignKey('msl_clients.id'), primary_key=True)
    call_id = Column(Integer,
                     ForeignKey('msl_phone_calls.id'), primary_key=True)
    
    def serialize(self):
        data = dict(client_id=self.client_id,
                    call_id=self.call_id)
        return data
    
class File(Base):
    __tablename__ = 'msl_files'
    id = Column(Integer, primary_key=True)
    content = Column(LargeBinary)
    info = Column(PickleType)

    def serialize(self):
        data = dict(id=self.id, content=self.content,
                    info=self.info)
        return data
    

class ScannedDocument(Base):
    __tablename__ = 'msl_scanned_docs'
    created = Column(DateTime, primary_key=True)
    name = Column(Unicode(255), unique=True)
    file_id = Column(Integer,
                       ForeignKey('msl_files.id'))
    info = Column(PickleType)

    def serialize(self):
        created = self.created.isoformat()
        data = dict(created=created, name=self.name,
                    file_id=self.file_id, info=self.info)
        return data
    
                    
class NamedDocument(Base):
    __tablename__ = 'msl_named_docs'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), unique=True)
    file_id = Column(Integer,
                       ForeignKey('msl_files.id'))
    info = Column(PickleType)
    created = Column(DateTime)
    created_by_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    def serialize(self):
        created = self.created.isoformat()
        data = dict(id=self.id, name=self.name,
                    file_id=self.file_id, info=self.info,
                    created=created, created_by_id=self.created_by_id)
        return data

class UnassignedDocument(Base):
    __tablename__ = 'msl_unassigned_docs'
    doc_id = Column(Integer,
                    ForeignKey('msl_named_docs.id'), primary_key=True)

    def serialize(self):
        return dict(doc_id=self.doc_id)
    
class ClientDocument(Base):
    __tablename__ = 'msl_client_docs'
    client_id = Column(Integer,
                       ForeignKey('msl_clients.id'), primary_key=True)
    doc_id = Column(Integer,
                    ForeignKey('msl_named_docs.id'), primary_key=True)
    info = Column(PickleType)
    created = Column(DateTime)
    created_by_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    def serialize(self):
        created = self.created.isoformat()
        data = dict(client_id=self.client_id, doc_id=self.doc_id,
                    info=self.info, created=created,
                    created_by_id=self.created_by_id)
        return data
    
class TicketDocument(Base):
    __tablename__ = 'msl_ticket_docs'
    ticket_id = Column(Integer,
                       ForeignKey('msl_tickets.id'), primary_key=True)
    doc_id = Column(Integer,
                    ForeignKey('msl_named_docs.id'), primary_key=True)
    info = Column(PickleType)
    attached = Column(DateTime)
    attached_by_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    def serialize(self):
        attached = self.attached.isoformat()
        data = dict(ticket_id=self.ticket_id, doc_id=self.doc_id,
                    info=self.info, attached=attached,
                    attached_by_id=self.attached_by_id)
        return data
    
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

    def serialize(self):
        created = self.created.isoformat()
        data = dict(id=self.id, name=self.name, client_id=self.client_id,
                    description_id=self.description_id, info=self.info,
                    created=created, created_by_id=self.created_by_id)
        return data

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
    
    def serialize(self):
        changed = self.changed.isoformat()
        data = dict(id=self.id, case_id=self.case_id,
                    status=self.status, reason=self.reason,
                    description_id=self.description_id,
                    changed=changed, changed_by_id=self.changed_by_id,
                    handler_id=self.handler_id)
        return data


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

    def serialize(self):
        created = self.created.isoformat()
        last_change = self.last_change.isoformat()
        data = dict(case_id=self.case_id,
                    last_change_id=self.last_change_id,
                    created=created, last_change=last_change,
                    status=self.status, changed_by_id=self.changed_by_id,
                    handler_id=self.handler_id)
        return data

class CaseUser(Base):
    __tablename__ = 'msl_case_users'
    case_id = Column(Integer,
                     ForeignKey('msl_cases.id'), primary_key=True)
    user_id = Column(Integer,
                     ForeignKey('users.id'), primary_key=True)

    def serialize(self):
        return dict(case_id=self.case_id, user_id=self.user_id)
    
class CaseTicket(Base):
    __tablename__ = 'msl_case_tickets'
    case_id = Column(Integer,
                     ForeignKey('msl_cases.id'), primary_key=True)
    ticket_id = Column(Integer,
                       ForeignKey('msl_tickets.id'), primary_key=True)
    info = Column(PickleType)
    attached = Column(DateTime)
    attached_by_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    def serialize(self):
        attached = self.attached.isoformat()
        data = dict(case_id=self.case_id,
                    ticket_id=self.ticket_id, 
                    info=self.info, attached=attached,
                    attached_by_id=self.attached_by_id)
        return data
    
class CaseDocument(Base):
    __tablename__ = 'msl_case_docs'
    case_id = Column(Integer,
                     ForeignKey('msl_cases.id'), primary_key=True)
    doc_id = Column(Integer,
                    ForeignKey('msl_named_docs.id'), primary_key=True)
    info = Column(PickleType)
    attached = Column(DateTime)
    attached_by_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    def serialize(self):
        attached = self.attached.isoformat()
        data = dict(case_id=self.case_id, doc_id=self.doc_id,
                    info=self.info, attached=attached,
                    attached_by_id=self.attached_by_id)
        return data

class CaseEvent(Base):
    __tablename__ = 'msl_case_events'
    case_id = Column(Integer,
                     ForeignKey('msl_cases.id'), primary_key=True)
    info = Column(PickleType)
    attached = Column(DateTime)
    attached_by_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    def serialize(self):
        attached = self.attached.isoformat()
        data = dict(case_id=self.case_id,
                    info=self.info, attached=attached,
                    attached_by_id=self.attached_by_id)
        return data

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
Event.users = relationship(EventUser)

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
    
