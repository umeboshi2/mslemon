<div class="phonecall-view">
  <div class="phonecall-header">
    <% the_date = pcall.received.strftime('%A, %d %B, %Y') %>
    <% callee = db.query(User).get(pcall.callee) %>
    <% received_by = db.query(User).get(pcall.received_by) %>
    At ${pcall.received.strftime('%R')} on ${the_date}<br>
    ${pcall.caller} called ${callee}<br>
    (Call received by ${received_by})
  </div>
  <div class="action-button">
    <% p = pcall.number %>
    <% p = p[1:4] + p[5:] %>
    <a href="tel:${p}">${pcall.number}</a>
  </div>
  <div class="phonecall-description">
    ${rst(pcall.text)|n}
  </div>
  <div class="phonecall-history">
    %for pcstatus in pcall.history:
    <div class="phonecall-status-entry">
      <div class="phonecall-status-entry-content">
	<% c = pcstatus %>
	<div class="phonecall-status-entry-changedate">
	  <% format = '%a %H:%M       -----       %d %B, %Y' %>
	  ${c.changed.strftime(format)}
	</div>
	<% status = pcm.stypes.get(c.status).name %>
	<% chng_by = db.query(User).get(c.changed_by_id).username %>
	<% handler = db.query(User).get(c.handler).username %>
	<% msg = '%s(%s)' % (status, chng_by) %>
	<% handle_msg = 'This call is being handled by %s' % handler %>
	<div class="phonecall-status-entry-changed">
	  ${msg}
	</div>
	<div class="phonecall-status-entry-reason">
	  ${rst(c.reason)|n}
	</div>
	${handle_msg}
      </div>
    </div>
    %endfor
  </div>
  <div class="phonecall-update-phonecall">
    <% kw = dict(context='updatephonecall', id=pcall.id) %>
    <% url = request.route_url('consult_phone', **kw) %>
    <a href="${url}">Update Status</a>
  </div>
</div>
