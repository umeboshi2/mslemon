<div class="ticket-view">
  <div class="ticket-header">
    <% the_date = case.created.strftime('%A, %d %B, %Y') %>
    <% first_change = case.history[0] %>
    <% handler = first_change.handler.username %>
    <% opener = first_change.changed_by.username %>
    At ${case.created.strftime('%R')} on ${the_date}<br>
    ${opener} created a case for ${handler}<br>
  </div>
  <div class="ticket-update-ticket">
    <% kw = dict(context='update', id=case.id) %>
    <% url = request.route_url('msl_cases', **kw) %>
    <a href="${url}">Update Status</a>
  </div>
  <div class="case-manage-users action-button">
    <% kw = dict(context='manageusers', id=case.id) %>
    <% url = request.route_url('msl_cases', **kw) %>
    <a href="${url}">Manage Users</a>
  </div>
  <div class="case-attach-ticket action-button">
    <% kw = dict(context='attachtkt', id=case.id) %>
    <% url = request.route_url('msl_cases', **kw) %>
    <a href="${url}">Attach Ticket</a>
  </div>
  <div class="case-attach-document action-button">
    <% kw = dict(context='attachdoc', id=case.id) %>
    <% url = request.route_url('msl_cases', **kw) %>
    <a href="${url}">Attach Document</a>
  </div>
  <div class="ticket-description">
    ${rst(case.description.text)|n}
  </div>
  <div class="case-document-list">
    <strong>Documents</strong>
    %for doc in case.documents:
    <div class="case-document-list-entry">
      <% url = request.route_url('msl_docs', context='export', id=doc.doc_id) %>
      <a href="${url}">${doc.document.name}</a>
    </div>
    %endfor
  </div>
  <div class="case-ticket-list">
    <strong>Tickets</strong>
    %for ctkt in case.tickets:
    <div class="case-ticket-list-entry">
      <% url = request.route_url('msl_tickets', context='view', id=ctkt.ticket_id) %>
      <a href="${url}">${ctkt.ticket.title}</a>
    </div>
    %endfor
  </div>
  <div class="ticket-history">
    <strong>History</strong>
    %for cstatus in case.history:
    <div class="ticket-status-entry">
      <div class="ticket-status-entry-content">
	<% c = cstatus %>
	<div class="ticket-status-entry-changedate">
	  <% format = '%a %H:%M       -----       %d %B, %Y' %>
	  ${c.changed.strftime(format)}
	</div>
	<% status = c.status %>
	<% chng_by = c.changed_by.username %>
	<% handler = c.handler.username %>
	<% msg = '%s(%s)' % (status, chng_by) %>
	<% handle_msg = 'This case is being handled by %s' % handler %>
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
    <% kw = dict(context='update', id=case.id) %>
    <% url = request.route_url('msl_cases', **kw) %>
    <a href="${url}">Update Status</a>
  </div>
</div>
