from trumpet.views.base import BaseViewer as TrumpetViewer
from trumpet.views.base import BaseMenu
from trumpet.views.menus import BaseMenu, TopBar

from mslemon.resources import StaticResources
from mslemon.models.usergroup import User

from mslemon.views.util import prepare_user_menu, prepare_layout
from mslemon.views.util import get_admin_username, get_user_id
from mslemon.views.util import get_regular_users



def make_main_menu(request):
    menu = BaseMenu(header='Main Menu', class_='submenu')
    user = request.session.get('user', None)
    logged_in = user is not None
    if 'user' in request.session:
        user = request.session['user']
        url = request.route_url('view_wiki')
        menu.append_new_entry('Wiki', url)
        
        url = request.route_url('consult_contacts', context='list', id='all')
        menu.append_new_entry('Contacts', url)

        url = request.route_url('consult_clients', context='list', id='all')
        menu.append_new_entry('Clients', url)

        url = request.route_url('consult_calendar', context='list', id='all')
        menu.append_new_entry('Calendar', url)

        url = request.route_url('msl_tickets', context='main', id='all')
        menu.append_new_entry('Tickets', url)

        url = request.route_url('msl_phonecalls', context='main', id='all')
        menu.append_new_entry('Phone Calls', url)

        url = request.route_url('msl_docs', context='main', id='all')
        menu.append_new_entry('Documents', url)

        url = request.route_url('msl_cases', context='main', id='all')
        menu.append_new_entry('Cases', url)

        url = request.route_url('test_rest_views', model='sitetext')
        menu.append_new_entry('test backbone', url)
        
    return menu
    
class BaseViewer(TrumpetViewer):
    def __init__(self, request):
        super(BaseViewer, self).__init__(request)
        prepare_layout(self.layout)
        self.layout.user_menu = prepare_user_menu(request)
        self.css = self.layout.resources.main_screen
        self.layout.brand = 'Miss Lemon'
        
    def __call__(self):
        if hasattr(self, 'css'):
            if self.css is not None:
                self.css.need()
        return super(BaseViewer, self).__call__()

    def get_admin_username(self):
        return get_admin_username(self.request)

    def is_admin_authn(self, authn):
        username = self.get_admin_username()
        user_id = get_user_id(self.request, username)
        return authn == user_id

    def get_current_user(self):
        user_id = self.get_current_user_id()
        return self.request.db.query(User).get(user_id)
    

    
class AdminViewer(BaseViewer):
    def __init__(self, request):
        super(AdminViewer, self).__init__(request)
        self.css = self.layout.resources.admin_screen
        
