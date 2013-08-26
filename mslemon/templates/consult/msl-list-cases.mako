<div class="tickets-list">
  <div class="tickets-list-list">
    %for cstatus in clist:
    <div class="tickets-list-entry">
      <div class="tickets-list-entry-content">
	<% case = cstatus.case %>
	<% a = '%s' % case.name %>
	<% r = 'msl_cases' %>
	<% kw = dict(context='view', id=case.id) %>
	<% url = request.route_url(r, **kw) %>
	<a href="${url}">${a}</a>&nbsp;(${cstatus.status})
	<div class="tickets-list-entry-content-received">
	  Created: ${case.created.strftime(dtformat)}
	</div>
	<div class="tickets-list-entry-content-lastupdate">
	  Last Update: ${cstatus.last_change.strftime(dtformat)}
	</div>
      </div>
    </div>
    %endfor
  </div>
</div>
