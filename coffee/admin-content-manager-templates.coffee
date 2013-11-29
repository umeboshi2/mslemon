jQuery ->
        ########################################
        # Templates
        ########################################
        side_view_template =
                """
                <div class="main-content-manager-view">
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
                <div class="listview-list-entry">
                        <%= path %>
                        <div class="action-button">show</div>
                </div>
                """
        #######################################################
        sitetmpl_view_template =
                """
                (INSERT TEMPLATE CONTENT HERE)
                """
        #######################################################
        sitecss_view_template =
                """
                (INSERT CSS CONTENT HERE)
                """
        #######################################################
        sitejs_view_template =
                """
                (INSERT JAVASCRIPT CONTENT HERE)
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
                sitecss_view_template:
                        new EJS text: sitecss_view_template
                sitejs_view_template:
                        new EJS text: sitejs_view_template
        window.admin_mgr_tmpl = admin_mgr_tmpl


        
                
