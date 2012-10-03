(function($, window, undefined) {
  var g = APP.g = {};
  var models = APP.models = {};
  var utils = APP.utils = {};
  var views = APP.views = {};

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
}(jQuery, this));
