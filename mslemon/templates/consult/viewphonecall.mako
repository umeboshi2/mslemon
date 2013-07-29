<div class="phonecall-view">
  <div class="phonecall-header">
    <% the_date = pcall.received.strftime('%A, %d %B, %Y') %>
    <% callee = db.query(User).get(pcall.callee) %>
    <% received_by = db.query(User).get(pcall.received_by) %>
    At ${pcall.received.strftime('%R')} on ${the_date}<br>
    ${pcall.caller} called ${callee}<br>
    (Call received by ${received_by})
  </div>
  <div class="phonecall-description">
    ${rst(pcall.text)|n}
  </div>
  <div class="phonecall-update-phonecall">
    <% kw = dict(context='updatephonecall', id=pcall.id) %>
    <% url = request.route_url('consult_phone', **kw) %>
    <a href="${url}">Update Status</a>
  </div>
</div>
