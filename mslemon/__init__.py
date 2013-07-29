import os
from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid_beaker import session_factory_from_settings

from trumpet.config.base import basetemplate, configure_base_layout

from mslemon.security import make_authn_authz_policies, authenticate
from mslemon.models.base import DBSession, Base
from mslemon.config.admin import configure_admin
from mslemon.config.main import configure_consultant

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    # set app name
    appname = 'mslemon'
    # need to use goout root factory for ACL
    root_factory = 'trumpet.resources.RootGroupFactory'
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
    if settings.get('db.populate', False):
        from mslemon.models.main import populate
        from mslemon.models.consultant import populate_ticket_status
        from mslemon.models.main import make_test_data
        Base.metadata.create_all(engine)
        #initialize_sql(engine)
        populate(admin_username)
        #populate_ticket_status()
        make_test_data(DBSession)
        
    # setup authn and authz
    secret = settings['%s.authn.secret' % appname]
    cookie = settings['%s.authn.cookie' % appname]
    timeout = int(settings['%s.authn.timeout' % appname])
    authn_policy, authz_policy = make_authn_authz_policies(
        secret, cookie, callback=authenticate,
        timeout=timeout)
    # create config object
    config = Configurator(settings=settings,
                          root_factory=root_factory,
                          request_factory=request_factory,
                          authentication_policy=authn_policy,
                          authorization_policy=authz_policy)
    session_factory = session_factory_from_settings(settings)
    config.set_session_factory(session_factory)

    configure_base_layout(config)
    configure_admin(config)
    configure_consultant(config)
    config.add_static_view('static',
                           'mslemon:static', cache_max_age=3600)
    ##################################
    # Main Views
    ##################################
    config.add_route('home', '/')
    config.add_view('mslemon.views.main.MainViewer',
                    layout='base',
                    renderer=basetemplate,
                    route_name='home')
    config.add_route('main', '/main/{context}/{id}')
    config.add_view('mslemon.views.main.MainViewer',
                    layout='base',
                    renderer=basetemplate,
                    route_name='main')
    ##################################
    # Login Views
    ##################################
    login_viewer = 'mslemon.views.login.LoginViewer'
    config.add_route('login', '/login')
    config.add_view(login_viewer,
                    renderer=basetemplate,
                    layout='base',
                    route_name='login')
    
    
    config.add_route('logout', '/logout')
    config.add_view(login_viewer,
                    renderer=basetemplate,
                    layout='base',
                    route_name='logout')

    
    # Handle HTTPForbidden errors with a
    # redirect to a login page.
    config.add_view(login_viewer,
                    context='pyramid.httpexceptions.HTTPForbidden',
                    renderer=basetemplate,
                    layout='base')
    ##################################

    ##################################
    # Misc. Views
    ##################################
    config.add_route('blob', '/blob/{filetype}/{id}')
    config.add_view('mslemon.views.blob.BlobViewer', route_name='blob',
                    renderer='string',
                    layout='base')
    
    # wrap app with Fanstatic
    app = config.make_wsgi_app()
    from fanstatic import Fanstatic
    return Fanstatic(app)

