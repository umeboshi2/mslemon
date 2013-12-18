jQuery ->
    get_template = TrumpetApp.get_template
        
    show_template = get_template('show-site-template-ejs')
    window.show_template = show_template

    edit_template = get_template('edit-site-template-ejs')
    window.edit_template = edit_template

    list_template = get_template('list-sitetext-entries')
    window.list_template = list_template
        
    fetch_success = (collection, response) ->
        make_alert('Succesful Transfer', 'success')
                
    fetch_error = (collection, response) ->
        make_alert('Error in Transfer', 'error')
                

    class Router extends Backbone.Router
        routes:
            '': 'home'
            '/edit/{id}': 'edit'
                        
                
    class SiteText extends Backbone.Model
        defaults:
            type: 'tutwiki'
            name: ''
            content: ''
                        
                        

    class SiteTextList extends Backbone.Collection
        model: SiteText
        url: '/rest/sitetext'
        # wrap the parsing to retrieve the
        # 'data' attribute from the json response
        parse: (response) ->
            return response.data
                        

    class EditSiteTextView extends Backbone.View
        el: $ '.ace-editor'
                
        initialize: ->
            #_.bindAll @, 'render', 'unrender', 'remove'
            @model.bind 'change', @render
            @model.bind 'remove', @unrender

        render: =>
            $('.something').hide()
            name = @model.get('name')
            html = edit_template.render({name:name})
            $(@el).html html
            # startup editor
            @editor = ace.edit('editor')
            @editor.getSession().setMode('ace/mode/markdown')
            @editor.setTheme('ace/theme/cobalt')
            content = @model.get('content')
            @editor.setValue(content)
            window.editor = @editor
            return @

        unrender: =>
            $(@el).remove()

        remove: ->
            @model.destroy()

        save: ->
            content = @editor.getValue()
            @model.set('name', $('input').val())
            @model.set('content', content)
            @model.save()
            @unrender()
            $('#site-text-editor').remove()
            $('.something').show()
                        
        events:
            'click .save': 'save'
                
    class SiteTextView extends Backbone.View
        tagName: 'div'
        className: 'sitetext-entry'
                
        initialize: ->
            #_.bindAll @, 'render', 'unrender', 'remove'
            @model.bind 'change', @render
            @model.bind 'remove', @unrender
            $(@el).addClass('listview-list-entry')

        render: =>
            name = @model.get('name')
            content = show_template.render({name:name})
            $(@el).html content
            return @

        renderForm: =>
            @editor = new EditSiteTextView model: @model
            @editor.render()
            return @
                        
        unrender: =>
            $(@el).remove()

        remove: ->
            @model.destroy()
        
        edit: ->
            @renderForm()
          
        save: ->
            content = $('textarea').val()
            @model.set('name', $('input').val())
            @model.set('content', content)
            @model.save()
                        
        events:
            'click .delete': 'remove'
            'click .edit': 'edit'
            'click .save': 'save'
        
    class SiteTextListView extends Backbone.View
        el: $ '.site-text-list'

        initialize: ->
            console.log("Init SiteTextListView")
            @counter = 0
            @collection = new SiteTextList
            @collection.bind 'add', @appendItem
                        
        render: ->
            html = list_template.render()
            $(@el).html html
            return @
                        
                           
        addItem: ->
            @counter++
            item = new SiteText
            @collection.add item

        appendItem: (sitetext) ->
            view = new SiteTextView model: sitetext
            $('.site-text-list').append view.render().el
    
        fetchItems: ->
            @collection.fetch 
            success: fetch_success
                                
        events:
            'click .new-site-text-button': 'addItem'
            'click .fetch-site-text-button': 'fetchItems'
                        

                
                                                
                        
    window.list_view = new SiteTextListView
    window.router = new Router
    home_route_run = () ->
        console.log("Home Route")
        window.list_view.render()
                
    window.router.on 'route:home', home_route_run

    Backbone.history.start()
        
                
