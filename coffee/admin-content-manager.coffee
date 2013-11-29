jQuery ->
        fetch_success = (collection, response) ->
                make_alert('Succesful Transfer', 'success')
                
        fetch_error = (collection, response) ->
                make_alert('Error in Transfer', 'error')
                
        list_views = ->
                'sitepath': SitePathListView
                'sitetmpl': SiteTemplateListView
                'sitecss': SiteCSSListView
                'sitejs': SiteJSListView
        window.lviews = list_views
        class Router extends Backbone.Router
                routes:
                        '': 'home'
                        'view/:listview': 'listview'
                        #'sitepath': 'sitepath'
                        #'/sitetmpl': 'sitetmpl'
                        #'sitecss' : 'sitecss'
                        #'sitejs' : 'sitejs'
                        #'/edit/{id}': 'edit'

                common: ->
                        side_view.render()
                        if side_view.current_view != null
                                side_view.current_view.remove()
                        $('.right-listview').remove()
                        div = '<div class="right-listview"></div>'
                        $('.right-column-content').html div
                        



                home: ->
                        #console.log('HOMEYYYYYYYYYYYY')
                        @common()

                listview: (lview) ->
                        @common()
                        klass = list_views()[lview]
                        view = new klass
                        view.render()
                        side_view.current_view = view
                        
                        
                sitepath: ->
                        @common()
                        #console.log('Hsdfsdfsdfsdfsdf')
                        view = new SitePathListView
                        view.render()
                        
                sitetmpl: ->
                        @common()
                        #console.log('Hsdfsdfsdfsdfsdf')
                        view = new SiteTemplateListView
                        view.render()
                        
                sitecss: ->
                        @common()
                        #console.log('Hsdfsdfsdfsdfsdf')
                        view = new SiteCSSListView
                        view.render()
                        
                sitejs: ->
                        @common()
                        #console.log('Hsdfsdfsdfsdfsdf')
                        view = new SiteJSListView
                        view.render()
                        


        ########################################
        # Models
        ########################################
        class SitePath extends Backbone.Model
                defaults:
                        name: ''
                
        class SiteTemplate extends Backbone.Model
                defaults:
                        name: ''
                        content: ''
                        
        class SiteCSS extends Backbone.Model
                defaults:
                        name: ''
                        content: ''
                        
        class SiteJS extends Backbone.Model
                defaults:
                        name: ''
                        content: ''
                        

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
                tagName: 'div'

        class SitePathView extends BaseModelView
                className: 'sitepath-entry'

                initialize: ->
                        _.bindAll @, 'render'
                        @model.bind 'change', @render
                        @model.bind 'remove', @unrender
                        

                template:
                        admin_mgr_tmpl.sitepath_entry_template

                render: ->
                        path = @model.get('name')
                        template = admin_mgr_tmpl.sitepath_entry_template
                        #$(@el).html template.render({path: path})
                        html = template.render({path: path})
                        this.$el.html html
                        #this.$el.click ->
                        #        $(this).addClass('action-button')
                        return @

                unrender: ->
                        $(@el).remove()

                events:
                        'click el': ->
                                $(@el).hide()
                        
                        
                        
                
        ########################################
        # List Views for collections
        ########################################
        class BaseListView extends Backbone.View
                #el: $ '.right-column-content'
                el: $ '.right-listview'
                
                render: (data) ->
                        @$el.html @template.render(data).el
                        #$(@el).html @template.render data
                        $('.right-column-content').append(@$el)
                        return @
                events:
                        'click .fetch-button': 'fetch'
                                        
        class SitePathListView extends BaseListView
                el: $ '.right-listview'
                
                template:
                        admin_mgr_tmpl.sitepath_view_template
                        
                initialize: ->
                        console.log('Init SitePathListView')
                        @collection = new SitePathList
                        @collection.bind 'add', @appendItem
                        @collection.fetch()

                addItem: ->
                        item = new SitePath
                        @collection.add item

                # we need the fat arrow to get $(el)
                # defined properly
                appendItem: (sitepath) =>
                        #make_alert('appended item' + sitepath)
                        view = new SitePathView model: sitepath
                        path = view.render(sitepath).el
                        #$(@el).append path
                        $('.listview-list').append path
                        
                fetch: =>
                        @collection.fetch()
                        
                                                
        class SiteTemplateListView extends BaseListView
                template:
                        admin_mgr_tmpl.sitetmpl_view_template
                        
                initialize: ->
                        console.log('Init SiteTemplateListView')

        class SiteCSSListView extends BaseListView
                template:
                        admin_mgr_tmpl.sitecss_view_template
                        
                initialize: ->
                        console.log('Init SiteCSSListView')

        class SiteJSListView extends BaseListView
                template:
                        admin_mgr_tmpl.sitejs_view_template
                        
                initialize: ->
                        console.log('Init SiteJSListView')


        class SideView extends Backbone.View
                el: $ '.sidebar'

                initialize: ->
                        console.log('Init SideView')
                        @current_view = null
        
                template:
                        admin_mgr_tmpl.side_view_template
                        
                render: ->
                        $(@el).html @template.render()
                        return @

                pathview:
                        new SitePathListView
                tmplview:
                        new SiteTemplateListView
                cssview:
                        new SiteCSSListView
                jsview:
                        new SiteJSListView
                        

                setup_sitepath_viewer: ->
                        @pathview.render()
                        
                setup_sitetmpl_viewer: ->
                        @tmplview.render()
                        
                setup_sitecss_viewer: ->
                        @cssview.render()

                setup_sitejs_viewer: ->
                        @jsview.render()
                        
                        
                events:
                        'click .sitepaths-button': ->
                                #main_router.navigate 'sitepath', trigger: true
                                main_router.navigate 'view/sitepath', trigger: true
                        'click .sitetmpl-button': ->
                                main_router.navigate 'view/sitetmpl', trigger: true
                                
                        'click .sitecss-button': 'setup_sitecss_viewer'
                        'click .sitejs-button': 'setup_sitejs_viewer'
                        





                        
        window.side_view = new SideView
        window.main_router = new Router
                
                
        Backbone.history.start()
        
                
