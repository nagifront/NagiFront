var app = angular.module('nagifront', ['djng.urls']).config(function($httpProvider) {
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});
app.controller('search', function($scope, $http, $window, djangoUrl){
  $scope.search = function(){
    $http.post(djangoUrl.reverse('index'), {
        type: $scope.type,
        name: $scope.name,
    }).then(function success(response){
      var result = response.data.result;
      if (result){
        $window.location.href = '/';
      } else {
      }
    }, function failure(response){
    });
  };
  })
