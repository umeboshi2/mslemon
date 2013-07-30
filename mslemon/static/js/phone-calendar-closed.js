// Generated by CoffeeScript 1.6.1
(function() {

  $(document).ready(function() {
    var rnow, thour, url;
    rnow = new Date();
    thour = rnow.getHours() - 2;
    url = '/consult/json/closedcalls/calls';
    return $('#phone-calendar').fullCalendar({
      header: {
        left: 'month, agendaWeek, agendaDay',
        center: 'title'
      },
      theme: true,
      eventSources: [
        {
          url: url,
          color: '#8B8878'
        }
      ],
      editable: false,
      selectable: false,
      allDayDefault: false,
      eventColor: '#8B8878',
      defaultView: 'agendaDay',
      firstHour: thour
    });
  });

}).call(this);
