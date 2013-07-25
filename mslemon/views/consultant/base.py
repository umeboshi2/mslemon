from mslemon.views.base import prepare_layout

def prepare_base_layout(request):
    layout = request.layout_manager.layout
    prepare_layout(layout)
    layout.ctx_menu.set_header(' ')
    if 'user' not in request.session:
        url = request.route_url('login')
        layout.ctx_menu.append_new_entry('Login', url)
    else:
        url = request.route_url('consult_contacts', context='list', id='all')
        layout.ctx_menu.append_new_entry('Contacts', url)

        url = request.route_url('consult_clients', context='list', id='all')
        layout.ctx_menu.append_new_entry('Clients', url)

        url = request.route_url('consult_calendar', context='list', id='all')
        layout.ctx_menu.append_new_entry('Calendar', url)

        url = request.route_url('consult_tickets', context='list', id='all')
        layout.ctx_menu.append_new_entry('Tickets', url)
    #url = request.route_url('view_wiki')
    #layout.ctx_menu.append_new_entry('Wiki', url)
    layout.title = 'Consultant'
    layout.header = 'Consultant'
    layout.subheader = ''
    

    

