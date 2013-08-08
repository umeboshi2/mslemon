from trumpet.views.base import BaseViewer as TrumpetViewer
from trumpet.views.base import BaseMenu
from trumpet.views.menus import BaseMenu, TopBar

from mslemon.resources import StaticResources
from mslemon.models.usergroup import User

def prepare_layout(layout):
    layout.title = 'Miss Lemon'
    layout.header = layout.title
    layout.subheader = ''
    layout.content = ''
    layout.ctx_menu = BaseMenu(header=' ')
    layout.footer = ''
    layout.resources = StaticResources()
    layout.resources.favicon.need()


def make_main_menu(request):
    bar = TopBar(request.matched_route.name)
    bar.entries['Home'] = request.route_url('home')
    if 'user' in request.session:
        url = request.route_url('consult_phone', context='add', id='somebody')
        bar.entries['Take Call'] = url
        user = request.session['user']
        if 'admin' in user.groups:
            try:
                url = request.route_url('admin', context='main')
                bar.entries['Admin'] = url
            except KeyError:
                pass
    return bar


def make_ctx_menu(request):
    menu = BaseMenu(header='Main Menu', class_='submenu')
    user = request.session.get('user', None)
    logged_in = user is not None
    if logged_in:
        #url = request.route_url('user', context='preferences')
        url = request.route_url('user', context='status')
        menu.append_new_entry('Preferences', url)
    else:
        login_url = request.route_url('login')
        menu.append_new_entry('Sign In', login_url)
    if 'user' in request.session:
        user = request.session['user']
        url = request.route_url('consult_contacts', context='list', id='all')
        menu.append_new_entry('Contacts', url)

        url = request.route_url('consult_clients', context='list', id='all')
        menu.append_new_entry('Clients', url)

        url = request.route_url('consult_calendar', context='list', id='all')
        menu.append_new_entry('Calendar', url)

        url = request.route_url('consult_tickets', context='list', id='all')
        menu.append_new_entry('Tickets', url)

        url = request.route_url('consult_phone', context='list', id='all')
        menu.append_new_entry('Phone Calls', url)

    return menu
    
class BaseViewer(TrumpetViewer):
    def __init__(self, request):
        super(BaseViewer, self).__init__(request)
        prepare_layout(self.layout)
        self.layout.main_menu = make_main_menu(request).render()
        self.css = self.layout.resources.main_screen
        #skey = 'mslemon.admin.admin_username'
        #self.admin_username = self.request.registry.settings[skey]
        #import pdb ; pdb.set_trace()
        
    def __call__(self):
        if hasattr(self, 'css'):
            self.css.need()
        return super(BaseViewer, self).__call__()

    def get_current_user(self):
        db = self.request.db
        user_id = self.request.session['user'].id
        return db.query(User).get(user_id)

class AdminViewer(BaseViewer):
    def __init__(self, request):
        super(AdminViewer, self).__init__(request)
        self.css = self.layout.resources.admin_screen
        
