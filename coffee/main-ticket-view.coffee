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
        $('#ticket-list').hide()
        $('#ticket-calendar').fullCalendar
                header:
                        left: 'month, agendaWeek, agendaDay'
                        center: 'title'
                theme: true
                eventSources:
                        [
                                {
                                        url: $('#assignedUrl').val()
                                        color: '#8B8878'
                                },
                        ]
                editable: false
                selectable: false
                allDayDefault: false
                eventColor: '#8B8878'
                defaultView: $('#calendar_view_assigned').val()
                # the firstHour is where the agendaDay
                # calendar starts.
                firstHour: thour
        # ######################
        # event source buttons
        # ######################
        $('#list-button').click ->
                button = $('#list-button')
                $('#ticket-calendar').toggle()
                $('#ticket-list').toggle()
                text = button.text()
                button.text('sdfsdfsdf')
                if text == 'List'
                        button.text('Calendar')
                if text == 'Calendar'
                        button.text('List')

        $('.query-button').click ->
                calendar_content = $('#ticket-calendar')
                list_content = $('#ticket-list')
                viewbutton = $('#list-button')
                view = viewbutton.text()
                button = $(this)
                tkt_type = $(this).attr('id').split('-')[0]
                defaultViewID = '#calendar_view_' + tkt_type
                defaultView = $(defaultViewID).val()
                # FIXME: we may need a bar of buttons for different
                # view types.
                # 
                # if the view text says List, we are in Calendar view
                if view == 'List'
                        urlid = '#' + tkt_type + 'Url'
                        now = new Date()
                        hr = now.getHours() - 2
                        url = $(urlid).val()
                        element = calendar_content
                        # FIXME: put calendar view type in template
                        make_calendar(element, url, defaultView, hr)
                # else we are in List View
                else
                        urlid = '#ALL' + tkt_type + 'Url'
                        url = $(urlid).val()
                        list_content.load(url, {}, () ->
                                title = tkt_type.slice(0,1).toUpperCase() + tkt_type.slice(1)
                                $('.tickets-list-header').text(title + ' Tickets')
                                )

                
                
                        

                        
                
                