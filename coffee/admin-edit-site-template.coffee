$(document).ready ->
        # prepare page
        $('#save-content').hide()
        # setup vars and functions
        fresh_edit = (data, status, xhr) ->
                $('#save-content').hide()
                make_alert(status, status)


        # init editor
        editor = ace.edit('editor')
        editor.getSession().on('change', () ->
                $('#save-content').show()
                )
        # set editor mode
        editor.getSession().setMode('ace/mode/ejs')
        # set editor theme
        editor.setTheme('ace/theme/twilight')

        # click save button
        $('#save-content').click ->
                formdata =
                        update: 'submit'
                        content: editor.getValue()
                $(this).hide()
                $.post(window.location, formdata, fresh_edit)
                        
