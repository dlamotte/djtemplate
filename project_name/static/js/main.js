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
      this.$nav.find('li.active').removeClass('active');
      this.manager = new utils.ViewManager(el);
    },

    nav_select: function(className) {
      this.$nav.find('li.active').removeClass('active');
      this.$nav.find('li .' + className).parent().addClass('active');
    },

    navigate_trigger: function() {
      var args = _.toArray(arguments);
      var opts = args[1];
      opts || (opts = {});
      opts.trigger = true;
      args[1] = opts;
      Backbone.Router.prototype.navigate.apply(this, args);
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
