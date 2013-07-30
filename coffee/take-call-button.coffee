$(document).ready ->
        $('#take-call-button').click ->
                url = $('#take-call-url').val()
                window.location = url
                