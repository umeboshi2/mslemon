jQuery ->
        ########################################
        # Templates
        ########################################
        list_titles =
                path: 'Site Paths'
                tmpl: 'Site Templates'
                css: 'Site CSS'
                js: 'Site Javascript'
                
        side_view_template =
                """
                <div class="main-content-manager-view">
                <div>
                <div class="action-button home-button">Main</div>
                </div>
                <div>
                <div class="action-button sitepaths-button">Paths</div>
                </div>
                <div>
                <div class="action-button sitetmpl-button">Templates</div>
                </div>
                <div>
                <div class="action-button sitecss-button">CSS</div>
                </div>
                <div>
                <div class="action-button sitejs-button">JS</div>
                </div>
                <div>
                <div class="action-button sitefoo-button">nothing</div>
                </div>
                </div>
                """
        #######################################################
        entry_template =
                '
                <div class="listview-list-entry">
                        <%= name %> 
          <div class="pull-right action-button show-entry-btn">show</div>
                </div>
                '
        #######################################################
        editor_template = '
                <div id="edit-status">Editing <%= name %>
                <div class="action-button" id="save-content">Save</div>
                </div>
                <div id="editor"></div>
                '
        listview_template = '
                <% var title = TrumpetApp.admin_mgr_tmpl.list_titles[type] %>
                <div class="listview-header"><%= title %>
                <div class="pull-right action-button add-entry-btn">New Entry</div>
                </div>
                <div class="listview-list"></div>
                '
        #######################################################
        admin_mgr_tmpl =
                list_titles: list_titles
                side_view_template:
                        new EJS text: side_view_template
                entry_template:
                        new EJS text: entry_template
                editor_template:
                        new EJS text: editor_template
                listview_template:
                        new EJS text: listview_template
        window.TrumpetApp = {}
        TrumpetApp.admin_mgr_tmpl = admin_mgr_tmpl

        

        
                
