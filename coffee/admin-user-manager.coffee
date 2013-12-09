jQuery ->

        class Router extends Backbone.Router
                routes:
                        '': 'home'

                common: ->
                        s = TrumpetApp.side_view
                        s.render()
                        if s.current_view != null
                                s.current_view.remove()
                        
                home: ->
                        @common()


        ########################################
        # Models
        ########################################
        class User extends Backbone.Model
                defaults:
                        name: ''
                        type: 'user'
                        
        class Group extends Backbone.Model
                defaults:
                        name: ''
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
                model: User
                url: '/rest/groups'
                # wrap the parsing to retrieve the
                # 'data' attribute from the json response
                parse: (response) ->
                        return response.data

                         


        class SideView extends Backbone.View
                el: $ '.sidebar'

                initialize: ->
                        #console.log('Init SideView')
                        @current_view = null

                render: ->
                        $(@el).text 'Hello world!!!'
                        return @


                TrumpetApp.main_router = new Router
                TrumpetApp.side_view = new SideView

                Backbone.history.start()
                