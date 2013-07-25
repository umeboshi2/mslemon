import transaction
from sqlalchemy.orm.exc import NoResultFound
import deform

from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.security import remember, forget

from trumpet.models.usergroup import User, Password
from trumpet.views.menus import BaseMenu
from trumpet.views.forms import LoginSchema
from trumpet.views.login import check_login_form



from mslemon.models.base import DBSession
from mslemon.views.base import BaseViewer




class LoginViewer(BaseViewer):
    def __init__(self, request):
        super(LoginViewer, self).__init__(request)
        self.route = self.request.matched_route.name
        self.came_from = self.request.route_url(self.route,
                                                **request.matchdict)
        self.dbsession = DBSession()
        self.css = self.layout.resources.screen
        # simple dispatch for this viewer
        if self.route == 'logout':
            self.logout_view()
        elif self.route == 'login':
            self.login_view()
        else:
            self.login_view()
    
            
    def _base_form_view(self, formdata=None):
        schema = LoginSchema()
        form = deform.Form(schema, buttons=('login',))
        if self.came_from == self.request.route_url('login'):
            self.came_from = self.request.route_url('home')
        if formdata is None:
            formdata = dict(came_from=self.came_from)
        rendered = form.render(formdata)
        self.layout.content = rendered
        self.layout.resources.deform_auto_need(form)
        
    def _login_submitted(self):
        schema = LoginSchema()
        form = deform.Form(schema, buttons=('login',))
        self.layout.resources.deform_auto_need(form)
        controls = self.request.POST.items()
        try:
            data = form.validate(controls)
        except deform.ValidationFailure, e:
            self.layout.content = e.render()
            return
        if check_login_form(self.request):
            username = data['username']
            came_from = data['came_from']
            headers = remember(self.request, username)
            self.response = HTTPFound(location=came_from, headers=headers)
        else:
            self._base_form_view(formdata=data)
            message = "Login Failed. Try again."
            self.layout.subheader = message

    def login_view(self):
        if 'login' in self.request.params:
            self._login_submitted()
        else:
            self._base_form_view()

    def logout_view(self):
        headers = forget(self.request)
        if 'user' in self.request.session:
            del self.request.session['user']
        while self.request.session.keys():
            key = self.request.session.keys()[0]
            del  self.request.session[key]
        location = self.request.route_url('home')
        self.response = HTTPFound(location=location, headers=headers)
