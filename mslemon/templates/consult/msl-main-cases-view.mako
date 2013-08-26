<div class="cases-main-view">
  <% casetypes = ['assigned', 'delegated', 'unread', 'pending', 'closed'] %>
  <div class="cases-main-view-button-bar">
    <div id="list-button" class="action-button">List</div>
  </div>
  <div class="cases-main-view-button-bar">
    %for casetype in casetypes:
    <div id="${casetype}-button" class="action-button query-button">${casetype.capitalize()}</div>
    %endfor
  </div>
  <hr>
  <div id="cases-content">
    <div id="calendar-variables">
      %for casetype in casetypes:
      <input type="hidden" id="${casetype}Url" value="${calendar_urls[casetype]}">
      <input type="hidden" id="calendar_view_${casetype}" value="${calviews[casetype]}">
      %endfor
    </div>
    <div id="list-variables">
      %for casetype in casetypes:
      <input type="hidden" id="ALL${casetype}Url" value="${list_urls[casetype]}">
      %endfor
    </div>
    <div id="loading">
      <h2>Loading Events</h2>
    </div>
    <div id="cases-type-list-header">
      Current Cases
    </div>
    <div id="cases-calendar">
    </div>
    <div id="cases-list">
    </div>
  </div>
</div>
