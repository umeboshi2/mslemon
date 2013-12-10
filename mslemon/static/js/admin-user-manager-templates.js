// Generated by CoffeeScript 1.6.3
(function() {
  jQuery(function() {
    var admin_usrmgr_tmpl, create_template, editor_template, entry_template, list_titles, listview_template, side_view_template;
    list_titles = {
      path: 'Site Paths',
      tmpl: 'Site Templates',
      css: 'Site CSS',
      js: 'Site Javascript'
    };
    side_view_template = '\
                <div class="main-content-manager-view">\
                <div>\
                <div class="action-button home-button">Main</div>\
                </div>\
                <div>\
                <div class="action-button sitefoo-button">nothing</div>\
                </div>\
                </div>\
                ';
    entry_template = '\
                <div class="listview-list-entry">\
                        <%= name %> \
          <div class="pull-right action-button show-entry-btn">show</div>\
                </div>\
                ';
    editor_template = '\
                <div id="edit-status">Editing <%= name %>\
                <div class="action-button" id="save-content">Save</div>\
                </div>\
                <div id="editor"></div>\
                ';
    listview_template = '\
                <% var title = TrumpetApp.admin_mgr_tmpl.list_titles[type] %>\
                <div class="listview-header"><%= title %>\
                <div class="pull-right action-button add-entry-btn" id="new-entry-button">New Entry</div>\
                </div>\
                <div class="listview-list"></div>\
                ';
    create_template = '\
                <div class="listview-header2">\
                </div>\
                <div class="create-form">\
                        <div class="action-button" id="create-content">Save</div>\
                        <span class="form-inline" style="white-space:nowrap">\
                        <label class="form-inline" for="nameinput">Name</label>\
                        <input style="width:80%" class="form-control form-inline pull-right" name="name" id="nameinput">\
                        </span>\
                        <div id="edit-status">\
                        </div>\
                        <div id="editor"></div>\
                </div>        \
                ';
    admin_usrmgr_tmpl = {
      list_titles: list_titles,
      side_view_template: new EJS({
        text: side_view_template
      }),
      entry_template: new EJS({
        text: entry_template
      }),
      editor_template: new EJS({
        text: editor_template
      }),
      listview_template: new EJS({
        text: listview_template
      }),
      create_template: new EJS({
        text: create_template
      })
    };
    return TrumpetApp.admin_usrmgr_tmpl = admin_usrmgr_tmpl;
  });

}).call(this);