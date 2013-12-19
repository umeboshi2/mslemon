<% model = webview.model %>
<input type="hidden" name="webview_id" value="${webview.id}"/>
<input type="hidden" name="model_id" value="${model.id}"/>
<div class="listview-header">
  View WebView ${webview.name}
</div>
<div class="listview-header">
  Model: ${model.name} Fields
</div>
<div class="listview-list field-list">
  %for field in model.fields:
  <% field = field.field %>
  <div class="listview-entry">
    ${field.name} (${field.type})
  </div>
  %endfor
</div>
<div class="listview-list editing-space"></div>
<p>We need to use ace for text, html and teacup types.</p>
