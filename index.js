module.exports = DS.RESTAdapter.extend({
  buildURL: function(record, suffix) {
    // add the trailing slash if necessary to avoid redirects
    var url = this._super(record, suffix);
    if (url.charAt(url.length-1) !== '/') url += '/'
    return url;
  }
});