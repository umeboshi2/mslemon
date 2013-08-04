<div class="phone-main-view">
  <div class="phone-main-view-button-bar">
    <div id="list-button" class="action-button">List</div>
  </div>
  <div class="phone-main-view-button-bar">
    <div id="received-button" class="action-button query-button">Received</div>
    <div id="assigned-button" class="action-button query-button">Assigned</div> 
    <div id="delegated-button" class="action-button query-button">Delegated</div> 
    <div id="unread-button" class="action-button query-button">Unread</div>
    <div id="pending-button" class="action-button query-button">Pending</div>
    <div id="closed-button" class="action-button query-button">Closed</div>
  </div>
  <hr>
  <div id="phonecall-content">
    <% calltypes = ['received', 'assigned', 'delegated', 'unread', 'pending', 'closed'] %>
    <div id="calendar-variables">
      %for calltype in calltypes:
      <input type="hidden" id="${calltype}Url" value="${calendar_urls[calltype]}">
      %endfor
    </div>
    <div id="list-variables">
      %for calltype in calltypes:
      <input type="hidden" id="ALL${calltype}Url" value="${list_urls[calltype]}">
      %endfor
    </div>
    <div id="phone-calendar">
    </div>
    <div id="phonecall-list">
    </div>
  </div>
</div>
