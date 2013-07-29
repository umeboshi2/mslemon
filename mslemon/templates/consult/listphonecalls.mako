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
	<a href="${url}">${a}</a>
      </div>
    </div>
    %endfor
  </div>
</div>
