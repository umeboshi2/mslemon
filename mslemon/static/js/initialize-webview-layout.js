// Generated by CoffeeScript 1.6.3
(function() {
  $(document).ready(function() {
    var layout, layout_content_retrieved, url, webview_id;
    webview_id = url.replace(/^.*\/|\.[^.]*$/g, '');
    url = '/rest/webviews/' + webview_id;
    layout = {};
    layout_content_retrieved = function(data, status, xhr) {
      if (status === 'success') {
        return layout = data;
      }
    };
    return $.get(url, {}, layout_content_retrieved);
  });

}).call(this);
