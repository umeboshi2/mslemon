<div class="view-event">
  <div class="event-entry">
    <% kw = dict(context='viewvenue', id=event.id) %>
    <% url = request.route_url('main', **kw) %>
    <p><a class="event-entry-title" href="${url}">${event.title}</a></p>
    ${event.description|n}
  </div>
  <br>
  <div class="export-event-ical action-button">
    <% url = request.route_url('consult_calendar', context='export', id=event.id) %>
    <input type="hidden" value=${url} id="export-event">
    Export iCal
  </div>
</div>
