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
    <a href="${url}" id="export-event">Export iCal</a>
  </div>
  <div class="event-manage-users action-button">
    <% kw = dict(context='manageusers', id=event.id) %>
    <% url = request.route_url('consult_calendar', **kw) %>
    <a href="${url}">Manage Users</a>
  </div>
</div>
