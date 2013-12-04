jQuery ->
        fetch_success = (collection, response) ->
                make_alert('Succesful Transfer', 'success')
                
        fetch_error = (collection, response) ->
                make_alert('Error in Transfer', 'error')
                
        list_views = ->
                'path': SitePathListView
                'tmpl': SiteTemplateListView
                'css': SiteCSSListView
                'js': SiteJSListView
        # FIXME: attached to window for testing
        window.lviews = list_views
        
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
                template: TrumpetApp.admin_mgr_tmpl.entry_template
                
                initialize: ->
                        _.bindAll @, 'render'
                        @model.bind 'change', @render
                        @model.bind 'remove', @unrender
                                
                render: ->
                        html = @template.render @model.attributes
                        this.$el.html html
                        return @

                unrender: ->
                        $(@el).remove()

                events:
                        'click .show-entry-btn': 'editme'
                        

                editme: ->
                        tmpl = TrumpetApp.admin_mgr_tmpl.editor_template
                        html = tmpl.render @model.attributes
                        el = $('.listview-list')
                        el.html html

                        # make save button
                        save_btn = $('#save-content')
                        save_btn.hide()
                        save_btn.click =>
                                @model.set('content', editor.getValue())
                                response = @model.save()
                                response.done ->
                                        make_alert('Saved')
                                        $('#save-content').hide()
                                response.fail ->
                                        make_alert('Failed to save model')

                        # make editor
                        editor = ace.edit('editor')
                        session = editor.getSession()
                        session.setValue @model.get 'content'
                        session.on('change', () ->
                                $('#save-content').show()
                                )
                        # set editor properties based
                        # on model type
                        mtype = @model.get('type')
                        if mtype == 'path'
                                el.html "SHOW ME"
                        else if mtype == 'tmpl'
                                session.setMode('ace/mode/ejs')
                        else if mtype == 'css'
                                session.setMode('ace/mode/css')
                        else if mtype == 'js'
                                session.setMode('ace/mode/javascript')
                        else
                                el.html "Bad type" + mtype
                        editor.setTheme('ace/theme/twilight')
                        return @
                        
        ########################################
        # List Views for collections
        ########################################
        class BaseListView extends Backbone.View
                el: $ '.right-column-content'

                render: (data) ->
                        tmpl = TrumpetApp.admin_mgr_tmpl.listview_template
                        @$el.html tmpl.render(data)
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
                        html = "Make new Entry " + model.get 'type'
                        $('.listview-list').html html
                        
                        
                        
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


        class SideView extends Backbone.View
                el: $ '.sidebar'

                initialize: ->
                        console.log('Init SideView')
                        @current_view = null
        
                template:
                        TrumpetApp.admin_mgr_tmpl.side_view_template
                        
                render: ->
                        $(@el).html @template.render()
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
        
                
