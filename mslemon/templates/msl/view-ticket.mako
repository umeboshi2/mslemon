<div class="ticket-view">
  <div class="listview-header">
    <% the_date = ticket.created.strftime('%A, %d %B, %Y') %>
    <% first_change = ticket.history[0] %>
    <% handler = first_change.handler.username %>
    <% opener = first_change.changed_by.username %>
    At ${ticket.created.strftime('%R')} on ${the_date}<br>
    ${opener} created a ticket for ${handler}<br>
  </div>
  <div class="ticket-description">
    ${rst(ticket.description.text)|n}
  </div>
  <div class="listview-history">
    %for tstatus in ticket.history:
    <div class="listview-status-entry">
      <div class="ticket-status-entry-content">
	<% c = tstatus %>
	<div class="listview-status-entry-changedate">
	  <% format = '%a %H:%M       -----       %d %B, %Y' %>
	  ${c.changed.strftime(format)}
	</div>
	<% status = c.status %>
	<% chng_by = c.changed_by.username %>
	<% handler = c.handler.username %>
	<% msg = '%s(%s)' % (status, chng_by) %>
	<% handle_msg = 'This ticket is being handled by %s' % handler %>
	<div class="listview-status-entry-changed">
	  ${msg}
	</div>
	<div class="listview-status-entry-reason">
	  ${rst(c.reason)|n}
	</div>
	${handle_msg}
      </div>
    </div>
    %endfor
  </div>
  <div class="ticket-update-ticket action-button">
    <% kw = dict(context='updateticket', id=ticket.id) %>
    <% url = request.route_url('msl_tickets', **kw) %>
    <a href="${url}">Update Status</a>
  </div>
</div>
