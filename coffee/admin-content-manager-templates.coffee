jQuery ->
    ########################################
    # Variables
    ########################################
    list_titles =
        path: 'Site Paths'
        tmpl: 'Site Templates'
        css: 'Site CSS'
        js: 'Site Javascript'
    
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
            div '.btn.btn-default.sitepaths-button', 'Paths'
            div '.btn.btn-default.sitetmpl-button', 'Templates'
            div '.btn.btn-default.sitecss-button', 'CSS'
            div '.btn.btn-default.sitejs-button', 'JS'
        
                        
    #######################################################
    entry_template = renderable (entry) ->
        div '.listview-list-entry', ->
            text entry.name
            div '.btn.btn-default.btn-xs.pull-right.show-entry-btn', ->
                icon '.fa.fa-pencil'
    #######################################################
    editor_template = renderable (model) ->
        div '#edit-status', ->
            text 'Editing ' + model.name
            div '#save-content.action-button', 'Save'
        div '#editor'
                
    listview_template = renderable (data) ->
        nbtn = '#new-entry-button.pull-right.btn.btn-default.btn-xs.add-entry-btn'                
        div '.listview-header', ->
            text list_titles[data.type]
            div nbtn, ->
                icon '.fa.fa-plus-square'
        div '.listview-list'
                
    create_template = renderable (model) ->
        _nameinput = '#nameinput.form-inline.form-control.pull-right'
        div '.create-form', ->
            div '#create-content.action-button', 'Save'
            span '.form-inline', style:'white-space:nowrap', ->
                label '.form-inline', for: 'nameinput', ->
                    text 'Name'
                input  _nameinput, style: 'width:80%', name: 'name'
            div '#edit-status'
            div '#editor'

    #######################################################
    admin_mgr_tmpl =
        side_view:
            side_view_template
        entry:
            entry_template
        editor:
            editor_template
        listview:
            listview_template
        create:
            create_template
        
    TrumpetApp.admin_mgr_tmpl = admin_mgr_tmpl

        

        
                
