import string

import colander
import deform
import vobject

from sqlalchemy.exc import IntegrityError

from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound

from mslemon.views.base import prepare_layout
from mslemon.views.base import BaseViewer


from mslemon.managers.contacts import ContactManager

from mslemon.views.consultant.base import prepare_base_layout
from haberdashery.resources import list_contacts

phone_re = '\((?P<areacode>[1-9][0-9][0-9])\)-(?P<prefix>[0-9][0-9][0-9])-(?P<suffix>[0-9][0-9][0-9][0-9])'
letters = string.ascii_letters[26:]

class AddContactSchema(colander.Schema):
    firstname = colander.SchemaNode(
        colander.String(),
        title = 'First Name',
        )
    lastname = colander.SchemaNode(
        colander.String(),
        title = 'Last Name',
        missing=colander.null,
        )
    email = colander.SchemaNode(
        colander.String(),
        validator=colander.Email(),
        title='Email Address',
        missing=colander.null,
        )
    phone = colander.SchemaNode(
        colander.String(),
        title='Phone Number',
        widget=deform.widget.TextInputWidget(mask='(999)-999-9999',
                                      mask_placeholder='0'),
        missing=colander.null,
        )

def prepare_main_layout(request):
    prepare_base_layout(request)
    layout = request.layout_manager.layout
    layout.title = 'Consultant Contacts'
    layout.header = 'Consultant Contacts'
    layout.subheader = 'Contacts Area'
    

def make_vcard(contact):
    card = vobject.vCard()
    card.add('n')
    card.n.value = vobject.vcard.Name(family=contact.lastname,
                                      given=contact.firstname)
    card.add('fn')
    fname = contact.lastname
    if contact.firstname:
        fname = '%s %s' % (contact.firstname, contact.lastname)
    card.fn.value = fname
    card.add('email')
    card.email.type_param = 'INTERNET'
    if contact.email is not None:
        card.email.value = contact.email
    card.add('tel')
    card.tel.type_param = 'WORK'
    if contact.phone is not None:
        card.tel.value = contact.phone
    return card


def parse_vcard_object(card):
    firstname = card.n.value.given
    if not firstname:
        firstname = None
    lastname = card.n.value.family
    email = None
    if hasattr(card, 'email'):
        email = card.email.value
        if not email:
            email = None
    phone = None
    if hasattr(card, 'tel'):
        phone = card.tel.value
        if not phone:
            phone = None
    return firstname, lastname, email, phone

    
