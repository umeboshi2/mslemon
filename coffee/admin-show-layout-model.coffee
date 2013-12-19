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
    add_new_field_button = $ '.add-field-button'
        
        
    model_field_url = (model_id, field_id) ->
            url = '/rest/admin/layoutmodels/' + model_id
            url = url + '/fields/' + field_id
            return url

    header_template = renderable (content) ->
        div '.btn.btn-default.btn-xs', ->
            text content

    editor_template = renderable (field_id) ->
        div "field-id": field_id, '#edit-status', ->
            text 'Editing field'
            div '#save-content.action-button', ->
                text 'Save'
            div '#cancel-button.action-button.pull-right', ->
                text 'Cancel'
            div '#field-editor'
        
    select_field_widget = renderable (fields) ->
        classes = '.listview-entry.action-button.add-this-field'
        div '#select-fields.listview-list', ->
            for field in fields
                fid = '#field-' + field.id
                divid = fid + classes
                div divid, ->
                    text field.name


    field_for_model_selected = (response) ->
        $('#select-fields').remove()                        
        window.location.reload()

    select_fields_for_model = (response) ->
        fields = response.data
        html = select_field_widget fields
        $('.header').append html
        $('.add-this-field').click ->
            btnid = $(this).attr 'id'
            elist = btnid.split '-'
            field_id = elist[1]
            model_id = $('input[name=model_id]').val()
            $('.header').html model_id + '-' + field_id
            url = '/rest/admin/layoutmodels/' + model_id
            url = url + '/fields'
            data = {field_id: field_id}
            request = $.post url, data, field_for_model_selected, 'json'
                        

    create_editor = (model_id, field_id, ftype) ->
        html = editor_template field_id
        editing_space.html html
        field_list.hide()
        add_new_field_button.hide()
        editing_space.show()
                        
        save_button = $ '#save-content'
        save_button.hide()
        cancel_button = $ '#cancel-button'
        cancel_button.click ->
            window.location.reload()
            
                
        editor = ace.edit('field-editor')
        TrumpetApp.editor = editor
        session = editor.getSession()
        session.on('change', () ->
            save_button.show()
            )
        if ftype == 'html'
            session.setMode('ace/mode/html')
        else if ftype == 'teacup'
            session.setMode('ace/mode/coffee')
            session.setTabSize(4)
        editor.setTheme('ace/theme/twilight')

        url = model_field_url(model_id, field_id)
        content_callback = (data, status, xhr) ->
            if status == 'success'
                window.rdata = data
                if data.content != null
                    editor.setValue data.content
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
                content: editor.getValue()
                model_id: model_id
                field_id: field_id
            url = '/rest/admin/layoutmodels/'
            url = url + model_id + '/fields/' + field_id

            $.ajax url,
                type: 'PUT'
                data: formdata
                success: fresh_edit
                error: save_edit_error
                dataType: 'json'
                                
                        
                                
                
    add_new_field_button.click ->
        model_id = $('input[name=model_id]').val()
        url = '/rest/admin/layoutfields'
        request = $.get url, {}, select_fields_for_model, 'json'
                
                                        

    $('.edit-button').click ->
        btnid = $(this).attr('id')
        elist = btnid.split('-')
        field_id = elist[1]
        model_id = $('input[name=model_id]').val()
        oldtext = $('.header').text()
        ftype = $(this).attr('field-type')
        create_editor model_id, field_id, ftype
                
        if TrumpetApp.editor != null
            TrumpetApp.editor.destroy()

        if oldtext == 'Ms. Lemon'
            $('.header').html header_template('FOoo-' + id)
        else
            $('.header').html header_template('Ms. Lemon')

                
    $('.delete-button').click ->
        model_id = $('input[name=model_id]').val()
        btnid = $(this).attr('id')
        elist = btnid.split('-')
        id = elist[1]
        field_id = id
        oldtext = $('.header').text()
        if oldtext == 'Ms. Lemon'
            $('.header').html header_template('Delete-' + id)
        else
            $('.header').html header_template('Ms. Lemon')
    
        formdata =
            update: 'submit'
            model_id: model_id
            field_id: field_id
        url = '/rest/admin/layoutmodels/'
        url = url + model_id + '/fields/' + field_id

        delete_field_success = (data, status, xhr) ->
            window.location.reload()
            
        $.ajax url,
            type: 'DELETE'
            data: formdata
            success: delete_field_success
            dataType: 'json'
        
    # do stuff
    editing_space.hide()

        