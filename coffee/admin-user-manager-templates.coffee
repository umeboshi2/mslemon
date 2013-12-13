jQuery ->
        ########################################
        # Templates
        ########################################
        list_titles =
                user: 'Users'
                group: 'Groups'

                
        side_view_template =
                '
                <div class="main-content-manager-view btn-group-vertical">
                <div class="btn btn-default home-button">Main</div>
                <div class="btn btn-default users-button">Users</div>
                <div class="btn btn-default groups-button">Groups</div>
                </div>
                '
        #######################################################
        entry_template =
                '
                <div class="listview-list-entry">
                        <%= name %> 
          <div class="pull-right btn btn-default btn-xs show-entry-btn"><i class="fa fa-folder-open"></i></div>
                </div>
                '
        user_entry_template =
                '
                <div class="listview-list-entry">
                        <%= username %> 
          <div class="pull-right btn btn-default btn-xs show-entry-btn"><i class="fa fa-folder-open"></i></div>
                </div>
                '
        #######################################################
        main_user_view = '
                <div class="main-user-view">
                        view user <strong><%= username %></strong>
                        <div class="listview-header">Groups for <%= username %><div class="btn btn-default btn-xs pull-right" id="addgroup">Add Group</div></div>
                       <div class="user-group-list listview-list">
                        </div>
                </div>
                '
        user_group_entry = '
                <div>
                        <%= name %>
                        <div class="btn btn-default btn-xs">remove</div>
                </div>
                '
        main_group_view = '
                <div class="main-group-view">
                        view group <strong><%= name %></strong><br>
                         <div class="group-members-list">
                        </div>
                </div>
                '
                
        editor_template = '
                <div id="edit-status">Editing <%= name %>
                <div class="action-button" id="save-content">Save</div>
                </div>
                '
        listview_template = '
                <% var title = TrumpetApp.admin_usrmgr_tmpl.list_titles[type] %>
                <div class="listview-header"><%= title %>
                <div class="pull-right btn btn-default btn-xs add-entry-btn" id="new-entry-button"><i class="fa fa-plus-square"></i></div>
                </div>
                <div class="listview-list"></div>
                '
        create_template = '
                <div class="listview-header2">
                </div>
                <div class="create-form">
                        <div class="action-button" id="create-content">Save</div>
                        <span class="form-inline" style="white-space:nowrap">
                        <label class="form-inline" for="nameinput">Name</label>
                        <input style="width:80%" class="form-control form-inline pull-right" name="name" id="nameinput">
                        </span>
                </div>        
                '
        #######################################################
        admin_usrmgr_tmpl =
                list_titles: list_titles
                side_view:
                        new EJS text: side_view_template
                entry:
                        new EJS text: entry_template
                user_entry:
                        new EJS text: user_entry_template
                editor:
                        new EJS text: editor_template
                listview:
                        new EJS text: listview_template
                create:
                        new EJS text: create_template
                main_user_view:
                        new EJS text: main_user_view
                main_group_view:
                        new EJS text: main_group_view
                user_group_entry:
                        new EJS text: user_group_entry
                        
        
        TrumpetApp.admin_usrmgr_tmpl = admin_usrmgr_tmpl

        

        
                
