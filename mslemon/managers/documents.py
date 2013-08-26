import os
from datetime import datetime, timedelta

import transaction
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import desc
from sqlalchemy import func

from mslemon.util import datetime_from_pdf_filename
from mslemon.util import get_scanned_filenames

from mslemon.managers.util import convert_range_to_datetime

#FIXME: better module name
from mslemon.models.misslemon import File, ScannedDocument
from mslemon.models.misslemon import NamedDocument, ClientDocument
from mslemon.models.misslemon import UnassignedDocument, NamedDocument
    
    
class ScannedDocumentsManager(object):
    def __init__(self, session):
        self.session = session
        self.directory = None
        
    def query(self):
        q = self.session.query(ScannedDocument)
        return q
    
    def get(self, id):
        return self.query().get(id)

    def set_scans_directory(self, directory):
        self.directory = directory

    def insert_scanned_file(self, filename):
        fullname = os.path.join(self.directory, filename)
        # file must fit in memory
        content = file(fullname).read()
        created = datetime_from_pdf_filename(filename)
        with transaction.manager:
            f = File()
            f.content = content
            self.session.add(f)
            f = self.session.merge(f)
            s = ScannedDocument()
            s.created = created
            s.name = filename
            s.file_id = f.id
            self.session.add(s)
            s = self.session.merge(s)
        return s
    
        
    def get_latest(self):
        q = self.session.query(NamedDocument)
        q = q.order_by(NamedDocument.created.desc())
        latest = q.first()
        if latest is None:
            q = self.session.query(ScannedDocument)
            q = q.order_by(ScannedDocument.created.desc())
            latest = q.first()
        return latest
    
        

    def update_database(self):
        filenames = get_scanned_filenames(self.directory)
        latest = self.get_latest()
        for filename in filenames:
            dt = datetime_from_pdf_filename(filename)
            if latest is None or dt > latest.created:
                self.insert_scanned_file(filename)

    def _range_filter(self, query, start, end):
        query = query.filter(ScannedDocument.created >= start)
        query = query.filter(ScannedDocument.created <= end)
        return query
    
    def get_documents(self, start, end, timestamps=False):
        if timestamps:
            start, end = convert_range_to_datetime(start, end)
        q = self.session.query(ScannedDocument)
        q = self._range_filter(q, start, end)
        return q.all()
    
    def name_document(self, scan_id, name, user_id):
        with transaction.manager:
            s = self.get(scan_id)
            nd = NamedDocument()
            nd.name = name
            nd.file_id = s.file_id
            nd.created = s.created
            nd.created_by_id = user_id
            self.session.add(nd)
            nd = self.session.merge(nd)
            ud = UnassignedDocument()
            ud.doc_id = nd.id
            self.session.add(ud)
            self.session.delete(self.get(scan_id))
        return nd
    
            
    
class DocumentManager(object):
    def __init__(self, session):
        self.session = session
        self.scans = ScannedDocumentsManager(self.session)
        
    def set_scans_directory(self, directory):
        self.scans.set_scans_directory(directory)

    def query(self):
        return self.session.query(NamedDocument)

    def all(self):
        return self.query().all()

    def get_unassigned(self):
        return self.session.query(UnassignedDocument).all()
    
