<div class="ticket-view">
  <% dlurl = request.route_url('msl_docs', context='export', id=doc.id) %>
  <div class="ticket-header">
    <% the_date = doc.created.strftime('%A, %d %B, %Y') %>
    At ${doc.created.strftime('%R')} on ${the_date}<br>
    A document was named <br>
    ${doc.name} <br>
    by ${doc.created_by.username}.<br>
  </div>
  <div><p>You can press the 
      <a class="action-button" id="download-document" href="${dlurl}">download</a> 
      button to preview the file.
  </div>
  <div> 
    <% url = request.route_url('msl_docs', context='to_case', id=doc.id) %>
    <a class="action-button" href="${url}">Assign to Case</a>
  </div>
  <div>
    ${form|n}
  </div>
  <div class="ticket-description">
  </div>
  <div class="ticket-history">
  </div>
</div>
