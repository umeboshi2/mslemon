# Create TrumpetApp as a namespace object
window.TrumpetApp =
    functions: {}
    main_loop: null
        
url_join = () ->
    fix_string = (string) ->
        string = string.replace /[\/]+/g, '/'
        string = string.replace /\:\//g, '://'
        string = string.replace /\/\?/g, '?'
        string = string.replace /\/\#/g, '#'
        return string
        
    joined = [].slice.call(arguments, 0).join('/')
    return fix_string joined
    

make_alert_div = (message, priority) ->
    alert_div = '<div id="main-alert" class="alert alert-#priority# alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>$__replaceme__</div>'
    div = alert_div.replace('$__replaceme__', message)
    div = div.replace('#priority#', priority)
    return div
        
make_alert = (message, priority) ->
    div = make_alert_div(message, priority)
    $('.main-content').prepend(div)


get_template = (name) ->
    prefix = '/blob/ejs/search'
    params = jQuery.param name: name
    url = prefix + '?' + params
    return new EJS({url: url})

toggle_ace_keybinding = (button, editor) ->
    button.click ->
        keybinding = button.text()
        if keybinding == 'emacs'
            button.text 'ace'
            editor.setKeyboardHandler('')
        else
            button.text 'emacs'
            editor.setKeyboardHandler('ace/keyboard/emacs')
                


# attach some functions to TrumpetApp namespace
TrumpetApp.make_alert_div = make_alert_div
TrumpetApp.make_alert = make_alert
TrumpetApp.get_template = get_template
TrumpetApp.functions.url_join = url_join
TrumpetApp.functions.toggle_ace_keybinding = toggle_ace_keybinding


$(document).ready ->
    # hide the status bar
    $('.status-bar').hide()
