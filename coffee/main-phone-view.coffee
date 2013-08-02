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
                # the firstHour is where the agendaDay
                # calendar starts.
                firstHour: firsthour

make_calendar_orig = (element) ->
        eventSource_ = $('#eventSource').val()
        defaultView_ = $('#defaultView').val()
        rnow = new Date()
        thour = rnow.getHours() - 2


$(document).ready ->
        rnow = new Date()
        thour = rnow.getHours() - 2
        #$('#phonecall-list').load('/consult/frag/contactlist/A')
        $('#phonecall-list').hide()
        $('#phone-calendar').fullCalendar
                header:
                        left: 'month, agendaWeek, agendaDay'
                        center: 'title'
                theme: true
                eventSources:
                        [
                                {
                                        url: $('#receivedUrl').val()
                                        color: '#8B8878'
                                },
                        ]
                editable: false
                selectable: false
                allDayDefault: false
                eventColor: '#8B8878'
                defaultView: 'agendaDay'
                # the firstHour is where the agendaDay
                # calendar starts.
                firstHour: thour
        # ######################
        # event source buttons
        # ######################
        $('#received-button').click ->
                _now = new Date()
                _hr = _now.getHours() - 2
                _url = $('#receivedUrl').val()
                _element = $('#phone-calendar')
                make_calendar(_element, _url, 'agendaDay', _hr)                

        $('#assigned-button').click ->
                _now = new Date()
                _hr = _now.getHours() - 2
                _url = $('#assignedUrl').val()
                _element = $('#phone-calendar')
                make_calendar(_element, _url, 'agendaWeek', _hr)                

        $('#delegated-button').click ->
                _now = new Date()
                _hr = _now.getHours() - 2
                _url = $('#delegatedUrl').val()
                _element = $('#phone-calendar')
                make_calendar(_element, _url, 'agendaWeek', _hr)                

        $('#unread-button').click ->
                _now = new Date()
                _hr = _now.getHours() - 2
                _url = $('#unreadUrl').val()
                _element = $('#phone-calendar')
                make_calendar(_element, _url, 'agendaWeek', _hr)                
                
        $('#pending-button').click ->
                _now = new Date()
                _hr = _now.getHours() - 2
                _url = $('#pendingUrl').val()
                _element = $('#phone-calendar')
                make_calendar(_element, _url, 'agendaWeek', _hr)                

        $('#closed-button').click ->
                _now = new Date()
                _hr = _now.getHours() - 2
                _url = $('#closedUrl').val()
                _element = $('#phone-calendar')
                make_calendar(_element, _url, 'month', _hr)                
                
        $('#list-button').click ->
                button = $('#list-button')
                $('#phone-calendar').toggle()
                $('#phonecall-list').toggle()
                text = button.text()
                button.text('sdfsdfsdf')
                if text == 'List'
                        button.text('Calendar')
                if text == 'Calendar'
                        button.text('List')
                        