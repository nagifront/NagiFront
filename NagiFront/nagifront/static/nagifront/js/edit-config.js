app.controller('edit-config', function($scope, $http, $window, djangoUrl){
  $scope.is_active_advanced = false;
  $scope.active_advanced = function(){
    $scope.is_active_advanced = true;
  }
  $scope.diactive_advanced = function(){
    $scope.is_active_advanced = false;
  }
  $scope.show_modal = true;
  $scope.close_modal = function(){
    $scope.show_modal = false;
  }
})
