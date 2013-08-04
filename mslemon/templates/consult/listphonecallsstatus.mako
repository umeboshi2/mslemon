<div class="phonecalls-list">
  <div class="phonecalls-list-header">
    Current Phonecalls
  </div>
  <div class="phonecalls-list-list">
    %for cstatus in clist:
    <div class="phonecalls-list-entry">
      <div class="phonecalls-list-entry-content">
	<% a = '%s' % cstatus.phone_call.caller %>
	<% r = 'consult_phone' %>
	<% kw = dict(context='viewcall', id=cstatus.phone_call.id) %>
	<% url = request.route_url(r, **kw) %>
	<a href="${url}">${a}</a>&nbsp;(${cstatus.statustype.name})
	<div class="phonecalls-list-entry-content-received">
	  Received: ${cstatus.phone_call.received.strftime(dtformat)}
	</div>
	<div class="phonecalls-list-entry-content-lastupdate">
	  Last Update: ${cstatus.last_change.strftime(dtformat)}
	</div>
      </div>
    </div>
    %endfor
  </div>
</div>
