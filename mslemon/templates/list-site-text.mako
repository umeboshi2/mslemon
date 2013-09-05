<div class="tickets-list">
  <div class="tickets-list-list">
    %for entry in entries:
    <div class="tickets-list-entry">
      <div class="tickets-list-entry-content">
	<% getdata = dict(context='viewentry', id=entry.id) %>
	<% href_view = viewer.url(**getdata) %>
	<% getdata['context'] = 'editentry' %>
	<% href_edit = viewer.url(**getdata) %>
	<a href="${href_view}">${entry.name}</a>
	<div class="tickets-list-entry-content-edit">
	  <a href="${href_edit}">(edit)</a>
	</div>
      </div>
    </div>
    %endfor
  </div>
</div>
