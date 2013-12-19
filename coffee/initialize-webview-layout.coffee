$(document).ready ->
    #url = document.URL
    webview_id = url.replace(/^.*\/|\.[^.]*$/g, '')
    url = '/rest/webviews/' + webview_id

    layout = {}

    layout_content_retrieved = (data, status, xhr) ->
        if status == 'success'
            layout = data
            
    $.get url, {}, layout_content_retrieved
    
    