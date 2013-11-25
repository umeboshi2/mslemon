jQuery ->
        fetch_success = (collection, response) ->
                $('.header').text('success')

        class Router extends Backbone.Router
                routes:
                        '': 'home'
                        
                
        class SiteText extends Backbone.Model
                defaults:
                        type: 'tutwiki'
                        name: ''
                        content: ''
                        # do we need these?
                        created: ''
                        modified: ''
                        

        class SiteTextList extends Backbone.Collection
                model: SiteText
                url: '/rest/sitetext'
                # wrap the parsing to retrieve the
                # 'data' attribute from the json response
                parse: (response) ->
                        return response.data
                        

        class EditSiteTextView extends Backbone.View
                tagName: 'div'
                className: 'sitetext-entry'
                
                initialize: ->
                        _.bindAll @, 'render', 'unrender', 'remove'
                        @model.bind 'change', @render
                        @model.bind 'remove', @unrender

                render: =>
                        $(@el).html """
                          <span>Name: #{@model.get 'name'}</span>
                          <span class="action-button save">save</span>
                          <span class="action-button delete">delete</span>
                        """
                        return @

                unrender: =>
                        $(@el).remove()

                remove: ->
                        @model.destroy()

                save: ->
                        @model.save()
                events:
                        'click .save': 'save'
                
        class SiteTextView extends Backbone.View
                tagName: 'div'
                className: 'sitetext-entry'
                
                initialize: ->
                        _.bindAll @, 'render', 'unrender', 'remove'
                        @model.bind 'change', @render
                        @model.bind 'remove', @unrender

                render: =>
                        $(@el).html """
                          <span>Name: #{@model.get 'name'}</span>
                          <span class="action-button edit">edit</span>
                          <span class="action-button delete">delete</span>
                        """
                        return @

                renderForm: =>
                        $(@el).html """
                          <div>
                          <form>
                          <label>Name:</label><input name="name" value='#{@model.get 'name'}'><br>
                          <label>Content:</label><textarea type="textarea" name="content" width="60" height="10">#{@model.get 'content'}</textarea>
                          </form>
                          </div>
                          <span class="action-button save">save</span>
                          <span class="action-button delete">delete</span>
                        """
                        return @
                        
                unrender: =>
                        $(@el).remove()

                remove: ->
                        @model.destroy()

                edit: ->
                        @renderForm()
          
                saveOrig: ->
                        @model.set('name', $('input').val())
                        @model.set('content', $('textarea').val())
                        @model.save()

                                                
                save: ->
                        content = $('textarea').val()
                        #$('.footer').text(content)
                        @model.set('name', $('input').val())
                        @model.set('content', content)
                        @model.save()
                        
                        
                events:
                        'click .delete': 'remove'
                        'click .edit': 'edit'
                        'click .save': 'save'
        
        class SiteTextListView extends Backbone.View
                el: $ '.something'

                initialize: ->
                        console.log("Init SiteTextListView")
                        @counter = 0
                        @collection = new SiteTextList
                        @collection.bind 'add', @appendItem
                        # fetch routine
                                                                                
                        
                render: ->
                        $(@el).append '<div class="action-button fetch-site-text-button">Fetch Site Text</div>'
                        $(@el).append '<div class="action-button new-site-text-button">New Site Text</div>'
                        $(@el).append '<div class="site-text-list"></div>'

                addItem: ->
                        @counter++
                        item = new SiteText
                        @collection.add item

                appendItem: (sitetext) ->
                        view = new SiteTextView model: sitetext
                        $('.site-text-list').append view.render().el

                fetchItems: ->
                        $('.header').text('foobar')
                        response = @collection.fetch ->
                                success: fetch_success
                        #item = @collection.get(1)
                        #@appendItem @collection.get 1
                        #@appendItem item
                        #bbitem = new SiteText
                        #bbitem.set(item)
                        #@appendItem bbitem
                        #$('.footer').text(_.values bbitem.attributes)
                                


                tellmereset:
                        $('.header').text('tellmereset')
                        
                events:
                        'click .new-site-text-button': 'addItem'
                        'click .fetch-site-text-button': 'fetchItems'
                        

                
                                                
                        
        #Backbone.sync = (method, model, success, error) ->
        #        #$('.header').text(method)
        #        $('.header').text(success)

        window.list_view = new SiteTextListView
        window.router = new Router
        home_route_run = () ->
                console.log("Home Route")
                window.list_view.render()
                
        window.router.on 'route:home', home_route_run

        Backbone.history.start()
        
                