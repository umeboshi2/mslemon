// Generated by CoffeeScript 1.6.3
(function() {
  $(document).ready(function() {
    $('.article').hallo(function() {
      return {
        toolbar: 'halloToolbarFixed',
        plugins: {
          halloformat: {}
        }
      };
    });
    Backbone.sync = function(method, model, options) {
      if (console && console.log) {
        console.log("Model Contents", model.toJSONDL());
      }
      $('.footer').text(model.toJSONDL());
      return options.success(model);
    };
    return $('.fa-pencil').click(function() {
      if ($(this).hasClass('fa-spin')) {
        $(this).removeClass('fa-spin');
        $(this).removeClass('fa-spinner');
        $(this).addClass('fa-pencil');
      } else {
        $(this).addClass('fa-spin');
        $(this).removeClass('fa-pencil');
        $(this).addClass('fa-spinner');
      }
      $('.footer').text($(this).attr('class'));
      return $('.hallotoolbar').toggle();
    });
  });

}).call(this);
