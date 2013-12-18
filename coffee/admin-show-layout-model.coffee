$(document).ready ->
        #ab = $ '.action-button'
        #ab.text 'Action Button'
        renderable = teacup.renderable

        div = teacup.div
        icon = teacup.i
        strong = teacup.strong
        span = teacup.span
        label = teacup.label
        input = teacup.input
        
        text = teacup.text

        header_template = renderable (content) ->
                div '.btn.btn-default.btn-xs', ->
                        text content
                        

        $('.edit-button').click ->
                btnid = $(this).attr('id')
                elist = btnid.split('-')
                id = elist[1]
                oldtext = $('.header').text()
                if oldtext == 'Ms. Lemon'
                        $('.header').html header_template('FOoo-' + id)
                else
                        $('.header').html header_template('Ms. Lemon')
        
        $('#attach-css-button').click ->
                url = $(this).attr('href')
                window.location = url
                $(this).hide()

        $('#attach-js-button').click ->
                url = $(this).attr('href')
                window.location = url
                $(this).hide()

        $('.detach-button').click ->
                btnid = $(this).attr('id')
                url = $(this).attr('href')
                elist = btnid.split('-')
                ctype = elist[1]
                #path_id = new Number(elist[2])
                #obj_id = new Number(elist[3])
                detach_id = elist[2] + '-' + elist[3]
                $('header > h2').text(ctype + '-' + detach_id)
                window.location = url