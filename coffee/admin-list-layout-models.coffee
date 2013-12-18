$(document).ready ->
        $('.delete-confirm').hide()

        destroy_entry = (data, status, xhr) ->
                f = $.parseJSON(data)
                entry_id = 'entry-' + f.id
                if f.update == 'deleted'
                        $('#'+ entry_id).empty()
                        $('#'+ entry_id).remove()
                else
                        $('#'+ entry_id).empty()
                        msg = "There are pages using this resource."
                        $('#'+ entry_id).text(msg)

        delete_resource = (id) ->
                entry_id = 'entry-' + id
                #$('#'+ entry_id).hide()
                formdata =
                        update: 'delete'
                        id: id
                $.post(window.location, formdata, destroy_entry)
                
                
                

        $('.delete-button').click ->
                $(this).hide()
                btnid = $(this).attr('id').split('-')[1]
                div_id = 'div-confirm-' + btnid
                $('#'+ div_id).show()
                #$(this).children('.delete-confirm').show()
                #$('$this > .delete-confirm').show()

                       
        $('.cancel-button').click ->
                btnid = $(this).attr('id').split('-')[1]
                div_id = 'div-confirm-' + btnid
                $('#'+ div_id).hide()
                del_id = 'delete-' + btnid
                $('#'+ del_id).show()
                
                
        $('.confirm-button').click ->
                btnid = $(this).attr('id').split('-')[1]
                #div_id = 'div-confirm-' + ctype + '-' + btnid
                #$('#'+ div_id).hide()
                #del_id = 'delete-' + ctype + '-' + btnid
                #$('#'+ del_id).show()
                delete_resource(btnid)
                
        $('#save-content').click ->
                #$('#editor').toggle()
                $('header > h2').text(window.location)
                formdata =
                        update: "submit"
                        content: editor.getValue()
                post_to_url(window.location, formdata, 'post')
                $('header > h2').text("Posted")
                
