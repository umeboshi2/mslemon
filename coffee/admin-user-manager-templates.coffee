jQuery ->
    ########################################
    # Variables
    ########################################
    list_titles =
        user: 'Users'
        group: 'Groups'


    #{renderable, ul, li, input, div} = require 'teacup'
    renderable = teacup.renderable

    div = teacup.div
    icon = teacup.i
    strong = teacup.strong
    span = teacup.span
    label = teacup.label
    input = teacup.input
        
    text = teacup.text
    
    ########################################
    # Templates
    ########################################
    side_view_template = renderable () ->
        div '.main-content-manager-view.btn-group-vertical', ->
            div '.btn.btn-default.home-button', 'Main'
            div '.btn.btn-default.users-button', 'Users'
            div '.btn.btn-default.groups-button', 'Groups'
                                

    _btnclass = '.btn.btn-default.btn-xs.pull-right.show-entry-btn'
        
    entry_template = renderable (atts) ->
        div '.listview-list-entry', ->
            text atts.name
            div _btnclass, ->
                icon '.fa.fa-folder-open'
                                
                
    user_entry_template = renderable (atts) ->
        div '.listview-list-entry', ->
            text atts.username
            div _btnclass, ->
                icon '.fa.fa-folder-open'

    create_template = renderable () ->
        _nameinput = '#nameinput.form-inline.form-control.pull-right'
        div '.create-form', ->
            div '#create-content.action-button', ->
                text 'Save'
            span '.form-inline', style:'white-space:nowrap', ->
                label '.form-inline', for: 'nameinput', ->
                    text 'Name'
                input  _nameinput, style: 'width:80%', name: 'name'
                                
                                        
    #######################################################
    _addgroup = '#addgroup.btn.btn-default.btn-xs.pull-right'
    main_user_view = renderable (user) ->
        div '.main-user-view', ->
            text 'view user '
            strong user.username
            div '.listview-header', ->
                text "Groups for " + user.username
                # add group button
                div _addgroup, ->
                    text "Add Group"
            div '.listview-list.user-group-list'
            
    user_group_entry = renderable (group) ->
        div ->
            text group.name
            div '.detach-group.btn.btn-default.btn-xs', ->
                text "remove"
                                
    main_group_view = renderable (group) ->
                div '.main-group-view', ->
                    div '.listview-header', ->
                        text 'view group '
                        strong group.name
                    div '.listview-list.group-members-list'

    listview_template = renderable (data) ->
        nbtn = '#new-entry-button.pull-right.btn.btn-default.btn-xs.add-entry-btn'
        div '.listview-header', ->
            text list_titles[data.type]
            div nbtn, ->
                icon '.fa.fa-plus-square'
        div '.listview-list'
                
                        
    #######################################################
    admin_usrmgr_tmpl =
        side_view:
            side_view_template
        entry:
            entry_template
        user_entry:
            user_entry_template
        create:
            create_template
        listview:
            listview_template
        main_user_view:
            main_user_view
        main_group_view:
            main_group_view
        user_group_entry:
            user_group_entry
        
        
    TrumpetApp.admin_usrmgr_tmpl = admin_usrmgr_tmpl

        

        

                                
