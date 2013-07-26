<div class="phonecall-view">
  <div class="phonecall-header">
    ${pcall.caller}
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
