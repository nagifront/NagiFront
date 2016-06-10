(function(){Math.clamp=function(a,b,c){return Math.max(b,Math.min(c,a));}})();
var app = angular.module('nagifront', ['sun.scrollable','djng.urls', 'd3']).config(function($httpProvider) {
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});
