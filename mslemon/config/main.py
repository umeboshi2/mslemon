from trumpet.config.base import basetemplate
from trumpet.config.base import add_view

viewers = dict(contacts='ContactViewer',
               clients='ClientViewer',
               calendar='CalendarViewer',
               tickets='TicketViewer',
               phone='PhoneCallViewer',)

def configure_consultant(config, rootpath='/consult', permission='consultant'):
    config.add_route('consult', rootpath)
    config.add_view('mslemon.views.consultant.main.MainViewer',
                    route_name='consult',
                    renderer=basetemplate,
                    layout='base',
                    permission=permission)
    for route in ['contacts', 'clients', 'calendar', 'tickets', 'phone']:
        route_name = 'consult_%s' % route
        config.add_route(route_name,
                         '%s/%s/{context}/{id}' % (rootpath, route))
        view = 'mslemon.views.consultant.%s.%s' % (route, viewers[route])
        config.add_view(view, route_name=route_name,
                        renderer=basetemplate,
                        layout='base',
                        permission=permission)
    route_name = 'consult_json'
    config.add_route(route_name,
                     '%s/json/{context}/{id}' % rootpath)
    config.add_view('mslemon.views.consultant.json.JSONViewer',
                    route_name=route_name,
                    renderer='json',
                    layout='base',
                    permission=permission)
    route_name = 'consult_frag'
    config.add_route(route_name,
                     '%s/frag/{context}/{id}' % rootpath)
    config.add_view('mslemon.views.consultant.frag.FragViewer',
                    route_name=route_name,
                    renderer='string',
                    layout='base',
                    permission=permission)
    
    

    
                     
    
