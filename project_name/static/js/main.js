(function($, window, undefined) {
  'use strict';

  var g = APP.g = {};
  var collections = APP.collections = {};
  var models = APP.models = {};
  var utils = APP.utils = {};
  var views = APP.views = {};

  utils.ViewManager = function(el) {
    this.el = el;
    this.$el = $(el);
    this.current = null;
  };
  utils.ViewManager.prototype.show = function(view) {
    if (this.current && this.current.close) {
      this.current.close();
    }

    this.current = view;
    this.current.render();

    this.$el.html(this.current.el);
  };

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
      '': 'home'
    },

    initialize: function() {
      this.manager = new utils.ViewManager(document.getElementById('content'));
    },

    navigate_trigger: function() {
      var args = _.toArray(arguments);
      var opts = args[1];
      opts || (opts = {});
      opts.trigger = true;
      args[1] = opts;
      Backbone.Router.prototype.navigate.apply(this, args);
    },

    home: function() {
      this.manager.show(new views.Base());
    }
  });
}(jQuery, this));
