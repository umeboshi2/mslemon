$(document).ready ->
        rnow = new Date()
        thour = rnow.getHours() - 2
        $('#phone-calendar').fullCalendar
                header:
                        left: 'month, agendaWeek, agendaDay'
                        center: 'title'
                theme: true
                eventSources:
                        [
                                {
                                        url:'/consult/json/phonecal/calls',
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
                
                
                