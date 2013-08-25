import transaction
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import desc


from mslemon.models.misslemon import Contact

class ContactManager(object):
    def __init__(self, session):
        self.session = session
        self.base = Contact
        
    def query(self):
        return self.session.query(Contact)

    def get(self, id):
        return self.query().get(id)

    def add(self, firstname, lastname=None, email=None, phone=None):
        with transaction.manager:
            c = Contact(firstname, lastname, email, phone)
            self.session.add(c)
        return self.session.merge(c)

    def update(self, contact, **kw):
        with transaction.manager:
            for key in kw:
                setattr(contact, key, kw[key])
            contact = self.session.merge(contact)
        return contact

    def delete(self, id):
        with transaction.manager:
            contact = self.get(id)
            if contact is not None:
                self.session.delete(contact)

    def all(self):
        return self.query().all()

    
