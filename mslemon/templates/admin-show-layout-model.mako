<input type="hidden" name="model_id" val="${model.id}"/>
<div class="listview-header">
  View Model ${model.name}
</div>
<div class="listview-header">
  Fields
  <div class="action-button pull-right add-field-button">add field</div>
</div>
<div class="listview-list field-list">
  %for field in model.fields:
  <% field = field.field %>
  <div class="listview-entry">
    ${field.name} (${field.type})
    <div class="action-button pull-right edit-button" id="edit-${field.id}">edit</div>
  </div>
  %endfor
</div>
<div id="field-editor"></div>
<p>We need to use ace for text, html and teacup types.</p>
