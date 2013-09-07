$(document).ready ->
                
        $('#action-button-submit').hide()
        mouse_over_event = (event, jsEvent, view) ->
                #$('header > h2').text(event.title)
                #$(this).css().clear()
                #content = $(this).html()
                $('header > h2').text(event.title)
                
        loading_events = (bool) ->
                if bool
                        $('#loading').show()
                        $('.fc-header').hide()
                else
                        $('#loading').hide()
                        $('.fc-header').show()

        render_cal_event = (calEvent, element) ->
                element.css
                        'font-size': '0.7em'
                        'padding': '0.2em'
        eventless = () ->
                alert('No events displayed')
                
        eventObject =
                title: "New Event"
                color: 'red'
                textColor: 'RoyalBlue'
                

        
        $('#newevent').data('eventObject', eventObject)
        $('#newevent').draggable 
                zIndex: 999
                revert: true
                revertDuration: 0

        drop_an_event = (date, allDay) ->
                today = Date()
                if today == today
                        originalEventObject = $(this).data('eventObject')
                        copiedEventObject = $.extend({}, originalEventObject)
                        copiedEventObject.start = date
                        title = $('#newevent_input').val()
                        copiedEventObject.title = title
                        copiedEventObject.allDay = allDay
                        $('#maincalendar').fullCalendar('renderEvent',
                                copiedEventObject, true)
                        $(this).remove()
                        $('#newevent-container').remove()
                        $('#action-button-submit').toggle()
                else
                        $(this).hide()
                        location.reload()

        $('#action-button-submit').click ->
                $('#maincalendar').toggle()
                events = $('#maincalendar').fullCalendar('clientEvents')
                event = events[0]
                estart = event.start.getTime()
                # It looks like a new Date object must be made
                d = new Date()
                now = d.getTime()
                if estart <= now
                        alert("Event starts before now. Try again.")
                        location.reload()
                        return
                format = 'yyyy-MM-dd HH:mm:ss'
                start = event.start
                end = event.end
                event.start = $('#maincalendar')
                        .fullCalendar('formatDate', start, format)
                event.end = $('#maincalendar')
                        .fullCalendar('formatDate', end, format)
                addurl = $('#add-event-url').val()
                post_to_url(addurl, event, 'post')

        evurl = $('#event-source-url').val()
        $('#maincalendar').fullCalendar
                header:
                        left: 'month, agendaWeek, agendaDay'
                        center: 'title'
                theme: true
                eventSources:
                        [
                                url: evurl
                        ]
                editable: true
                droppable: true
                drop: drop_an_event
                selectable: false
                allDayDefault: false
                loading: loading_events
                eventAfterRender: render_cal_event
                eventRender: render_cal_event
                #eventMouseover: mouse_over_event
                eventColor: '#8B8878'
                defaultView: 'month'
                