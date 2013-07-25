#from pyramid.security import Allow, Everyone, Authenticated
from fanstatic import Library, Resource

from haberdashery.resources import jqueryui, fc_css

#from trumpet.resources import jqueryui
#from trumpet.resources import StaticResources as TrumpetResources

library = Library('mslemon_lib', 'static')
css = Library('mslemon_css', 'static/css')
js = Library('mslemon_js', 'static/js')

