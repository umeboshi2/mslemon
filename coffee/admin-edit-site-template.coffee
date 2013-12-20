$(document).ready ->
    # prepare page
    $('#save-content').hide()
    # setup vars and functions
    fresh_edit = (data, status, xhr) ->
        $('#save-content').hide()
        make_alert(status, status)


    # init editor
    editor = ace.edit('editor')
    session = editor.getSession()
    session.on('change', () ->
        $('#save-content').show()
        )
    # set editor mode
    session.setMode('ace/mode/coffee')
    # set editor theme
    editor.setTheme('ace/theme/trumpet')
    editor.setKeyboardHandler('ace/keyboard/emacs')

    button = $ '#keybinding'
    togglefun = TrumpetApp.functions.toggle_ace_keybinding
    togglefun(button, editor)
    

    # click save button
    $('#save-content').click ->
        formdata =
            update: 'submit'
            content: editor.getValue()
        #$(this).hide()
        $.post(window.location, formdata, fresh_edit)
                        
