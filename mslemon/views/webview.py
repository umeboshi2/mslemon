from trumpet.views.webview import BaseWebView

class WebView(BaseWebView):
    def __init__(self, request):
        super(WebView, self).__init__(request)
        resources = self.request.root.static_resources
        resources.initialize_webview_layout.need()
        resources.favicon.need()
        
        
