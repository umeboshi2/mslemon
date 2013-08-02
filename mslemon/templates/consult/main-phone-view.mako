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
    <div id="calendar-variables">
      <input type="hidden" id="receivedUrl" value="${received_url}">
      <input type="hidden" id="assignedUrl" value="${assigned_url}">
      <input type="hidden" id="delegatedUrl" value="${delegated_url}">
      <input type="hidden" id="unreadUrl" value="${unread_url}">
      <input type="hidden" id="pendingUrl" value="${pending_url}">
      <input type="hidden" id="closedUrl" value="${closed_url}">
    </div>
    <div id="phone-calendar">
    </div>
    <div id="phonecall-list">
    </div>
  </div>
</div>
