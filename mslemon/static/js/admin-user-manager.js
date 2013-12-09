// Generated by CoffeeScript 1.6.3
(function() {
  var __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  jQuery(function() {
    var Group, GroupList, Router, SideView, User, UserList, _ref, _ref1, _ref2, _ref3, _ref4, _ref5;
    Router = (function(_super) {
      __extends(Router, _super);

      function Router() {
        _ref = Router.__super__.constructor.apply(this, arguments);
        return _ref;
      }

      Router.prototype.routes = {
        '': 'home'
      };

      Router.prototype.common = function() {
        var s;
        s = TrumpetApp.side_view;
        s.render();
        if (s.current_view !== null) {
          return s.current_view.remove();
        }
      };

      Router.prototype.home = function() {
        return this.common();
      };

      return Router;

    })(Backbone.Router);
    User = (function(_super) {
      __extends(User, _super);

      function User() {
        _ref1 = User.__super__.constructor.apply(this, arguments);
        return _ref1;
      }

      User.prototype.defaults = {
        name: '',
        type: 'user'
      };

      return User;

    })(Backbone.Model);
    Group = (function(_super) {
      __extends(Group, _super);

      function Group() {
        _ref2 = Group.__super__.constructor.apply(this, arguments);
        return _ref2;
      }

      Group.prototype.defaults = {
        name: '',
        type: 'group'
      };

      return Group;

    })(Backbone.Model);
    UserList = (function(_super) {
      __extends(UserList, _super);

      function UserList() {
        _ref3 = UserList.__super__.constructor.apply(this, arguments);
        return _ref3;
      }

      UserList.prototype.model = User;

      UserList.prototype.url = '/rest/users';

      UserList.prototype.parse = function(response) {
        return response.data;
      };

      return UserList;

    })(Backbone.Collection);
    GroupList = (function(_super) {
      __extends(GroupList, _super);

      function GroupList() {
        _ref4 = GroupList.__super__.constructor.apply(this, arguments);
        return _ref4;
      }

      GroupList.prototype.model = User;

      GroupList.prototype.url = '/rest/groups';

      GroupList.prototype.parse = function(response) {
        return response.data;
      };

      return GroupList;

    })(Backbone.Collection);
    return SideView = (function(_super) {
      __extends(SideView, _super);

      function SideView() {
        _ref5 = SideView.__super__.constructor.apply(this, arguments);
        return _ref5;
      }

      SideView.prototype.el = $('.sidebar');

      SideView.prototype.initialize = function() {
        return this.current_view = null;
      };

      SideView.prototype.render = function() {
        $(this.el).text('Hello world!!!');
        return this;
      };

      TrumpetApp.main_router = new Router;

      TrumpetApp.side_view = new SideView;

      Backbone.history.start();

      return SideView;

    })(Backbone.View);
  });

}).call(this);
