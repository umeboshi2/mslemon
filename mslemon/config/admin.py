from trumpet.config.base import basetemplate
from trumpet.config.base import add_view

main_view = 'mslemon.views.admin.main.MainViewer'

def configure_admin(config, rootpath='/admin', permission='admin'):
    config.add_route('admin', '%s/*traverse' % rootpath,
                     factory='mslemon.views.admin.main.admin_root_factory')
    add_view(config, main_view, 'admin', permission=permission)

    
def configure_adminOrig(config, rootpath='/admin', permission='admin'):
    config.add_route('admin', rootpath)
    add_view(config, main_view, 'admin', permission=permission)
    config.add_route('admin_images', '%s/images/{context}/{id}' % rootpath)
    add_view(config, 'mslemon.views.admin.images.ImageManagementViewer',
             'admin_images', permission=permission)
    config.add_route('admin_sitetext', '%s/sitetext/{context}/{id}' % rootpath)
    add_view(config, 'mslemon.views.admin.sitetext.SiteTextViewer',
             'admin_sitetext', permission=permission)
    config.add_route('admin_users', '%s/users/{context}/{id}' % rootpath)
    add_view(config, 'mslemon.views.admin.users.UserManagementViewer',
               'admin_users', permission=permission)
    route_name = 'admin_dbadmin'
    config.add_route(route_name, '%s/dbadmin/{context}/{id}' % rootpath)
    add_view(config, 'mslemon.views.admin.dbadmin.DBAdminViewer',
              route_name, permission=permission)
    
    route = 'admin_site_templates'
    config.add_route(route, '%s/sitetemplates/{context}/{id}' % rootpath)
    add_view(config, 'mslemon.views.admin.templatemgr.MainViewer',
             route, permission=permission)
    
    route = 'admin_sitecontent_mgr'
    config.add_route(route, '%s/sitecontentmgr/{context}/{id}' % rootpath)
    add_view(config, 'mslemon.views.admin.contentmgr.MainViewer',
             route, permission=permission)
    
