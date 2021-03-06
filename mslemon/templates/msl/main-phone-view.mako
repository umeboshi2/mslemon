<div class="phone-main-view">
  <% calltypes = ['received', 'taken', 'assigned', 'delegated', 'unread', 'pending', 'closed'] %>
  <div class="phone-main-view-button-bar">
    <div id="list-button" class="action-button">List</div>
  </div>
  <div class="phone-main-view-button-bar">
    %for calltype in calltypes:
    <div id="${calltype}-button" class="action-button query-button">${calltype.capitalize()}</div>
    %endfor
  </div>
  <hr>
  <div id="phonecall-content">
    <div id="calendar-variables">
      %for calltype in calltypes:
      <input type="hidden" id="${calltype}Url" value="${calendar_urls[calltype]}">
      <input type="hidden" id="calendar_view_${calltype}" value="${calviews[calltype]}">
      %endfor
    </div>
    <div id="list-variables">
      %for calltype in calltypes:
      <input type="hidden" id="ALL${calltype}Url" value="${list_urls[calltype]}">
      %endfor
    </div>
    <div id="loading">
      <h2>Loading Events</h2>
    </div>
    <div class="phonecalls-list-header">
      Current Phonecalls
    </div>
    <div id="phone-calendar">
    </div>
    <div id="phonecall-list">
    </div>
  </div>
</div>