class ContactViewer(BaseViewer):
    def __init__(self, request):
        BaseViewer.__init__(self, request)
        prepare_main_layout(self.request)
        self.contacts = ContactManager(self.request.db)
        self._dispatch_table = dict(
            list=self.list_contacts,
            add=self.add_contact,
            delete=self.delete_contact,
            confirmdelete=self.confirm_delete_contact,
            viewcontact=self.view_contact,
            editcontact=self.edit_contact,
            exportcontact=self.export_contact,
            exportall=self.export_all_contacts,
            importcontact=self.import_contact,
            importsubmit=self.import_contact_submit,)
        self.context = self.request.matchdict['context']
        self._view = self.context

        url = self.url(context='add', id='somebody')
        self.layout.ctx_menu.append_new_entry("Add Contact", url)

        url = self.url(context='exportall', id='everybody')
        self.layout.ctx_menu.append_new_entry("Export Contacts", url)

        url = self.url(context='importcontact', id='somebody')
        self.layout.ctx_menu.append_new_entry("Import Contacts", url)
        
        self.dispatch()

    def list_contacts(self):
        contacts = self.contacts.all()
        env = dict(contacts=contacts, letters=letters)
        template = 'mslemon:templates/consult/listcontacts.mako'
        list_contacts.need()
        self.layout.content = self.render(template, env)
        
        
    def add_contact(self):
        schema = AddContactSchema()
        form = deform.Form(schema, buttons=('submit',))
        self.layout.resources.deform_auto_need(form)
        if 'submit' in self.request.POST:
            controls = self.request.POST.items()
            self.layout.subheader = 'Contact Submitted'
            try:
                data = form.validate(controls)
            except deform.ValidationFailure, e:
                self.layout.content = e.render()
                return
            firstname = data['firstname']
            lastname = data.get('lastname')
            if not lastname:
                lastname = None
            email = data.get('email')
            if not email:
                email = None
            phone = data.get('phone')
            if not phone:
                phone = None
            c = self.contacts.add(firstname, lastname, email, phone)
            name = '%s %s' % (c.firstname, c.lastname)
            content = '<p>Contact %s added.</p>' % name
            self.layout.content = content
            return
        rendered = form.render()
        self.layout.content = rendered
        self.layout.subheader = 'Add a Contact'
            
                           
    def edit_contact(self):
        id = int(self.request.matchdict['id'])
        contact = self.contacts.get(id)
        formdata = {}
        for key in ['firstname', 'lastname', 'email', 'phone']:
            formdata[key] = getattr(contact, key)
        
        schema = AddContactSchema()
        form = deform.Form(schema, buttons=('submit',))
        self.layout.resources.deform_auto_need(form)
        if 'submit' in self.request.POST:
            controls = self.request.POST.items()
            self.layout.subheader = 'Contact Submitted'
            try:
                data = form.validate(controls)
            except deform.ValidationFailure, e:
                self.layout.content = e.render()
                return
            firstname = data['firstname']
            lastname = data.get('lastname')
            if not lastname:
                lastname = None
            email = data.get('email')
            if not email:
                email = None
            phone = data.get('phone')
            if not phone or phone == '(000)-000-0000':
                phone = None
            kw = dict(firstname=firstname, lastname=lastname,
                      email=email, phone=phone)
            self.contacts.update(contact, **kw)
            c = self.contacts.get(id)
            name = '%s %s' % (c.firstname, c.lastname)
            content = '<p>Contact %s updated.</p>' % name
            self.layout.content = content
            return
        rendered = form.render(formdata)
        self.layout.content = rendered
        self.layout.subheader = 'Edit Contact %s' % id
        
        
    def delete_contact(self):
        id = self.request.matchdict['id']
        url = self.url(context='confirmdelete', id=id)
        a = '<a href="%s">Confirm Delete</a>' % url
        self.layout.content = a
        

    def confirm_delete_contact(self):
        id = self.request.matchdict['id']
        self.contacts.delete(id)
        #self.layout.content = "Deleted"
        url = self.url(context='list', id='all')
        self.response = HTTPFound(url)
    
    def view_contact(self):
        id = self.request.matchdict['id']
        c = self.contacts.get(id)
        env = dict(c=c)
        template = 'mslemon:templates/consult/viewcontact.mako'
        self.layout.content = self.render(template, env)

    def export_contact(self):
        id = self.request.matchdict['id']
        c = self.contacts.get(id)
        vcf = make_vcard(c)
        r = Response(content_type='text/vcard',
                     body=vcf.serialize())
        if c.firstname is not None:
            name = '%s_%s' % (c.firstname, c.lastname)
        else:
            name = c.lastname
        filename = '%s.vcf' % name
        r.content_disposition = 'attachment; filename="%s"' % filename
        self.response = r


    def export_all_contacts(self):
        stream = ''
        for contact in self.contacts.all():
            stream += make_vcard(contact).serialize()
        r = Response(content_type='text/vcard', body=stream)
        r.content_disposition = 'attachment; filename="AllContacts.vcf"'
        self.response = r

    def import_contact(self):
        env = dict()
        template = 'mslemon:templates/consult/importcontacts.mako'
        self.layout.content = self.render(template, env)
        

    def import_contact_submit(self):
        fname = self.request.POST['vcf'].filename
        ifile = self.request.POST['vcf'].file
        stream = ifile.read()
        count = 0
        excluded = []
        for card in vobject.readComponents(stream):
            cfields = parse_vcard_object(card)
            try:
                self.contacts.add(*cfields)
                count += 1
            except IntegrityError:
                excluded.append(card)
        self.layout.content = "Imported %d cards." % count
        
        
    
        
