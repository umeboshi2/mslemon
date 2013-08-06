<div class="phonecalls-list">
  <div class="phonecalls-list-header">
    Current Phonecalls
  </div>
  <div class="phonecalls-list-list">
    %for call in calls:
    <div class="phonecalls-list-entry">
      <div class="phonecalls-list-entry-content">
	<% c = call %>
	<% a = '%s' % c.caller %>
	<% r = 'consult_phone' %>
	<% kw = dict(context='viewcall', id=c.id) %>
	<% url = request.route_url(r, **kw) %>
	<a href="${url}">${a}</a>&nbsp;(${c.status[0].statustype.name})
	<div class="phonecalls-list-entry-content-received">
	  Received: ${c.received.strftime(dtformat)}
	</div>
	<div class="phonecalls-list-entry-content-lastupdate">
	  Last Update: ${c.status[0].last_change.strftime(dtformat)}
	</div>
      </div>
    </div>
    %endfor
  </div>
</div>
