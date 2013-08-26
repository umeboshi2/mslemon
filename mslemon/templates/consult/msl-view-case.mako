<div class="ticket-view">
  <div class="ticket-header">
    <% the_date = case.created.strftime('%A, %d %B, %Y') %>
    <% first_change = case.history[0] %>
    <% handler = first_change.handler.username %>
    <% opener = first_change.changed_by.username %>
    At ${case.created.strftime('%R')} on ${the_date}<br>
    ${opener} created a case for ${handler}<br>
  </div>
  <div class="ticket-description">
    ${rst(case.description.text)|n}
  </div>
  <div class="ticket-history">
    %for cstatus in case.history:
    <div class="ticket-status-entry">
      <div class="ticket-status-entry-content">
	<% c = cstatus %>
	<div class="ticket-status-entry-changedate">
	  <% format = '%a %H:%M       -----       %d %B, %Y' %>
	  ${c.changed.strftime(format)}
	</div>
	<% status = c.status %>
	<% chng_by = c.changed_by.username %>
	<% handler = c.handler.username %>
	<% msg = '%s(%s)' % (status, chng_by) %>
	<% handle_msg = 'This case is being handled by %s' % handler %>
	<div class="ticket-status-entry-changed">
	  ${msg}
	</div>
	<div class="ticket-status-entry-reason">
	  ${rst(c.reason)|n}
	</div>
	${handle_msg}
      </div>
    </div>
    %endfor
  </div>
  <div class="ticket-update-ticket">
    <% kw = dict(context='update', id=case.id) %>
    <% url = request.route_url('msl_cases', **kw) %>
    <a href="${url}">Update Status</a>
  </div>
</div>
