$(document).ready ->
        rnow = new Date()
        thour = rnow.getHours() - 2
        url = '/consult/json/receivedcalls/calls'
        $('#phone-calendar').fullCalendar
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
                defaultView: 'agendaDay'
                # the firstHour is where the agendaDay
                # calendar starts.
                firstHour: thour
                
                
                