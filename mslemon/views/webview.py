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
        #resources.require.need()
        #resources.require.main.need()
        
        
