loading_events = (bool) ->
    if bool
        $('#loading').show()
        $('.fc-header').hide()
    else
        $('#loading').hide()
        $('.fc-header').show()
        
make_calendar = (element, url, defaultview, firsthour) ->
    element.fullCalendar('destroy')
    element.fullCalendar
        header:
            left: 'month, agendaWeek, agendaDay'
            center: 'title'
        theme: true
        eventSources:
            [
                {
                    url: url
                    color: '#8B8878'
                },
            ]
        editable: false
        selectable: false
        allDayDefault: false
        eventColor: '#8B8878'
        defaultView: defaultview
        loading: loading_events
        # the firstHour is where the agendaDay
        # calendar starts.
        firstHour: firsthour

$(document).ready ->
    $('#loading').hide()
    rnow = new Date()
    thour = rnow.getHours() - 2
    $('#scandoc-list').hide()
    $('#scandoc-calendar').fullCalendar
        header:
            left: 'month, agendaWeek, agendaDay'
            center: 'title'
        theme: true
        eventSources:
            [
                {
                    url: '/msl/scandocsjson/foo/bar'
                    color: '#8B8878'
                },
            ]
        editable: false
        selectable: false
        allDayDefault: false
        eventColor: '#8B8878'
        defaultView: 'agendaWeek'
        # the firstHour is where the agendaDay
        # calendar starts.
        firstHour: thour
    # ######################
    # event source buttons
    # ######################
    $('#list-button').click ->
        button = $('#list-button')
        $('#scandoc-calendar').toggle()
        $('#scandoc-list').toggle()
        text = button.text()
        button.text('sdfsdfsdf')
        if text == 'List'
            button.text('Calendar')
        if text == 'Calendar'
            button.text('List')

