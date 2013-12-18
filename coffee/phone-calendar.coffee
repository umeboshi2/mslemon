make_calendar = (element) ->
    eventSource = $('#eventSource').val()
    defaultView = $('#defaultView').val()
    rnow = new Date()
    thour = rnow.getHours() - 2
    element.load('/')
    $('#list-button').hide()
    element.fullCalendar
        header:
            left: 'month, agendaWeek, agendaDay'
            center: 'title'
        theme: true
        eventSources:
            [
                {
                    url: eventSource
                    color: '#8B8878'
                },
            ]
        editable: false
        selectable: false
        allDayDefault: false
        eventColor: '#8B8878'
        defaultView: defaultView
        # the firstHour is where the agendaDay
        # calendar starts.
        firstHour: thour
                
                
