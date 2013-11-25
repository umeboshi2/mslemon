jQuery ->
        class SiteText extends Backbone.Model
                defaults:
                        type: 'tutwiki'
                        name: ''
                        content: ''
                        

        class SiteTextList extends Backbone.Collection
                model: SiteText
                url: '/rest/sitetext'
        
        class SiteTextView extends Backbone.View
                tagName: 'div'
                className: 'sitetext-entry'
                
                initialize: ->
                        _.bindAll @, 'render', 'unrender', 'remove'
                        @model.bind 'change', @render
                        @model.bind 'remove', @unrender

                render: =>
                        $(@el).html """
                          <div>Name: #{@model.get 'name'}</div>
                          <div>Content: #{@model.get 'content'}</div>
                          <span class="action-button delete">delete</span>
                        """
                        return @

                unrender: =>
                        $(@el).remove()

                remove: ->
                        @model.destroy()

                events:
                        'click .delete': 'remove'
                        
        
        class SiteTextListView extends Backbone.View
                el: $ '.something'

                initialize: ->
                        @collection = new SiteTextList
                        @collection.bind 'add', @appendItem
                        @counter = 0
                        @render()
                        
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
                        item = @collection.get(1)
                        #@appendItem @collection.get 1
                        #@appendItem item
                        bbitem = new SiteText item
                        bbitem.set(item)
                        @appendItem bbitem
                        $('.footer').text(_.keys bbitem.attributes)
                                

                                
                events:
                        'click .new-site-text-button': 'addItem'
                        'click .fetch-site-text-button': 'fetchItems'

                
                                                
                        
        Backbone.sync = (method, model, success, error) ->
                $('.header').text(method)
                

        list_view = new SiteTextListView
        