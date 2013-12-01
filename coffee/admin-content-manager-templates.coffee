jQuery ->
        ########################################
        # Templates
        ########################################
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
        sitepath_view_template =
                """
                <div class="listview-header">Site Paths</div>
                <div class="listview-list"></div>
                """

        sitepath_entry_template =
                """
                        <div class="listview-list-entry" id="sitepath-<%= id %>">
                        <%= name %>
                        <div class="pull-right action-button show-sitepath-btn">show</div>
                </div>
                """
        #######################################################
        sitetmpl_view_template =
                """
                <div class="listview-header">Site Templates</div>
                <div class="listview-list"></div>
                """
        sitetmpl_entry_template =
                """
                <div class="listview-list-entry">
                        <%= name %>
          <div class="pull-right action-button show-sitetmpl-btn">show</div>
                </div>
                """
        #######################################################
        sitecss_view_template =
                """
                <div class="listview-header">Site CSS</div>
                <div class="listview-list"></div>
                """
        #######################################################
        sitejs_view_template =
                """
                <div class="listview-header">Site Javascript</div>
                <div class="listview-list"></div>
                """
        #######################################################
        admin_mgr_tmpl =
                side_view_template:
                        new EJS text: side_view_template
                sitepath_view_template:
                        new EJS text: sitepath_view_template
                sitepath_entry_template:
                        new EJS text: sitepath_entry_template
                sitetmpl_view_template:
                        new EJS text: sitetmpl_view_template
                sitetmpl_entry_template:
                        new EJS text: sitetmpl_entry_template
                sitecss_view_template:
                        new EJS text: sitecss_view_template
                sitejs_view_template:
                        new EJS text: sitejs_view_template
        window.TrumpetApp = {}
        TrumpetApp.admin_mgr_tmpl = admin_mgr_tmpl

        

        
                
