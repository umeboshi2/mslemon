// Generated by CoffeeScript 1.6.1
(function() {
  var make_calendar;

  make_calendar = function(element) {
    var defaultView, eventSource, rnow, thour;
    eventSource = $('#eventSource').val();
    defaultView = $('#defaultView').val();
    rnow = new Date();
    thour = rnow.getHours() - 2;
    element.load('/');
    $('#list-button').hide();
    return element.fullCalendar({
      header: {
        left: 'month, agendaWeek, agendaDay',
        center: 'title'
      },
      theme: true,
      eventSources: [
        {
          url: eventSource,
          color: '#8B8878'
        }
      ],
      editable: false,
      selectable: false,
      allDayDefault: false,
      eventColor: '#8B8878',
      defaultView: defaultView,
      firstHour: thour
    });
  };

}).call(this);
