from pyramid.security import Allow, Everyone, Authenticated
from fanstatic import Library, Resource

from haberdashery.resources import jqueryui, fullcalendar
from haberdashery.resources import ace
from haberdashery.resources import bootstrap
from haberdashery.resources import create_js
from haberdashery.resources import backbone
from haberdashery.resources import teacup
from haberdashery.resources import font_awesome_css

from haberdashery.resources import ejs
from haberdashery.resources import backbone_relational
from haberdashery.resources import supermodel


#from trumpet.resources import jqueryui
from trumpet.resources import StaticResources as TrumpetResources

library = Library('mslemon_lib', 'static')
css = Library('mslemon_css', 'static/css')
js = Library('mslemon_js', 'static/js')

LIBRARY_MAP = dict(css=css, js=js, libs=library)

def _get_type(filename):
    if filename.endswith('.js'):
        marker = '.js'
    elif filename.endswith('.css'):
        marker = '.css'
    else:
        raise RuntimeError, "Bad filename %s" % filename
    return marker

def minfilename(filename, marker=None):
    if marker is None:
        marker = _get_type(filename)
    prefix = filename.split(marker)[0]
    return '%s.min%s' % (prefix, marker)

def make_resource(filename, depends=None):
    ftype = _get_type(filename)
    minified = minfilename(filename, marker=ftype)
    lib = LIBRARY_MAP[ftype[1:]]
    if depends is None:
        return Resource(lib, filename, minified=minified)
    else:
        return Resource(lib, filename, minified=minified,
                        depends=depends)

favicon = Resource(library, 'favicon.ico')

main_screen = make_resource('mainscreen.css',
                           depends=[bootstrap.bootstrap_js])

admin_screen = make_resource('adminscreen.css',
                             depends=[bootstrap.bootstrap_js])

post_to_url = make_resource('post2url.js', depends=[jqueryui])


common_page = make_resource('common-page.js', depends=[font_awesome_css,
                                                       jqueryui,
                                                       bootstrap.bootstrap_js,
                                                       ejs,
                                                       teacup,])

take_call_button = make_resource('take-call-button.js', depends=[jqueryui])
main_phone_view = make_resource('main-phone-view.js', depends=[fullcalendar])
main_ticket_view = make_resource('main-ticket-view.js', depends=[fullcalendar])
main_cases_view = make_resource('main-cases-view.js', depends=[fullcalendar])
main_scandoc_view = make_resource('main-scandoc-view.js',
                                  depends=[fullcalendar])
main_calendar_view = make_resource('main-calendar-view.js',
                                   depends=[fullcalendar])
planevent_calendar_view = make_resource('planevent-calendar-view.js',
                                        depends=[fullcalendar, post_to_url])


#phone_calendar = Resource(js, 'phone-calendar.js', depends=[fullcalendar])
phone_calendar = make_resource('phone-calendar.js', depends=[fullcalendar])


create_ui_theme = Resource(library, 'themes/create-ui/css/create-ui.css',
                           depends=[create_js])

midgard_notify = Resource(library,
                          'themes/midgard-notifications/midgardnotif.css',
                          depends=[create_ui_theme])

midgard_tags = Resource(library,
                        'themes/midgard-tags/tags.css',
                        depends=[create_js])

insert_image = Resource(library,
                        'themes/insertimage.css',
                        depends=[create_js])

edit_wiki_page_deps = [midgard_notify, midgard_tags,
                       insert_image]

edit_wiki_page = make_resource('edit-wiki-page.js',
                               depends=edit_wiki_page_deps)

test_backbone = make_resource('test-backbone.js',
                              depends=[backbone])

class StaticResources(TrumpetResources):
    main_screen = main_screen
    admin_screen = admin_screen
    
    # override trumpet favicon
    favicon = favicon
    
    common_page = common_page

    main_calendar_view = main_calendar_view
    take_call_button = take_call_button
    planevent_calendar_view = planevent_calendar_view
    main_phone_view = main_phone_view
    main_ticket_view = main_ticket_view
    main_cases_view = main_cases_view
    main_scandoc_view = main_scandoc_view
    
    phone_calendar = phone_calendar
    edit_wiki_page = edit_wiki_page
    
    post_to_url = post_to_url

    test_backbone = test_backbone


    
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



#####################################################
#####################################################
# New resource system for traversal and sqlalchemy
# Modified from cookbook:
# http://docs.pylonsproject.org/projects/pyramid_cookbook/en/latest/routing/traversal_sqlalchemy.html
#
#####################################################
#####################################################

class Resource(dict):
    def __init__(self, name, parent):
        self.__name__ = name
        self.__parent__ = parent

class Root(Resource):
    "The root resource."
    static_resources = StaticResources()
    __default_acl__ = [
        (Allow, Everyone, 'public'),
        (Allow, Authenticated, 'user'),
        (Allow, Authenticated, 'consultant'),
        (Allow, 'manager', 'manage'),
        (Allow, 'editor', ('wiki_add', 'wiki_edit')),
        (Allow, 'admin', ('admin', 'manage')),
        ]

    @property
    def __acl__(self):
        return self.__default_acl__
    

    def add_resource(self, name, orm_class):
        self[name] = ORMContainer(name, self, self.request, orm_class)

    def __init__(self, request):
        self.request = request
        from mslemon.models.usergroup import User
        self.add_resource('users2', User)
        self['main2'] = dict()
        #self['admin'] = dict(main='foobar')
        self['views'] = Resource('webviews', self)
        #self['views']['webviews'] = Resource('app', self['views'])
        #v = self['views']
        #import pdb ; pdb.set_trace()
        
        
        

    #def __getitem__(self, key):
    #    if key == 'webviews':
    #        print self.request.subpath
    #    else:
    #        return super(Root, self).__getitem__(key)
    
        
        
    
    

class ORMContainer(dict):
    """Traversal component tied to a SQLAlchemy ORM class.

    Calling .__getitem__ fetches a record as an ORM instance, adds certain
    attributes to the object, and returns it.
    """
    def __init__(self, name, parent, request, orm_class):
        self.__name__ = name
        self.__parent__ = parent
        self.request = request
        self.db = request.db
        self.orm_class = orm_class

    def __getitem__(self, key):
        try:
            key = int(key)
        except ValueError:
            raise KeyError(key)
        obj = self.db.query(self.orm_class).get(key)
        if obj is None:
            raise KeyError(key)
        obj.__name__ = key
        obj.__parent__ = self
        return obj
    

