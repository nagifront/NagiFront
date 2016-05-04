var app = angular.module('nagifront', ['djng.urls']).config(function($httpProvider) {
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});
app.controller('login', function($scope, $http, $window, djangoUrl){
  $scope.login = function(){
    $http.post(djangoUrl.reverse('login'), {
        id: $scope.id,
        password: $scope.password,
    }).then(function success(response){
      var result = response.data.result;
      var message = response.data.message;
      if (result){
        $window.location.href = '/';
      } else {
        $scope.show_modal = true;
        $scope.message = response.data.message;
      }
    }, function failure(response){
      $scope.show_modal = true;
      $scope.message = '예기치 못한 에러가 발생했습니다';
    });
  }

  $scope.close_modal = function(){
    $scope.show_modal = false;
  }
})
