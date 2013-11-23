$(document).ready ->


        #$('.article').midgardCreate()
        #$('body').data('midgardNotifications').showTutorial()
        #$('.article').midgardCreate('setEditorForProperty',
        #        'content', 'hallo')
        #$('.article').midgardCreate('configureEditor', 'title', 'halloWidget')

        $('.article').hallo ->
                toolbar: 'halloToolbarFixed'
                plugins:
                        halloformat: {}
        
        Backbone.sync = (method, model, options) ->
                if (console && console.log)
                        console.log("Model Contents", model.toJSONDL())
                $('.footer').text(model.toJSONDL())
                options.success(model)

        $('.fa-pencil').click ->
                if $(this).hasClass('fa-spin')
                        $(this).removeClass('fa-spin')
                        $(this).removeClass('fa-spinner')
                        $(this).addClass('fa-pencil')
                else
                        $(this).addClass('fa-spin')
                        $(this).removeClass('fa-pencil')
                        $(this).addClass('fa-spinner')
                $('.footer').text($(this).attr('class'))
                $('.hallotoolbar').toggle()
                        
