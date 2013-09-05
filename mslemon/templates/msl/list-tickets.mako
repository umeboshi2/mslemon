<div class="tickets-list">
  <div class="tickets-list-header">
    Current Tickets
  </div>
  <div class="tickets-list-list">
    %for cstatus in tlist:
    <div class="tickets-list-entry">
      <div class="tickets-list-entry-content">
	<% ticket = cstatus.ticket %>
	<% a = '%s' % ticket.title %>
	<% r = 'msl_tickets' %>
	<% kw = dict(context='viewticket', id=ticket.id) %>
	<% url = request.route_url(r, **kw) %>
	<a href="${url}">${a}</a>&nbsp;(${cstatus.status})
	<div class="tickets-list-entry-content-received">
	  Created: ${ticket.created.strftime(dtformat)}
	</div>
	<div class="tickets-list-entry-content-lastupdate">
	  Last Update: ${cstatus.last_change.strftime(dtformat)}
	</div>
      </div>
    </div>
    %endfor
  </div>
</div>
