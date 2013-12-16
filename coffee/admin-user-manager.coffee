jQuery ->

        list_views = ->
                'user': UserListView
                'group': GroupListView

        make_group_select_dlg = ->
                console.log("make_group_select_dlg")
                html = '<div id="select-group-dialog"></div>'
                page = $ '.main-content'
                page.append html
                dl = $ '#select-group-dialog'
                view = new GroupSelectView
                html = view.render
                dl.dialog
                        dialogClass: 'no-close'
                        modal: true
                        buttons:
                                'cancel': ->
                                        $(this).dialog 'close'
                                        dl.remove()
                                        
                #dl.append view.el
                                        
                
                                
                
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
        class User extends Supermodel.Model
                type: Backbone.HasMany
                relatedModel: 'Group'
                collectionType: 'UserList'
                
                defaults:
                        objtype: 'user'
                        
        class Group extends Backbone.RelationalModel
                defaults:
                        objtype: 'group'
















        ########################################
        # Collections
        ########################################
        class BaseCollection extends Backbone.Collection
                # wrap the parsing to retrieve the
                # 'data' attribute from the json response
                parse: (response) ->
                        return response.data
                
        class UserList extends BaseCollection
                model: User
                url: '/rest/users'

        class GroupList extends BaseCollection
                model: Group
                url: '/rest/groups'
                # wrap the parsing to retrieve the
                # 'data' attribute from the json response
                parse: (response) ->
                        return response.data

        make_ug_collection = (user_id) ->
                class uglist extends BaseCollection
                        model: Group
                        url: '/rest/users/' + user_id + '/groups'
                return new uglist


                
                
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
                        html = tmpl @model.attributes
                        #html = @template.render @model.attributes
                        this.$el.html html
                        return @

                unrender: ->
                        $(@el).remove()

                events:
                        'click .show-entry-btn': 'showentry'

                showentry: ->
                        el = $('.listview-list')
                        if @model.get('objtype') == 'user'
                                view = new MainUserView main_model: @model
                        else
                                view = new MainGroupView main_model: @model
                        html = view.render @model.attributes
                        el.html html
                        
        
        class BaseMainContentView extends Backbone.View
                el: $ '.right-column-content'
                                        
                remove: () ->
                        @undelegateEvents()
                        @$el.empty()
                        @stopListening()
                        return @

        class MainUserView extends BaseMainContentView
                render: (user) ->
                        tmpl = TrumpetApp.admin_usrmgr_tmpl.main_user_view
                        html = tmpl(user)
                        @$el.html html
                        uview = new UserGroupListView  user
                        return @
                                                                        
        class MainGroupView extends BaseMainContentView
                render: (group) ->
                        tmpl = TrumpetApp.admin_usrmgr_tmpl.main_group_view
                        @$el.html tmpl group
                        return @
                                                                        
        class BaseListView extends BaseMainContentView
                render: (data) ->
                        tmpl = TrumpetApp.admin_usrmgr_tmpl.listview
                        @$el.html tmpl data
                        return @

                modelView: BaseModelView

                
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
                        html = tmpl model.attributes
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

        class GroupSelectView extends Backbone.View
                el: $ '#select-group-dialog'
                                        
                initialize: ->
                        console.log('Init GroupSelectView')
                        @collection = new GroupList
                        @collection.bind 'add', @appendItem
                        @collection.fetch()

                remove: () ->
                        @undelegateEvents()
                        @$el.empty()
                        @stopListening()
                        return @
                        
                render: (data) ->
                        tmpl = TrumpetApp.admin_usrmgr_tmpl.listview
                        @$el.html tmpl.render data
                        return @

                modelView: BaseModelView

                
                appendItem: (model) =>
                        view = new @modelView model: model
                        html = view.render(model).el
                        $('#select-group-dialog').append html

        class UserGroupView extends Backbone.View
                template: TrumpetApp.admin_usrmgr_tmpl.entry

                initialize: ->
                        _.bindAll @, 'render'
                        @model.bind 'change', @render
                        @model.bind 'remove', @unrender

                render: ->
                        #html = @model.get 'name'
                        # FIXME This is a HACK
                        tmplbox = TrumpetApp.admin_usrmgr_tmpl
                        tmpl = tmplbox.user_group_entry
                        html = tmpl @model.attributes
                        this.$el.html html
                        # FIXME: I want to use the
                        # declarative events instead
                        # of implementing a callback here
                        addgrpbutton = $ '#addgroup'
                        addgrpbutton.click =>
                                this.add_group()
                        return @

                unrender: ->
                        $(@el).remove()
                        
                events:
                        'click .detach-group': 'detach_group'

                detach_group: ->
                        @model.destroy()
                        @unrender()
                        
                add_group: ->
                        console.log('add_group')
                        make_group_select_dlg()

                
        # this is part of MainUserView     
        class UserGroupListView extends Backbone.View
                el: $ '.user-group-list'
                
                initialize: (user) ->
                        #console.log('Init UserGroupListView ' + user.id)
                        @collection = make_ug_collection user.id
                        @collection.bind 'add', @appendItem
                        @collection.fetch()

                modelView: UserGroupView

                
                appendItem: (model) =>
                        view = new @modelView model: model
                        html = view.render(model).el
                        $('.user-group-list').append html

                        
                events:
                        'click #addgroup': 'add_group'
                        
                add_group: ->
                        console.log('add_group')
                        #make_group_select_dlg()







        ########################################
        # Side View
        ########################################
                        
        class SideView extends Backbone.View
                el: $ '.sidebar'

                initialize: ->
                        #console.log('Init SideView')
                        @current_view = null

                render: ->
                        tmpl = TrumpetApp.admin_usrmgr_tmpl.side_view
                        html = tmpl()
                        $(@el).html html
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
                
