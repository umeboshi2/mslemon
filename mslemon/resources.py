from pyramid.security import Allow, Everyone, Authenticated
from fanstatic import Library, Resource

from haberdashery.resources import jqueryui, fullcalendar, deform_css
from haberdashery.resources import ace

#from trumpet.resources import jqueryui
from trumpet.resources import StaticResources as TrumpetResources

library = Library('mslemon_lib', 'static')
css = Library('mslemon_css', 'static/css')
js = Library('mslemon_js', 'static/js')

favicon = Resource(library, 'favicon.ico')

main_screen = Resource(css, 'mainscreen.css', depends=[deform_css])
admin_screen = Resource(css, 'adminscreen.css', depends=[deform_css])


post_to_url = Resource(js, 'post2url.js', depends=[jqueryui])

take_call_button = Resource(js, 'take-call-button.js', depends=[jqueryui])
main_phone_view = Resource(js, 'main-phone-view.js', depends=[fullcalendar])
main_ticket_view = Resource(js, 'main-ticket-view.js', depends=[fullcalendar])
main_cases_view = Resource(js, 'main-cases-view.js', depends=[fullcalendar])
main_scandoc_view = Resource(js, 'main-scandoc-view.js', depends=[fullcalendar])
main_calendar_view = Resource(js, 'main-calendar-view.js', depends=[fullcalendar])
planevent_calendar_view = Resource(js, 'planevent-calendar-view.js',
                                   depends=[fullcalendar, post_to_url])

phone_calendar = Resource(js, 'phone-calendar.js', depends=[fullcalendar])

admin_show_path_content = Resource(js, 'admin-show-path-content.js',
                                   depends=[jqueryui])

admin_list_site_paths = Resource(js, 'list-site-paths.js', depends=[jqueryui])
admin_list_site_resources = Resource(js, 'admin-list-site-resources.js',
                                     depends=[jqueryui])
admin_edit_site_resources = Resource(js, 'admin-edit-site-resources.js',
                                     depends=[ace.ace, jqueryui])


class StaticResources(TrumpetResources):
    main_screen = main_screen
    admin_screen = admin_screen
    
    # override trumpet favicon
    favicon = favicon
    

    main_calendar_view = main_calendar_view
    take_call_button = take_call_button
    planevent_calendar_view = planevent_calendar_view
    main_phone_view = main_phone_view
    main_ticket_view = main_ticket_view
    main_cases_view = main_cases_view
    main_scandoc_view = main_scandoc_view
    
    phone_calendar = phone_calendar
    admin_list_site_paths = admin_list_site_paths
    admin_show_path_content = admin_show_path_content
    admin_list_site_resources = admin_list_site_resources
    admin_edit_site_resources = admin_edit_site_resources
    
    post_to_url = post_to_url
    
# the acl entries are allow/deny, group, permission
class RootGroupFactory(object):
    __name__ = ""
    __acl__ = [
        (Allow, Everyone, 'public'),
        (Allow, Authenticated, 'user'),
        (Allow, Authenticated, 'consultant'),
        (Allow, 'manager', 'manage'),
        (Allow, 'editor', ('wiki_add', 'wiki_edit')),
        (Allow, 'admin', ('admin', 'manage')),
        ]

    def __init__(self, request):
        # comment
        pass


