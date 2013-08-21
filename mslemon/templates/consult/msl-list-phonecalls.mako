<div class="phonecalls-list">
  <div class="phonecalls-list-header">
    Current Phonecalls
  </div>
  <div class="phonecalls-list-list">
    %for pcall, cstatus in clist:
    <div class="phonecalls-list-entry">
      <div class="phonecalls-list-entry-content">
	<% a = '%s' % pcall.caller %>
	<% call = pcall %>
	<% r = 'consult_phone' %>
	<% kw = dict(context='view', id=call.id) %>
	<% url = request.route_url(r, **kw) %>
	<a href="${url}">${a}</a>&nbsp;(${cstatus.status})
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
