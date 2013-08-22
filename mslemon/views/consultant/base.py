from mslemon.views.base import prepare_layout, make_ctx_menu

def prepare_base_layout(request):
    layout = request.layout_manager.layout
    prepare_layout(layout)
    layout.ctx_menu = make_ctx_menu(request).output()
    #url = request.route_url('view_wiki')
    #layout.ctx_menu.append_new_entry('Wiki', url)
    layout.title = 'Consultant'
    layout.header = 'Consultant'
    layout.subheader = ''
    

    

