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
    $('#cases-list').hide()
    $('#cases-calendar').fullCalendar
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
        $('#cases-type-list-header').text('Assigned Cases')
    # ######################
    # event source buttons
    # ######################
    $('#list-button').click ->
        button = $('#list-button')
        $('#cases-calendar').toggle()
        $('#cases-list').toggle()
        text = button.text()
        button.text('sdfsdfsdf')
        if text == 'List'
            button.text('Calendar')
        if text == 'Calendar'
            button.text('List')

    $('.query-button').click ->
        calendar_content = $('#cases-calendar')
        list_content = $('#cases-list')
        viewbutton = $('#list-button')
        view = viewbutton.text()
        button = $(this)
        case_type = $(this).attr('id').split('-')[0]
        defaultViewID = '#calendar_view_' + case_type
        defaultView = $(defaultViewID).val()
        # FIXME: we may need a bar of buttons for different
        # view types.
        # 
        # if the view text says List, we are in Calendar view
        if view == 'List'
            urlid = '#' + case_type + 'Url'
            now = new Date()
            hr = now.getHours() - 2
            url = $(urlid).val()
            element = calendar_content
            # FIXME: put calendar view type in template
            make_calendar(element, url, defaultView, hr)
            title = case_type.slice(0,1).toUpperCase() + case_type.slice(1)
            $('#cases-type-list-header').text(title + ' Cases')
        # else we are in List View
        else
            urlid = '#ALL' + case_type + 'Url'
            url = $(urlid).val()
            list_content.load(url, {}, () ->
                title = case_type.slice(0,1).toUpperCase() + case_type.slice(1)
                $('#cases-type-list-header').text(title + ' Cases')
                )
                

                
                
                        

                        
                
                