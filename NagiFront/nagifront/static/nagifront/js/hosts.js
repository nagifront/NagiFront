app.controller('hosts', function($scope, $http, $window, djangoUrl){
  $scope.groups= [];
  $scope.ready = 0;
  $scope.selected = {name: undefined, id: -1};
  $http.get(djangoUrl.reverse('hosts-groups')).then(function(response) {
    var data = response.data;
      angular.forEach(data, function(value, key) {
        $scope.groups.push({name: value.alias, id: key});
    });
  });
  $scope.selectGroup = function(group) {
    $scope.selected = group;
    $scope.ready = 1;
  };
  $scope.move = function(id) {
    $http.get(djangoUrl.reverse('search')+'&id='+id+'&type=host')
    .then(function(response) {
      $window.location.href = 'search?id='+id+'&type=host';
    });
  };
})
