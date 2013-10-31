import os
import cPickle as Pickle

from ConfigParser import ConfigParser
from StringIO import StringIO
from sqlalchemy.orm.exc import NoResultFound
import transaction


from mslemon.models.base import DBSession

# usergroup
from mslemon.models.usergroup import User, Group, Password
from mslemon.models.usergroup import UserGroup, UserConfig

# sitecontent
from mslemon.models.sitecontent import SiteImage
from mslemon.models.sitecontent import SiteText


# cases
from mslemon.models.misslemon import Case, CaseTicket, CaseDocument
from mslemon.models.misslemon import UnassignedDocument
from mslemon.models.misslemon import CaseUser
from mslemon.models.misslemon import CaseStatusChange, CaseCurrentStatus
from mslemon.models.misslemon import CaseEvent

# clients
from mslemon.models.misslemon import Client

# events
from mslemon.models.misslemon import Event
from mslemon.models.misslemon import EventUser

# contacts
from mslemon.models.misslemon import Contact
from mslemon.models.misslemon import ClientContact, GlobalContact
from mslemon.models.misslemon import GroupContact, UserContact

#FIXME: better module name
# documents
from mslemon.models.misslemon import File, ScannedDocument
from mslemon.models.misslemon import NamedDocument, ClientDocument
from mslemon.models.misslemon import UnassignedDocument

# phonecalls
from mslemon.models.misslemon import PhoneCall
from mslemon.models.misslemon import ContactCall, ClientCall

# tickets
from mslemon.models.misslemon import Description
from mslemon.models.misslemon import Ticket, TicketCurrentStatus
from mslemon.models.misslemon import TicketStatusChange
from mslemon.models.misslemon import TicketDocument

# misc
from mslemon.models.misslemon import Address


class DBAdminManager(object):
    def __init__(self, session):
        self.session = session
    
    def _serial_list(self):
        pass

    def _serialize_objects(self, omap):
        data = dict()
        for name, obj in omap.items():
            data[name] = list()
            q = self.session.query(obj)
            for o in q:
                data[name].append(o.serialize())
        return data
    
    def backup_usergroup(self):
        omap = dict(User=User, Group=Group, Password=Password,
                    UserGroup=UserGroup, UserConfig=UserConfig)
        return self._serialize_objects(omap)
    

    def backup_sitecontent(self):
        omap = dict(SiteImage=SiteImage, SiteText=SiteText)
        return self._serialize_objects(omap)
    

    def backup_cases(self):
        omap = dict(Case=Case, CaseTicket=CaseTicket,
                    CaseDocument=CaseDocument,
                    CaseUser=CaseUser,
                    CaseStatusChange=CaseStatusChange,
                    CaseCurrentStatus=CaseCurrentStatus,
                    CaseEvent=CaseEvent)
        return self._serialize_objects(omap)

    def backup_clients(self):
        omap = dict(Client=Client)
        return self._serialize_objects(omap)

    def backup_events(self):
        omap = dict(Event=Event, EventUser=EventUser)
        return self._serialize_objects(omap)

    def backup_contacts(self):
        omap = dict(Contact=Contact, ClientContact=ClientContact,
                    GlobalContact=GlobalContact, GroupContact=GroupContact,
                    UserContact=UserContact)
        return self._serialize_objects(omap)

    def backup_files(self, dirname):
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        for f in self.session.query(File):
            filename = 'file-%d.pickle'  % f.id
            fullname = os.path.join(dirname, filename)
            print "Writing", fullname, len(f.content)
            with file(fullname, 'w') as outfile:
                data = f.serialize()
                Pickle.dump(data, outfile)
                
        
        
