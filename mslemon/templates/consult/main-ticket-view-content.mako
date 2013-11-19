<div class="ticket-main-view">
  <div id="ticket-content">
    <% tkt_types = ['assigned', 'delegated', 'unread', 'pending', 'closed'] %>
    <div id="calendar-variables">
      %for tkt_type in tkt_types:
      <input type="hidden" id="${tkt_type}Url" value="${calendar_urls[tkt_type]}">
      <input type="hidden" id="calendar_view_${tkt_type}" value="${calviews[tkt_type]}">
      %endfor
    </div>
    <div id="list-variables">
      %for tkt_type in tkt_types:
      <input type="hidden" id="ALL${tkt_type}Url" value="${list_urls[tkt_type]}">
      %endfor
    </div>
    <div id="loading">
      <h2>Loading Events</h2>
    </div>
    <div id="ticket-calendar">
    </div>
    <div id="ticket-list">
    </div>
  </div>
</div>
