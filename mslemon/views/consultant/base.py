from mslemon.views.base import prepare_layout
from mslemon.views.base import make_main_menu

def prepare_base_layout(request):
    layout = request.layout_manager.layout
    prepare_layout(layout)
    layout.main_menu = make_main_menu(request)
    #url = request.route_url('view_wiki')
    #layout.ctx_menu.append_new_entry('Wiki', url)
    layout.title = 'Consultant'
    layout.header = 'Consultant'
    layout.subheader = ''
    

    

