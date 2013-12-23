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

ace_editor_resource_urls = (prefix) ->
    resources =
        ace: url_join prefix, 'ace.js'
        emacs: url_join prefix, 'keybinding-emacs.js'
        modes:
            coffee: url_join prefix, 'mode-coffee.js'
            css: url_join prefix, 'mode-css.js'
            html: url_join prefix, 'mode-html.js'
            scss: url_join prefix, 'mode-scss.js'
        workers:
            coffee: url_join prefix, 'worker-coffee.js'
            css: url_join prefix, 'worker-css.js'
            javascript: url_join prefix, 'worker-javascript.js'
    return resources
    

make_javacript_tag = (url) ->
    tag = teacup.renderable ->
        teacup.script type:'text/javascript', src:url
    return tag()
    
    
load_ace_editor_resources = (mode) ->
    prefix = '/fanstatic/js.ace'
    trumpet_theme = '/fanstatic/libs/ace-theme-trumpet.js'
    
    rsc = ace_editor_resource_urls prefix
    #window.rsc = rsc
    head = $('head')
    head.append make_javacript_tag rsc.ace
    head.append make_javacript_tag rsc.emacs
    head.append make_javacript_tag rsc.workers[mode]
    head.append make_javacript_tag rsc.modes[mode]
    head.append make_javacript_tag trumpet_theme

# the calendar doesn't render correctly
# when these resources are loaded in this
# manner.

load_fullcalendar_resources = ->
    prefix = '/fanstatic/js.fullcalendar'
    main = url_join prefix, 'fullcalendar.js'
    google = url_join prefix, 'gcal.js'
    head = $('head')
    head.prepend make_javacript_tag main
    head.prepend make_javacript_tag google
    
    
    

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
TrumpetApp.functions.load_ace_editor_resources = load_ace_editor_resources
TrumpetApp.functions.load_fullcalendar_resources = load_fullcalendar_resources


$(document).ready ->
    # hide the status bar
    $('.status-bar').hide()
