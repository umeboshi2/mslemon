jQuery ->
        class Item extends Backbone.Model
                defaults:
                        part1: 'Hello'
                        part2: 'Backbone'

        class List extends Backbone.Collection
                model: Item

        class ItemView extends Backbone.View
                tagName: 'li'

                initialize: ->
                        _.bindAll(@, 'render', 'unrender', 'swap', 'remove')
                        @model.bind 'change', @render
                        @model.bind 'remove', @unrender
                        
                        
                render: =>
                        $(@el).html """
                          <span>#{@model.get 'part1'} #{@model.get 'part2'}!</span>
                          <span class="action-button swap">swap</span>
                          <span class="action-button delete">delete</span>
                        """
                        return @

                unrender: =>
                        $(@el).remove()

                swap: ->
                        @model.set
                                part1: @model.get 'part2'
                                part2: @model.get 'part1'

                remove: ->
                        @model.destroy()
                        
                events:
                        'click .swap': 'swap'
                        'click .delete': 'remove'
                        
        
        class ListView extends Backbone.View
                el: $ '.something'

                initialize: ->
                        #_.bindAll.apply [this].concat _.functions @
                        #_.bindAll.apply [@].concat _.functions @
                        #_.bindAll (@, @appendItem, @addItem, @render)
                        #_.bindAll [@].concat [@appendItem, @addItem]
                        _.bindAll(@, 'appendItem', 'addItem', 'render')
                        @collection = new List
                        @collection.bind 'add', @appendItem
                        
                        @counter = 0
                        @render()

                render: ->
                        $(@el).append '<button class="action-button">Add</button>'
                        $(@el).append '<ul class="mylist"></ul>'

                addItem: ->
                        @counter++
                        item = new Item
                        item.set part2: "#{item.get 'part2'} #{@counter}"
                        @collection.add item

                appendItem: (item) ->
                        item_view = new ItemView model: item
                        $('.mylist').append item_view.render().el
                        

                events: 'click button': 'addItem'

        Backbone.sync = (method, model, success, error) ->
                success()

        list_view = new ListView
        