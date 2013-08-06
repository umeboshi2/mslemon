<div class="phonecalls-list">
  <div class="phonecalls-list-header">
    Current Phonecalls
  </div>
  <div class="phonecalls-list-list">
    %for cstatus in clist:
    <div class="phonecalls-list-entry">
      <div class="phonecalls-list-entry-content">
	<% a = '%s' % cstatus.phone_call.caller %>
	<% call = cstatus.phone_call %>
	<% r = 'consult_phone' %>
	<% kw = dict(context='viewcall', id=call.id) %>
	<% url = request.route_url(r, **kw) %>
	<a href="${url}">${a}</a>&nbsp;(${cstatus.statustype.name})
	<div class="action-button">
	  <% p = call.number %>
	  <% p = p[1:4] + p[5:] %>
	  <a href="tel:${p}">${call.number}</a>
	</div>
	<div class="phonecalls-list-entry-content-received">
	  Received: ${call.received.strftime(dtformat)}
	</div>
	<div class="phonecalls-list-entry-content-lastupdate">
	  Last Update: ${cstatus.last_change.strftime(dtformat)}
	</div>
      </div>
    </div>
    %endfor
  </div>
</div>
