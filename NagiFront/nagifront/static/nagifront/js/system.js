app.controller('system', function($scope, $http, djangoUrl){
 $scope.categories = ['Configuration'];
 $scope.divisions = [''];
 $scope.sections = [''];
 $scope.update = function() {
  if($scope.category === 'configuration') {
    $scope.divisions = ['Hosts', 'Host group', 'Service'];
  }
  if($scope.division === 'Hosts') {
  }
 }
})
