from trumpet.views.base import BaseViewer as TrumpetViewer
from trumpet.views.base import BaseMenu

from mslemon.resources import StaticResources

def prepare_layout(layout):
    layout.title = 'Miss Lemon'
    layout.header = layout.title
    layout.subheader = ''
    layout.content = ''
    layout.ctx_menu = BaseMenu(header='Base Menu')
    layout.footer = ''
    layout.resources = StaticResources()
    layout.resources.favicon.need()

class BaseViewer(TrumpetViewer):
    def __init__(self, request):
        super(BaseViewer, self).__init__(request)
        prepare_layout(self.layout)
        self.css = self.layout.resources.main_screen

    def __call__(self):
        if hasattr(self, 'css'):
            self.css.need()
        return super(BaseViewer, self).__call__()

