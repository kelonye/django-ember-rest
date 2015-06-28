/**
  * Module dependencies
  */
require('ember-data');

// find query

module.exports = DS.RESTAdapter.extend({

  buildURL: function() {
    // add the trailing slash if necessary to avoid redirects
    var url = this._super.apply(this, arguments);
    if (url.charAt(url.length-1) !== '/') url += '/';
    return url;
  },

  findQuery: function(store, type, query) {
    var data = { query: query };
    return this.ajax(this.buildURL(type.typeKey), 'POST', { data: data });
  },

  pathForType: function(modelName) {
    var decamelized = Ember.String.decamelize(modelName);
    return Ember.String.pluralize(decamelized);
  },

});
