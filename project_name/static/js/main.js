(function($, window, undefined) {
  'use strict';

  var g = APP.global = {};
  var collections = APP.collections = {};
  var models = APP.models = {};
  var utils = APP.utils = {};
  var views = APP.views = {};

  utils.ViewManager = function(el) {
    this.el = el;
    this.$el = $(el);
    this.current = null;

    this.on('change', this.onchange, this);
  };
  _.extend(utils.ViewManager.prototype, Backbone.Events, {
    onchange: function() {
      if (this.current && this.current.close) {
        this.current.close();
      }
    },

    html: function(obj) {
      this.trigger('change');

      this.current = null;
      this.$el.html(obj);
    },

    show: function(view) {
      this.trigger('change');

      this.current = view;
      this.current.render();

      this.$el.html(this.current.el);
    }
  });

  utils.get_template = function(idsuffix) {
    if (! g.template_cache) {
      g.template_cache = {};
    }
    if (! g.template_cache[idsuffix]) {
      g.template_cache[idsuffix] = _.template(
        document.getElementById('template-' + idsuffix).innerHTML
      );
    }
    return g.template_cache[idsuffix];
  };

  collections.Base = Backbone.Collection.extend({
    url: API.v1.model,

    comparator: function(model) {
      return model.get('attr');
    }
  });

  models.Base = Backbone.RelationalModel.extend({
    urlRoot: API.v1.model,

    relations: [
      {
        type: 'HasOne',
        key: 'attr',
        relatedModel: models.Other
      }
    ]
  });

  views.Base = Backbone.View.extend({
    close: function() {
      this.remove();
      this.unbind();
      if (this.onclose) {
        this.onclose();
      }
    }
  });

  APP.Router = Backbone.Router.extend({
    routes: {
      '': 'home',
      'account/login/*extra': 'account_login'
    },

    initialize: function(el) {
      this._first_popstate = true;
      this.$nav.find('li.active').removeClass('active');
      this.history = Backbone.history;
      this.manager = new utils.ViewManager(el);
      this.search = window.location.search;

      _.bindAll(this, 'check_search');
      $(window).on('popstate', this.check_search);
    },

    check_search: function() {
      var search = this.search;
      this.search = window.location.search;

      if (this._first_popstate === true) {
        this._first_popstate = false;
        return;
      }

      if (search !== window.location.search) {
        this.history.loadUrl() || this.history.loadUrl(this.history.getHash());
      }
    },

    nav_select: function(className) {
      this.$nav.find('li.active').removeClass('active');
      this.$nav.find('li .' + className).parent().addClass('active');
    },

    navigate: function(fragment, opts) {
      var root = this.history.root;
      if (root !== '/') {
        if (root === fragment.substr(0, root.length)) {
          fragment = fragment.substr(root.length);
        }
        else if (root.substr(0, 1) === '/'
                 && root.substr(1) === fragment.substr(0, root.length - 1)) {
          fragment = fragment.substr(root.length - 1);
        }
      }
      return Backbone.Router.prototype.navigate.call(this, fragment, opts);
    },

    navigate_query: function(fragment, opts) {,
      return this.navigate(this.history.getFragment() + query, opts);
    },

    navigate_trigger: function(fragment, opts) {
      opts || (opts = {});
      opts.trigger = true;
      return this.navigate(fragment, opts);
    },

    do_404: function() {
      this.manager.html(utils.get_template('404')());
    },

    account_login: function() {
      this.manager.$el.find('input:first').focus();
    },

    home: function() {
      this.manager.html(utils.get_template('home')());
    },

    base: function() {
      this.manager.show(new views.Base());
    }
  });
}(jQuery, this));
