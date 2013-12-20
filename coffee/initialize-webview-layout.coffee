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

    check_timeout = 200
    check_for_mainloop_one = () ->
        if TrumpetApp.main_loop == null
            window.setTimeout(check_for_mainloop_two, check_timeout)
        else
            TrumpetApp.main_loop()

    check_for_mainloop_two = () ->
        if TrumpetApp.main_loop == null
            window.setTimeout(check_for_mainloop_one, check_timeout)
        else
            TrumpetApp.main_loop()
    


    layout_content_retrieved = (data, status, xhr) ->
        if status == 'success'
            layout = data
            TrumpetApp.LayoutModel = layout
            window.WVlayout = layout
            CoffeeScript.run layout.template.content
            template = TrumpetApp.LayoutTemplate
            html = template layout.model
            $('body').html html
            window.setTimeout(check_for_mainloop_one, check_timeout)
    $.get url, {}, layout_content_retrieved
    
    
    