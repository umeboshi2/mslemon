import os
from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid_beaker import session_factory_from_settings

from trumpet.config.base import basetemplate, configure_base_layout
from trumpet.models.sitecontent import SitePath

from mslemon.security import make_authn_authz_policies, authenticate
from mslemon.models.base import DBSession, Base
from mslemon.config.admin import configure_admin
from mslemon.config.main import configure_consultant
from mslemon.config.main import configure_mslemon_cases
from mslemon.config.main import configure_mslemon_docs
from mslemon.config.main import configure_wiki

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    # set app name
    appname = 'mslemon'
    from mslemon.resources import RootGroupFactory
    from mslemon.resources import Root, Resource
    from mslemon.resources import ORMContainer
    root_factory = RootGroupFactory
    root_factory = Root
    # alchemy request provides .db method
    request_factory = 'trumpet.request.AlchemyRequest'
    # get admin username
    admin_username = settings.get('mslemon.admin.admin_username', 'admin')
    # create db engine
    engine = engine_from_config(settings, 'sqlalchemy.')
    # setup db.sessionmaker
    settings['db.sessionmaker'] = DBSession
    # bind session to engine
    DBSession.configure(bind=engine)
    # bind objects to engine
    Base.metadata.bind = engine
    from trumpet.models.base import Base as TrumpetBase
    TrumpetBase.metadata.bind = engine
    if settings.get('db.populate', 'False') == 'True':
        from mslemon.models.main import make_test_data
        import mslemon.models.misslemon
        Base.metadata.create_all(engine)
        TrumpetBase.metadata.create_all(engine)
        #initialize_sql(engine)
        #make_test_data(DBSession)
        from mslemon.models.initialize import initialize_database
        from mslemon.models.initialize import IntegrityError
        initialize_database(settings)
    
        
    # setup authn and authz
    secret = settings['%s.authn.secret' % appname]
    cookie = settings['%s.authn.cookie' % appname]
    timeout = int(settings['%s.authn.timeout' % appname])
    authn_policy, authz_policy = make_authn_authz_policies(
        secret, cookie, callback=authenticate,
        timeout=timeout, tkt=False)
    root_factory.authn_policy = authn_policy

    # create config object
    config = Configurator(settings=settings,
                          root_factory=root_factory,
                          request_factory=request_factory,
                          authentication_policy=authn_policy,
                          authorization_policy=authz_policy)
    session_factory = session_factory_from_settings(settings)
    config.set_session_factory(session_factory)

    config.include('pyramid_fanstatic')
    config.include('cornice')

    config.include(configure_base_layout)
    config.include(configure_admin)
    config.include(configure_consultant)
    config.include(configure_mslemon_cases)
    config.include(configure_mslemon_docs)
    configure_wiki(config, '/msl_wiki')
    config.add_static_view('static',
                           'mslemon:static', cache_max_age=3600)
    view_defaults = dict(renderer=basetemplate, layout='base')
    
    ##################################
    # Main Views
    ##################################

    route_name = 'home'
    config.add_route(route_name, '/')
    config.add_view('mslemon.views.main.MainViewer',
                    route_name=route_name, **view_defaults)

    route_name = 'traverse'
    config.add_route(route_name, '/trv/*traverse')
    config.add_view('mslemon.views.main.TraversalViewer',
                    route_name=route_name, **view_defaults)


    route_name = 'test_rest_views'
    config.add_route(route_name, '/rviews/{model}')
    config.add_view('mslemon.views.testrest.TestViewer',
                    route_name=route_name, **view_defaults)

    route_name = 'main'
    config.add_route(route_name, '/main/{context}/{id}')
    config.add_view('mslemon.views.main.MainViewer',
                    route_name=route_name, **view_defaults)

    route_name = 'initdb'
    config.add_route(route_name, '/initdb/{context}/{id}')
    config.add_view('mslemon.views.main.MainViewer',
                    route_name=route_name, **view_defaults)

    ##################################
    # Login Views
    ##################################
    login_viewer = 'mslemon.views.login.LoginViewer'
    route_name = 'login'
    config.add_route(route_name, '/login')
    config.add_view(login_viewer, route_name=route_name, **view_defaults)

    route_name = 'logout'
    config.add_route(route_name, '/logout')
    config.add_view(login_viewer, route_name=route_name, **view_defaults)

    
    # Handle HTTPForbidden errors with a
    # redirect to a login page.
    config.add_view(login_viewer,
                    context='pyramid.httpexceptions.HTTPForbidden',
                    xhr=False,
                    **view_defaults)
    ##################################

    ##################################
    # Misc. Views
    ##################################
    config.add_route('blob', '/blob/{filetype}/{id}')
    config.add_view('mslemon.views.blob.BlobViewer', route_name='blob',
                    renderer='string',
                    layout='base')
    ##################################
    # Views for Users
    ##################################
    route_name = 'user'
    config.add_route(route_name, '/user/{context}')
    config.add_view('mslemon.views.userview.MainViewer',
                    route_name=route_name,
                    permission='user',
                    **view_defaults)
    ##################################
    config.add_view('mslemon.views.webview.WebView', name='webviews')
    
                    
                     
    
    # add REST views
    config.scan('mslemon.views.testrest')
    config.scan('mslemon.views.rest')
    config.scan('trumpet.views.rest.webview')

    
    
    app = config.make_wsgi_app()

    # FIXME: maybe do this somewhere else?
    # wrap app with Fanstatic
    from fanstatic import Fanstatic
    return Fanstatic(app)

