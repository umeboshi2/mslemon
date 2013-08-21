from pyramid.security import Allow, Everyone, Authenticated
from fanstatic import Library, Resource

from haberdashery.resources import jqueryui, fc_css, deform_css


#from trumpet.resources import jqueryui
from trumpet.resources import StaticResources as TrumpetResources

library = Library('mslemon_lib', 'static')
css = Library('mslemon_css', 'static/css')
js = Library('mslemon_js', 'static/js')

favicon = Resource(library, 'favicon.ico')

main_screen = Resource(css, 'mainscreen.css', depends=[deform_css])
admin_screen = Resource(css, 'adminscreen.css', depends=[deform_css])


take_call_button = Resource(js, 'take-call-button.js', depends=[jqueryui])
main_phone_view = Resource(js, 'main-phone-view.js', depends=[fc_css])
main_ticket_view = Resource(js, 'main-ticket-view.js', depends=[fc_css])

phone_calendar = Resource(js, 'phone-calendar.js', depends=[fc_css])


class StaticResources(TrumpetResources):
    main_screen = main_screen
    admin_screen = admin_screen
    
    # override trumpet favicon
    favicon = favicon
    

    take_call_button = take_call_button
    main_phone_view = main_phone_view
    main_ticket_view = main_ticket_view
    
    phone_calendar = phone_calendar
    

# the acl entries are allow/deny, group, permission
class RootGroupFactory(object):
    __name__ = ""
    __acl__ = [
        (Allow, Everyone, 'public'),
        (Allow, Authenticated, 'user'),
        (Allow, Authenticated, 'consultant'),
        (Allow, 'manager', 'manage'),
        (Allow, 'admin', ('admin', 'manage')),
        ]

    def __init__(self, request):
        # comment
        pass


