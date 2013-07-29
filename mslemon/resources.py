from pyramid.security import Allow, Everyone, Authenticated
from fanstatic import Library, Resource

from haberdashery.resources import jqueryui, fc_css

#from trumpet.resources import jqueryui
from trumpet.resources import StaticResources as TrumpetResources

library = Library('mslemon_lib', 'static')
css = Library('mslemon_css', 'static/css')
js = Library('mslemon_js', 'static/js')

favicon = Resource(library, 'favicon.ico')

main_screen = Resource(css, 'mainscreen.css')
admin_screen = Resource(css, 'adminscreen.css')

phone_calendar = Resource(js, 'phone-calendar.js', depends=[fc_css])


class StaticResources(TrumpetResources):
    main_screen = main_screen
    admin_screen = admin_screen
    
    # override trumpet favicon
    favicon = favicon
    

    phone_calendar = phone_calendar
    

# the acl entries are allow/deny, group, permission
class RootGroupFactory(object):
    __name__ = ""
    __acl__ = [
        (Allow, Everyone, 'public'),
        (Allow, Authenticated, 'user'),
        (Allow, 'manager', 'manage'),
        (Allow, 'admin', ('admin', 'manage')),
        (Allow, 'manager', ('wiki_add', 'wiki_edit')),
        (Allow, 'admin', ('wiki_add', 'wiki_edit')),
        (Allow, 'manager', 'consultant'),
        (Allow, 'admin', 'consultant'),
        ]

    def __init__(self, request):
        # comment
        pass


