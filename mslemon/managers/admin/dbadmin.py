import os
import cPickle as Pickle
from zipfile import ZipFile, ZIP_DEFLATED
import csv
from ConfigParser import ConfigParser
from StringIO import StringIO
from datetime import datetime

from sqlalchemy.orm.exc import NoResultFound
import transaction

from dateutil.parser import parse as dtparse

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

#FIXME: better module namelist
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

DBOBJECTS = ['User', 'Group', 'Password',
             'UserGroup', 'UserConfig', 'SiteImage',
             'SiteText', 'Case', 'CaseTicket', 'CaseDocument',
             'CaseUser', 'CaseStatusChange', 'CaseCurrentStatus',
             'CaseEvent', 'Client', 'Event', 'EventUser',
             'Contact', 'ClientContact', 'GlobalContact',
             'GroupContact', 'UserContact', 'File', 'ScannedDocument',
             'UnassignedDocument', 'PhoneCall', 'ContactCall',
             'ClientCall', 'Description', 'Ticket', 'TicketCurrentStatus',
             'TicketStatusChange', 'TicketDocument', 'Address']

             
empty_init_objects = ['GroupContact',
                      'UserContact',
                      'ClientContact',
                      'EventUser',
                      'Description',
                      'Ticket',
                      'TicketStatusChange',
                      'TicketCurrentStatus',
                      'PhoneCall',
                      'ContactCall',
                      'ClientCall',
                      'File',
                      'ScannedDocument',
                      'NamedDocument',
                      'UnassignedDocument',
                      'ClientDocument',
                      'TicketDocument',
                      'Case',
                      'CaseStatusChange',
                      'CaseCurrentStatus',
                      'CaseUser',
                      'CaseTicket',
                      'CaseDocument',
                      'CaseEvent',
                      ]


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
        #omap = dict(SiteImage=SiteImage, SiteText=SiteText)
        omap = dict(SiteImage=SiteImage)
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

    def backup_file(self, zfile, file_id):
        filename = 'files/file-%d' % file_id
        f = self.session.query(File).get(file_id)
        print "Writing", filename, len(f.content)
        zfile.writestr(filename, f.content)
        return dict(id=f.id, info=f.info)
    
    
    def backup_files(self, zfile):
        filelist = list()
        for file_id in self.session.query(File.id):
            data = self.backup_file(zfile, file_id.id)
            filelist.append(data)
        #zfile.writestr('fileinfo.pickle', Pickle.dumps(filelist))
        return filelist
    
    def backup_documents(self):
        omap = dict(ScannedDocument=ScannedDocument,
                    NamedDocument=NamedDocument,
                    ClientDocument=ClientDocument,
                    UnassignedDocument=UnassignedDocument)
        return self._serialize_objects(omap)

    def backup_phonecalls(self):
        omap = dict(PhoneCall=PhoneCall, ContactCall=ContactCall,
                    ClientCall=ClientCall)
        return self._serialize_objects(omap)

    def backup_tickets(self):
        omap = dict(Description=Description, Ticket=Ticket,
                    TicketCurrentStatus=TicketCurrentStatus,
                    TicketStatusChange=TicketStatusChange,
                    TicketDocument=TicketDocument)
        return self._serialize_objects(omap)

    def backup_misc(self):
        omap = dict(Description=Description,
                    Address=Address)
        return self._serialize_objects(omap)

    
    # this is for small databases
    def backup_objects(self):
        data = dict()
        for bf in [self.backup_usergroup,
                   self.backup_sitecontent, self.backup_cases,
                   self.backup_clients, self.backup_events,
                   self.backup_contacts, self.backup_documents,
                   self.backup_phonecalls,
                   self.backup_tickets, self.backup_misc]:
            data.update(bf())
        return data

    def backup(self, filename):
        #zipfileobj = file(filename, 'w')
        zipfile = ZipFile(filename, 'w', ZIP_DEFLATED)
        data = self.backup_objects()
        flist = self.backup_files(zipfile)
        data['File'] = flist
        zipfile.writestr('database', Pickle.dumps(data))
        zipfile.close()

    def _set_dbobject(self, dbobject, data):
        for key, value in data.items():
            if key in ['created', 'modified', 'attached',
                       'last_change', 'received', 'changed']:
                value = dtparse(value)
            setattr(dbobject, key, value)

    def restore_files(self, zfile):
        for f in self.session.query(File):
            id = f.id
            filename = 'files/file-%d' % id
            content = zfile.read(filename)
            with transaction.manager:
                f.content = content
                f = self.session.merge(f)
                
            
    def restore(self, filename):
        User.metadata.drop_all()
        User.metadata.create_all()
        zipfile = ZipFile(filename, 'r')
        dbdata = Pickle.loads(zipfile.read('database'))
        with transaction.manager:
            # usergroup objects
            for data in dbdata['User']:
                print "CREATING USER", data
                user = User(data['username'])
                self._set_dbobject(user, data)
                self.session.add(user)
            for data  in dbdata['UserConfig']:
                user_id = data['user_id']
                text = data['text']
                uc = UserConfig(user_id, text)
                self.session.add(uc)
            for data in dbdata['Password']:
                pw = Password(data['user_id'], data['password'])
                self.session.add(pw)
            for data in dbdata['Group']:
                g = Group(data['name'])
                self._set_dbobject(g, data)
                self.session.add(g)
            for data in dbdata['UserGroup']:
                ug = UserGroup(data['group_id'], data['user_id'])
                self.session.add(ug)
            # site content objects
            for data in dbdata['SiteImage']:
                si = SiteImage(data['name'], data['content'])
                self._set_dbobject(si, data)
                self.session.add(si)
            #for data in dbdata['SiteText']:
            #    st = SiteText(data['name'], data['content'])
            #    self._set_dbobject(st, data)
            #    self.session.add(st)
            #########################################
            # mslemon objects
            #########################################
            for data in dbdata['Address']:
                a = Address(data['street'])
                self._set_dbobject(a, data)
                self.session.add(a)
            for data in dbdata['Contact']:
                c = Contact(data['firstname'])
                self._set_dbobject(c, data)
                self.session.add(c)
            for data in dbdata['GlobalContact']:
                gc = GlobalContact(data['id'])
                self.session.add(gc)
            for data in dbdata['Client']:
                c = Client(data['name'], data['contact_id'])
                self._set_dbobject(c, data)
                self.session.add(c)
            for data in dbdata['Event']:
                e = Event(data['title'])
                for dtkey in ['start', 'end', 'created']:
                    setattr(e, dtkey, dtparse(data[dtkey]))
                for dkey in ['start_date', 'end_date']:
                    setattr(e, dkey, dtparse(data[dkey]).date())
                for tkey in ['start_time', 'end_time']:
                    setattr(e, tkey, dtparse(data[tkey]).time())
                for field in ['all_day', 'title', 'description',
                              'created_by_id', 'ext']:
                    setattr(e, field, data[field])
                self.session.add(e)
            for classname in empty_init_objects:
                dbclass = eval(classname)
                for data in dbdata[classname]:
                    dbobj = dbclass()
                    self._set_dbobject(dbobj, data)
                    self.session.add(dbobj)
        self.restore_files(zipfile)
                    
                    
            

    
    
        
        
DBOBJECTS = ['User', 'Group', 'Password',
             'UserGroup', 'UserConfig', 'SiteImage',
             'SiteText', 'Case', 'CaseTicket', 'CaseDocument',
             'CaseUser', 'CaseStatusChange', 'CaseCurrentStatus',
             'CaseEvent', 'Client', 'Event', 'EventUser',
             'Contact', 'ClientContact', 'GlobalContact',
             'GroupContact', 'UserContact', 'File', 'ScannedDocument',
             'UnassignedDocument', 'PhoneCall', 'ContactCall',
             'ClientCall', 'Description', 'Ticket', 'TicketCurrentStatus',
             'TicketStatusChange', 'TicketDocument', 'Address']

