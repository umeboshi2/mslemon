// Generated by CoffeeScript 1.6.3
(function() {
  var __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
    __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  jQuery(function() {
    var EditSiteTextView, Router, SiteText, SiteTextList, SiteTextListView, SiteTextView, fetch_success, home_route_run, _ref, _ref1, _ref2, _ref3, _ref4, _ref5;
    fetch_success = function(collection, response) {
      return $('.header').text('success');
    };
    Router = (function(_super) {
      __extends(Router, _super);

      function Router() {
        _ref = Router.__super__.constructor.apply(this, arguments);
        return _ref;
      }

      Router.prototype.routes = {
        '': 'home'
      };

      return Router;

    })(Backbone.Router);
    SiteText = (function(_super) {
      __extends(SiteText, _super);

      function SiteText() {
        _ref1 = SiteText.__super__.constructor.apply(this, arguments);
        return _ref1;
      }

      SiteText.prototype.defaults = {
        type: 'tutwiki',
        name: '',
        content: '',
        created: '',
        modified: ''
      };

      return SiteText;

    })(Backbone.Model);
    SiteTextList = (function(_super) {
      __extends(SiteTextList, _super);

      function SiteTextList() {
        _ref2 = SiteTextList.__super__.constructor.apply(this, arguments);
        return _ref2;
      }

      SiteTextList.prototype.model = SiteText;

      SiteTextList.prototype.url = '/rest/sitetext';

      SiteTextList.prototype.parse = function(response) {
        return response.data;
      };

      return SiteTextList;

    })(Backbone.Collection);
    EditSiteTextView = (function(_super) {
      __extends(EditSiteTextView, _super);

      function EditSiteTextView() {
        this.unrender = __bind(this.unrender, this);
        this.render = __bind(this.render, this);
        _ref3 = EditSiteTextView.__super__.constructor.apply(this, arguments);
        return _ref3;
      }

      EditSiteTextView.prototype.tagName = 'div';

      EditSiteTextView.prototype.className = 'sitetext-entry';

      EditSiteTextView.prototype.initialize = function() {
        _.bindAll(this, 'render', 'unrender', 'remove');
        this.model.bind('change', this.render);
        return this.model.bind('remove', this.unrender);
      };

      EditSiteTextView.prototype.render = function() {
        $(this.el).html("<span>Name: " + (this.model.get('name')) + "</span>\n<span class=\"action-button save\">save</span>\n<span class=\"action-button delete\">delete</span>");
        return this;
      };

      EditSiteTextView.prototype.unrender = function() {
        return $(this.el).remove();
      };

      EditSiteTextView.prototype.remove = function() {
        return this.model.destroy();
      };

      EditSiteTextView.prototype.save = function() {
        return this.model.save();
      };

      EditSiteTextView.prototype.events = {
        'click .save': 'save'
      };

      return EditSiteTextView;

    })(Backbone.View);
    SiteTextView = (function(_super) {
      __extends(SiteTextView, _super);

      function SiteTextView() {
        this.unrender = __bind(this.unrender, this);
        this.renderForm = __bind(this.renderForm, this);
        this.render = __bind(this.render, this);
        _ref4 = SiteTextView.__super__.constructor.apply(this, arguments);
        return _ref4;
      }

      SiteTextView.prototype.tagName = 'div';

      SiteTextView.prototype.className = 'sitetext-entry';

      SiteTextView.prototype.initialize = function() {
        _.bindAll(this, 'render', 'unrender', 'remove');
        this.model.bind('change', this.render);
        return this.model.bind('remove', this.unrender);
      };

      SiteTextView.prototype.render = function() {
        $(this.el).html("<span>Name: " + (this.model.get('name')) + "</span>\n<span class=\"action-button edit\">edit</span>\n<span class=\"action-button delete\">delete</span>");
        return this;
      };

      SiteTextView.prototype.renderForm = function() {
        $(this.el).html("<div>\n<form>\n<label>Name:</label><input name=\"name\" value='" + (this.model.get('content')) + "'><br>\n<label>Content:</label><textarea type=\"textarea\" name=\"content\" width=\"60\" height=\"10\">" + (this.model.get('content')) + "</textarea>\n</form>\n</div>\n<span class=\"action-button save\">save</span>\n<span class=\"action-button delete\">delete</span>");
        return this;
      };

      SiteTextView.prototype.unrender = function() {
        return $(this.el).remove();
      };

      SiteTextView.prototype.remove = function() {
        return this.model.destroy();
      };

      SiteTextView.prototype.edit = function() {
        return this.renderForm();
      };

      SiteTextView.prototype.events = {
        'click .delete': 'remove',
        'click .edit': 'edit'
      };

      return SiteTextView;

    })(Backbone.View);
    SiteTextListView = (function(_super) {
      __extends(SiteTextListView, _super);

      function SiteTextListView() {
        _ref5 = SiteTextListView.__super__.constructor.apply(this, arguments);
        return _ref5;
      }

      SiteTextListView.prototype.el = $('.something');

      SiteTextListView.prototype.initialize = function() {
        console.log("Init SiteTextListView");
        this.counter = 0;
        this.collection = new SiteTextList;
        return this.collection.bind('add', this.appendItem);
      };

      SiteTextListView.prototype.render = function() {
        $(this.el).append('<div class="action-button fetch-site-text-button">Fetch Site Text</div>');
        $(this.el).append('<div class="action-button new-site-text-button">New Site Text</div>');
        return $(this.el).append('<div class="site-text-list"></div>');
      };

      SiteTextListView.prototype.addItem = function() {
        var item;
        this.counter++;
        item = new SiteText;
        return this.collection.add(item);
      };

      SiteTextListView.prototype.appendItem = function(sitetext) {
        var view;
        view = new SiteTextView({
          model: sitetext
        });
        return $('.site-text-list').append(view.render().el);
      };

      SiteTextListView.prototype.fetchItems = function() {
        var response;
        $('.header').text('foobar');
        return response = this.collection.fetch(function() {
          return {
            success: fetch_success
          };
        });
      };

      SiteTextListView.prototype.tellmereset = $('.header').text('tellmereset');

      SiteTextListView.prototype.events = {
        'click .new-site-text-button': 'addItem',
        'click .fetch-site-text-button': 'fetchItems'
      };

      return SiteTextListView;

    })(Backbone.View);
    window.list_view = new SiteTextListView;
    window.router = new Router;
    home_route_run = function() {
      console.log("Home Route");
      return window.list_view.render();
    };
    window.router.on('route:home', home_route_run);
    return Backbone.history.start();
  });

}).call(this);
