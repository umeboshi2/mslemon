$(document).ready ->
    url = document.URL
    webview_id = url.replace(/^.*\/|\.[^.]*$/g, '')
    url = '/rest/webviews/' + webview_id

    layout = {}

    handle_teacup_field = (fieldname) ->
        field = TrumpetApp.LayoutModel.model.fields[fieldname]
        CoffeeScript.run(field.content)
        template = TrumpetApp.CurrentLayoutTemplate
        html = template field
        TrumpetApp.CurrentLayoutTemplate = null
        return html
    TrumpetApp.handle_teacup_field = handle_teacup_field
    TrumpetApp.CurrentLayoutTemplate = null
    

    layout_content_retrieved = (data, status, xhr) ->
        if status == 'success'
            layout = data
            TrumpetApp.LayoutModel = layout
            window.WVlayout = layout
            CoffeeScript.run layout.template
            template = TrumpetApp.LayoutTemplate
            html = template layout.model
            $('body').html html
    $.get url, {}, layout_content_retrieved
    
    