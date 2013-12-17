jQuery ->
        make_alert = TrumpetApp.make_alert
        
        fetch_success = (collection, response) ->
                make_alert('Succesful Transfer', 'success')
                
        fetch_error = (collection, response) ->
                make_alert('Error in Transfer', 'error')
                
        list_views = ->
                'path': SitePathListView
                'tmpl': SiteTemplateListView
                'css': SiteCSSListView
                'js': SiteJSListView

        # savebutton is jQuery object
        make_editor = (mtype, savebutton, content='') ->
                editor = ace.edit('editor')
                session = editor.getSession()
                session.setValue content
                session.on('change', () ->
                        savebutton.show()
                        )
                if mtype == 'tmpl'
                        session.setMode('ace/mode/ejs')
                else if mtype == 'css'
                        session.setMode('ace/mode/css')
                else if mtype == 'js'
                        session.setMode('ace/mode/javascript')
                editor.setTheme('ace/theme/twilight')
                return editor
                
                
                
        
        class Router extends Backbone.Router
                routes:
                        '': 'home'
                        'view/:listview': 'listview'

                common: ->
                        side_view.render()
                        if side_view.current_view != null
                                side_view.current_view.remove()


                home: ->
                        @common()

                listview: (lview) ->
                        @common()
                        klass = list_views()[lview]
                        view = new klass
                        view.render type: lview
                        side_view.current_view = view


        ########################################
        # Models
        ########################################
        class SitePath extends Backbone.Model
                defaults:
                        name: ''
                        type: 'path'
                        
        class SiteTemplate extends Backbone.Model
                defaults:
                        name: ''
                        content: ''
                        type: 'tmpl'
                        
        class SiteCSS extends Backbone.Model
                defaults:
                        name: ''
                        content: ''
                        type: 'css'
                        
        class SiteJS extends Backbone.Model
                defaults:
                        name: ''
                        content: ''
                        type: 'js'
                        

        ########################################
        # Collections
        ########################################
        class SitePathList extends Backbone.Collection
                model: SitePath
                url: '/rest/sitepath'
                # wrap the parsing to retrieve the
                # 'data' attribute from the json response
                parse: (response) ->
                        return response.data
                        
                
        class SiteTemplateList extends Backbone.Collection
                model: SiteTemplate
                url: '/rest/sitetmpl'
                # wrap the parsing to retrieve the
                # 'data' attribute from the json response
                parse: (response) ->
                        return response.data
                        
        class SiteCSSList extends Backbone.Collection
                model: SiteCSS
                url: '/rest/sitecss'
                # wrap the parsing to retrieve the
                # 'data' attribute from the json response
                parse: (response) ->
                        return response.data
                        
        class SiteJSList extends Backbone.Collection
                model: SiteJS
                url: '/rest/sitejs'
                # wrap the parsing to retrieve the
                # 'data' attribute from the json response
                parse: (response) ->
                        return response.data
                        
        ########################################
        # Views
        ########################################
        ########################################
        # Model Views for models
        ########################################
        class BaseModelView extends Backbone.View
                template: TrumpetApp.admin_mgr_tmpl.entry
                
                initialize: ->
                        _.bindAll @, 'render'
                        @model.bind 'change', @render
                        @model.bind 'remove', @unrender
                                
                render: ->
                        html = @template @model.attributes
                        this.$el.html html
                        return @

                unrender: ->
                        console.log('unrender ' + @model.attributes)
                        $(@el).remove()

                events:
                        'click .show-entry-btn': 'editme'
                        

                editme: ->
                        tmpl = TrumpetApp.admin_mgr_tmpl.editor
                        html = tmpl @model.attributes
                        el = $('.listview-list')
                        el.html html
                        
                        mtype = @model.get('type')
                        if mtype == 'path'
                                el.html "SHOW ME"
                                return @
                        button = $('#save-content')
                        content = @model.get 'content'
                        editor = make_editor mtype, button, content
                                
                        # setup save button
                        button.hide()
                        button.click =>
                                @model.set('content', editor.getValue())
                                response = @model.save()
                                response.done ->
                                        make_alert('Saved')
                                        $('#save-content').hide()
                                response.fail ->
                                        make_alert('Failed to save model')

                        # remove new entry button and replace it
                        # with delete button
                        nbutton = $('#new-entry-button')
                        nbutton.remove()
                        dbutton_html = '<div class="pull-right action-button del-entry-btn" id="del-entry-button">Delete</div>'
                        lvheader = $('.listview-header')
                        lvheader.append dbutton_html
                        confirm_div = '<div id="confirm-delete"><span class="ui-icon ui-icon-alert"></span>Delete this object?</div>'
                        $('.sidebar').append confirm_div
                        dbutton = $('#del-entry-button')
                        delete_model = =>
                                response = @model.destroy()
                                response.done ->
                                        make_alert 'Deleted ' + name
                                        pt = trigger: true, replace: true
                                        url = 'view/' + mtype
                                        main_router.navigate 'dummy', pt
                                        main_router.navigate url, pt
                                response.fail ->
                                        make_alert 'Failed to delete ' + name
                                        
                        dbutton.click =>
                                $('#editor').hide()
                                el = $('#confirm-delete')
                                el.dialog
                                        dialogClass: 'no-close'
                                        modal: true
                                        buttons:
                                                "delete": ->
                                                        $(this).dialog 'close'
                                                        delete_model()
                                                'cancel': ->
                                                        $(this).dialog 'close'
                                                        $('#editor').show()
                                                        
                                name = @model.get 'name'
                                                                
                                        
                        return @
                        
        ########################################
        # List Views for collections
        ########################################
        class BaseListView extends Backbone.View
                el: $ '.right-column-content'

                render: (data) ->
                        tmpl = TrumpetApp.admin_mgr_tmpl.listview
                        @$el.html tmpl(data)
                        return @
                        
                #http://stackoverflow.com/questions/10966440/recreating-a-removed-view-in-backbone-js
                remove: () ->
                        @undelegateEvents()
                        @$el.empty()
                        @stopListening()
                        return @
                        
                appendItem: (model) =>
                        view = new BaseModelView model: model
                        html = view.render(model).el
                        $('.listview-list').append html

                events:
                        'click .add-entry-btn': 'new_entry_view'

                new_entry_view: ->
                        mclass = @collection.model
                        model = new mclass()
                        tmpl = TrumpetApp.admin_mgr_tmpl.create
                        html = tmpl model.attributes
                        $('.listview-list').html html
                        mtype = model.get 'type'
                        button = $('#create-content')

                        editor = make_editor mtype, button, ''

                        # setup save button
                        button.hide()
                        button.click =>
                                model.set 'content', editor.getValue()
                                name = $('#nameinput').val()
                                model.set 'name', name
                                @collection.add model
                                response = model.save()
                                response.done ->
                                        msg = 'Created ' + name
                                        make_alert msg
                                response.fail ->
                                        msg = 'Failed to create ' + name
                                        make_alert msg
                                        
                        return @
                        
        class SitePathListView extends BaseListView
                initialize: ->
                        console.log('Init SitePathListView')
                        @collection = new SitePathList
                        @collection.bind 'add', @appendItem
                        @collection.fetch()

        class SiteTemplateListView extends BaseListView
                initialize: ->
                        console.log('Init SiteTemplateListView')
                        @collection = new SiteTemplateList
                        @collection.bind 'add', @appendItem
                        @collection.fetch()

        class SiteCSSListView extends BaseListView
                initialize: ->
                        console.log('Init SiteCSSListView')
                        @collection = new SiteCSSList
                        @collection.bind 'add', @appendItem
                        @collection.fetch()

        class SiteJSListView extends BaseListView
                initialize: ->
                        console.log('Init SiteJSListView')
                        @collection = new SiteJSList
                        @collection.bind 'add', @appendItem
                        @collection.fetch()


        class SitePathMainView extends Backbone.View

        class SitePathCssListView extends Backbone.View
                
                
        class SideView extends Backbone.View
                el: $ '.sidebar'

                initialize: ->
                        console.log('Init SideView')
                        @current_view = null
        
                template:
                        TrumpetApp.admin_mgr_tmpl.side_view
                        
                render: ->
                        $(@el).html @template()
                        return @


                # pull_trigger is to activate views
                # when the route changes
                pull_trigger = trigger: true, replace: true
                events:
                        'click .home-button': ->
                                main_router.navigate '', pull_trigger
                                
                        'click .sitepaths-button': ->
                                $('.listview-list').remove()
                                main_router.navigate 'dummy', pull_trigger
                                main_router.navigate 'view/path', pull_trigger
                                
                        'click .sitetmpl-button': ->
                                $('.listview-list').remove()
                                main_router.navigate 'dummy', pull_trigger
                                main_router.navigate 'view/tmpl', pull_trigger
                                
                        'click .sitecss-button': ->
                                $('.listview-list').remove()
                                main_router.navigate 'dummy', pull_trigger
                                main_router.navigate 'view/css', pull_trigger
                                
                        'click .sitejs-button': ->
                                $('.listview-list').remove()
                                main_router.navigate 'dummy', pull_trigger
                                main_router.navigate 'view/js', pull_trigger
                                
                        


                        
        window.main_router = new Router
        window.side_view = new SideView
                
                
        Backbone.history.start()
        
                
