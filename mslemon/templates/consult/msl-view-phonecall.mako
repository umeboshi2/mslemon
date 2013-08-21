<div class="ticket-view">
  <div class="phonecall-header">
    <% ticket = pcall.ticket %>
    <% the_date = pcall.received.strftime('%A, %d %B, %Y') %>
    <% callee = pcall.callee %>
    <% received_by = pcall.received_by %>
    At ${pcall.received.strftime('%R')} on ${the_date}<br>
    ${pcall.caller} called ${callee}<br>
    (Call received by ${received_by})
  </div>
  <div class="ticket-header">
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
  <div class="ticket-history">
    %for tstatus in ticket.history:
    <div class="ticket-status-entry">
      <div class="ticket-status-entry-content">
	<% c = tstatus %>
	<div class="ticket-status-entry-changedate">
	  <% format = '%a %H:%M       -----       %d %B, %Y' %>
	  ${c.changed.strftime(format)}
	</div>
	<% status = c.status %>
	<% chng_by = c.changed_by.username %>
	<% handler = c.handler.username %>
	<% msg = '%s(%s)' % (status, chng_by) %>
	<% handle_msg = 'This ticket is being handled by %s' % handler %>
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
    <% kw = dict(context='updateticket', id=ticket.id) %>
    <% url = request.route_url('msl_tickets', **kw) %>
    <a href="${url}">Update Status</a>
  </div>
</div>
