# Create TrumpetApp as a namespace object
window.TrumpetApp = {}


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


# attach some functions to TrumpetApp namespace
TrumpetApp.make_alert_div = make_alert_div
TrumpetApp.make_alert = make_alert
TrumpetApp.get_template = get_template

$(document).ready ->
        # hide the status bar
        $('.status-bar').hide()
