from trumpet.views.menus import BaseMenu

from mslemon.resources import StaticResources
from mslemon.models.usergroup import User

def prepare_user_menu(request):
    user = None
    menu = BaseMenu()
    if 'user' in request.session and request.session['user']:
        user = request.session['user']
    header = 'Guest User'
    if user is not None:
        header = user.username
    menu = BaseMenu(header=header)
    if user is not None:
        url = request.route_url('user', context='status')
        menu.append_new_entry('Preferences', url)
        if 'admin' in user.groups:
            #url = request.route_url('admin', context='main')
            url = request.route_url('admin', resource='main', traverse=[])
            menu.append_new_entry('Admin', url)
        url = request.route_url('logout')
        menu.append_new_entry('Log Out', url)
    else:
        login_url = request.route_url('login')
        menu.append_new_entry('Sign In', login_url)
    return menu

def prepare_layout(layout):
    layout.title = 'Ms. Lemon'
    layout.header = layout.title
    layout.resources = StaticResources()
    layout.resources.favicon.need()
    layout.resources.common_page.need()

def prepare_plain_layout(layout):
    layout.title = 'Ms. Lemon'
    layout.header = layout.title
    layout.resources = StaticResources()
    layout.resources.favicon.need()

    
def get_admin_username(request):
    skey = 'frenchhorn.admin.admin_username'
    admin_username = request.registry.settings.get(skey, 'admin')
    return admin_username

def get_user_id(request, username):
    db = request.db
    q = db.query(User).filter_by(username=username)
    return q.one().id

def get_regular_users(request):
    users = request.db.query(User).all()
    admin_username = get_admin_username(request)
    return [u for u in users if u.username != admin_username]


