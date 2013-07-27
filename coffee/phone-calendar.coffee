$(document).ready ->
        rnow = new Date()
        thour = rnow.getHours() - 4
        $('#phone-calendar').fullCalendar
                header:
                        left: 'month, agendaWeek, agendaDay'
                        center: 'title'
                theme: true
                eventSources:
                        [
                                url: '/consult/json/phonecal/calls'
                        ]
                editable: false
                selectable: false
                allDayDefault: false
                #loading: loading_events
                #eventAfterRender: render_cal_event
                #eventRender: render_cal_event
                #eventMouseover: mouse_over_event
                eventColor: '#8B8878'
                defaultView: 'agendaDay'
                firstHour: thour
                
                
                