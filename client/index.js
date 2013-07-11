require('ember-data');
module.exports = DS.RESTAdapter.extend({
  buildURL: function(record, suffix) {
    // add the trailing slash if necessary to avoid redirects
    var url = this._super(record, suffix);
    if (url.charAt(url.length-1) !== '/') url += '/'
    return url;
  },
  findQuery: function(store, type, query, recordArray) {
    var root = this.rootForType(type);
    var adapter = this;
    var data = { query: query };
    console.log(this.ajax)
    return this.ajax(this.buildURL(root), 'POST', {
      data: data
    }).then(function(json){
      adapter.didFindQuery(store, type, json, recordArray);
    }).then(null, DS.rejectionHandler);
  }
});
