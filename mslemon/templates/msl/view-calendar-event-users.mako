<div class="manage-event-users-view">
  <div class="manage-event-users-header">
  </div>
  <p>Here are the current users on this event.</p>
  <div class="manage-event-users-current-user-list">
    %for cuser in users:
    <div class="manage-event-users-current-user-entry">
      <% url = request.route_url('consult_calendar', context='detachuser', id="%s_%s" % (cuser.event_id, cuser.user_id)) %>
      ${cuser.user.username} <a href="${url}">(detach)</a>
    </div>
    %endfor
    <p>You can add another user to this event here.</p>
  <div class="manage-event-users-add-user-form">
    ${form.render()|n}
  </div>
  <% url = request.route_url('consult_calendar', context='view', id=event.id) %>
  <a class="action-button" href="${url}">View Event</a>
</div>
