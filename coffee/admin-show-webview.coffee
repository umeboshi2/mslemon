$(document).ready ->
    #ab = $ '.action-button'
    #ab.text 'Action Button'
    renderable = teacup.renderable

    div = teacup.div
    icon = teacup.i
    strong = teacup.strong
    span = teacup.span
    label = teacup.label
    input = teacup.input
        
    text = teacup.text

    editing_space = $ '.editing-space'
    field_list = $ '.field-list'
    webview_id = $('input[name=webview_id]').val()
        
        
    model_field_url = (model_id, field_id) ->
            url = '/rest/admin/layoutmodels/' + model_id
            url = url + '/fields/' + field_id
            return url

    header_template = renderable (content) ->
        div '.btn.btn-default.btn-xs', ->
            text content

    editor_template = renderable () ->
        div '#edit-status.listview-header', ->
            text 'Editing template'
            div '#save-content.action-button', ->
                text 'Save'
            div '#cancel-button.action-button.pull-right', ->
                text 'Cancel'
        div '#editor'
            
    create_editor = (webview_id) ->
        html = editor_template
        editing_space.html html
        #field_list.hide()
        editing_space.show()
                        
        save_button = $ '#save-content'
        save_button.hide()
        cancel_button = $ '#cancel-button'
        cancel_button.click ->
            window.location.reload()
            
                
        editor = ace.edit('editor')
        TrumpetApp.editor = editor
        session = editor.getSession()
        session.on('change', () ->
            save_button.show()
            )
        session.setMode('ace/mode/coffee')
        session.setTabSize(4)
        editor.setTheme('ace/theme/trumpet')
        #editor.setTheme('ace/theme/merbivore')
        url = '/rest/admin/webviews/' + webview_id
        content_callback = (data, status, xhr) ->
            if status == 'success'
                window.rdata = data
                if data.template != null
                    editor.setValue data.template
                    save_button.hide()
                    
        response = $.get url, {}, content_callback
        
                
        fresh_edit = (data, status, xhr) ->
            if status == 'success'
                save_button.hide()
        
            TrumpetApp.rdata = data
            TrumpetApp.rstatus = status
            TrumpetApp.rxhr = xhr

        save_edit_error = (data, status, xhr) ->
            TrumpetApp.rdata = data
            TrumpetApp.rstatus = status
            TrumpetApp.rxhr = xhr
            TrumpetApp.make_alert("Error in save")
                                                
        save_button.click ->
            formdata =
                update: 'submit'
                template: editor.getValue()
            url = '/rest/admin/webviews/' + webview_id

            $.ajax url,
                type: 'PUT'
                data: formdata
                success: fresh_edit
                error: save_edit_error
                dataType: 'json'
                                
                        
                                
    # do stuff
    #editing_space.hide()
    create_editor webview_id
    
        