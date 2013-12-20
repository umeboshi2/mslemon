from trumpet.views.webview import BaseWebView

from trumpet.managers.admin.sitewebview import SiteWebviewManager

class WebView(BaseWebView):
    def __init__(self, request):
        super(WebView, self).__init__(request)
        resources = self.request.root.static_resources
        resources.initialize_webview_layout.need()
        resources.favicon.need()
        resources.fullcalendar.need()
        resources.backbone.need()
        # ace stuff
        ace = resources.ace
        ace.ace.need()
        ace.keybinding_emacs.need()
        ace.worker_css.need()
        ace.worker_javascript.need()
        ace.worker_coffee.need()
        ace.mode_css.need()
        ace.mode_coffee.need()
        ace.mode_html.need()
        ace.mode_scss.need()
        resources.ace_theme_trumpet.need()
        
        
