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
                defaultView: $('#calendar_view_received').val()
                # the firstHour is where the agendaDay
                # calendar starts.
                firstHour: thour
        # ######################
        # event source buttons
        # ######################
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

        $('.query-button').click ->
                calendar_content = $('#phone-calendar')
                list_content = $('#phonecall-list')
                viewbutton = $('#list-button')
                view = viewbutton.text()
                button = $(this)
                calltype = $(this).attr('id').split('-')[0]
                defaultViewID = '#calendar_view_' + calltype
                defaultView = $(defaultViewID).val()
                # FIXME: we may need a bar of buttons for different
                # view types.
                # 
                # if the view text says List, we are in Calendar view
                if view == 'List'
                        urlid = '#' + calltype + 'Url'
                        now = new Date()
                        hr = now.getHours() - 2
                        url = $(urlid).val()
                        element = calendar_content
                        # FIXME: put calendar view type in template
                        make_calendar(element, url, defaultView, hr)
                # else we are in List View
                else
                        urlid = '#ALL' + calltype + 'Url'
                        url = $(urlid).val()
                        list_content.load(url, {}, () ->
                                title = calltype.slice(0,1).toUpperCase() + calltype.slice(1)
                                $('.phonecalls-list-header').text(title + ' Phone Calls')
                                )

                
                
                        

                        
                
                
