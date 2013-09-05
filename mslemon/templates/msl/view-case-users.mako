<div class="manage-case-users-view">
  <div class="manage-case-users-header">
  </div>
  <p>Here are the current users on this case.</p>
  <div class="manage-case-users-current-user-list">
    %for cuser in users:
    <div class="manage-case-users-current-user-entry">
      <% url = request.route_url('msl_cases', context='detachuser', id="%s_%s" % (cuser.case_id, cuser.user_id)) %>
      ${cuser.user.username} <a href="${url}">(detach)</a>
    </div>
    %endfor
    <p>You can add another user to this case here.</p>
  <div class="manage-case-users-add-user-form">
    ${form.render()|n}
  </div>
  <% url = request.route_url('msl_cases', context='view', id=users[0].case_id) %>
  <a class="action-button" href="${url}">View Case</a>
</div>
