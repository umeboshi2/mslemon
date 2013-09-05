<div class="ticket-view">
  <% dlurl = request.route_url('msl_scandocs', context='export', id=sdoc.created.isoformat()) %>
  <div class="ticket-header">
    <% the_date = sdoc.created.strftime('%A, %d %B, %Y') %>
    At ${sdoc.created.strftime('%R')} on ${the_date}<br>
    A document was scanned to ${scanplace}.<br>
  </div>
  <div><p>A document was scanned to the scanner in pdf format.  The document 
      has been named by the date and time of scanning, which is reflected 
      below. You can press the <a class="action-button" id="download-document" href="${dlurl}">download</a> button to preview the file.  If the file is your file, you can rename it below, and it will disappear from the scanned documents calendar.  Other users will not be able to see this document until you attach it to a client, ticket, or case.</p>
  </div>
  <div>
    ${form|n}
  </div>
  <div class="action-button">
    <% url = request.route_url('msl_scandocs', context='main', id='all') %>
    <a href="${url}">Scanned Documents</a>
  </div>
  <div class="ticket-description">
  </div>
  <div class="ticket-history">
  </div>
</div>
