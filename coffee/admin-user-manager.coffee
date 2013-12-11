jQuery ->

        list_views = ->
                'user': UserListView
                'group': GroupListView
                
        class Router extends Backbone.Router
                routes:
                        '': 'home'
                        'view/:listview': 'listview'

                common: ->
                        s = side_view
                        s.render()
                        if s.current_view != null
                                s.current_view.remove()
                        
                home: ->
                        @common()

                listview: (lview) ->
                        @common()
                        console.log('lview is ' + lview)
                        klass = list_views()[lview]
                        # FIXME debug
                        window.klass = klass
                        view = new klass
                        view.render type: lview
                        side_view.current_view = view
                        
        ########################################
        # Models
        ########################################
        class User extends Backbone.Model
                defaults:
                        type: 'user'
                        
        class Group extends Backbone.Model
                defaults:
                        type: 'group'

        ########################################
        # Collections
        ########################################
        class UserList extends Backbone.Collection
                model: User
                url: '/rest/users'
                # wrap the parsing to retrieve the
                # 'data' attribute from the json response
                parse: (response) ->
                        return response.data

        class GroupList extends Backbone.Collection
                model: Group
                url: '/rest/groups'
                # wrap the parsing to retrieve the
                # 'data' attribute from the json response
                parse: (response) ->
                        return response.data

                         
        ########################################
        # Views
        ########################################
        class BaseModelView extends Backbone.View
                template: TrumpetApp.admin_usrmgr_tmpl.entry

                initialize: ->
                        _.bindAll @, 'render'
                        @model.bind 'change', @render
                        @model.bind 'remove', @unrender

                render: ->
                        # FIXME This is a HACK
                        # we are using one entry template
                        # for both models.  The User db
                        # object should really have a 'name'
                        # attribute, rather than 'username',
                        # but that will be done later.  For
                        # now, there needs to be work done
                        # on using abstract backbone 'classes'
                        # upon different model types.
                        tmplbox = TrumpetApp.admin_usrmgr_tmpl
                        if @model.has 'username'
                                tmpl = tmplbox.user_entry
                        else
                                tmpl = tmplbox.entry
                                
                        #@model.set 'name', @model.get 'username'
                        html = tmpl.render @model.attributes
                        #html = @template.render @model.attributes
                        this.$el.html html
                        return @

                unrender: ->
                        $(@el).remove()

                events:
                        'click .show-entry-btn': 'showentry'

                showentry: ->
                        el = $('.listview-list')
                        el.html "HEllo"
                        
        
        class BaseListView extends Backbone.View
                el: $ '.right-column-content'

                render: (data) ->
                        tmpl = TrumpetApp.admin_usrmgr_tmpl.listview
                        @$el.html tmpl.render data
                        return @

                modelView: BaseModelView

                
                remove: () ->
                        @undelegateEvents()
                        @$el.empty()
                        @stopListening()
                        return @

                appendItem: (model) =>
                        view = new @modelView model: model
                        html = view.render(model).el
                        $('.listview-list').append html

                events:
                        'click .add-entry-btn': 'new_entry_view'

                new_entry_view: ->
                        mclass = @collection.model
                        model = new mclass()
                        tmpl = TrumpetApp.admin_usrmgr_tmpl.create
                        html = tmpl.render model.attributes
                        $('.listview-list').html html
                        
        class UserListView extends BaseListView
                initialize: ->
                        console.log('Init UserListView')
                        @collection = new UserList
                        @collection.bind 'add', @appendItem
                        @collection.fetch()

                appendItem: (model) =>
                        view = new @modelView model: model
                        # FIXME
                        window.mbview = view
                        html = view.render(model).el
                        $('.listview-list').append html
                
        class GroupListView extends BaseListView
                initialize: ->
                        console.log('Init GroupListView')
                        @collection = new GroupList
                        @collection.bind 'add', @appendItem
                        @collection.fetch()
                        
        class SideView extends Backbone.View
                el: $ '.sidebar'

                initialize: ->
                        #console.log('Init SideView')
                        @current_view = null

                render: ->
                        tmpl = TrumpetApp.admin_usrmgr_tmpl.side_view
                        $(@el).html tmpl.render()
                        return @

                # pull_trigger is to activate views
                # when the route changes
                pull_trigger = trigger: true, replace: true
                events:
                        'click .home-button': ->
                                main_router.navigate '', pull_trigger
                                
                        'click .users-button': ->
                                $('.listview-list').remove()
                                main_router.navigate 'dummy', pull_trigger
                                main_router.navigate 'view/user', pull_trigger
                                
                        'click .groups-button': ->
                                $('.listview-list').remove()
                                main_router.navigate 'dummy', pull_trigger
                                main_router.navigate 'view/group', pull_trigger
                                

        main_router = new Router
        side_view = new SideView

        Backbone.history.start()
                