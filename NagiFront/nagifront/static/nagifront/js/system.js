app.controller('system', function($scope, $http, djangoUrl){
 $scope.categories = ['Configuration'];
 $scope.divisions = [''];
 $scope.sections = [''];
 $scope.update = function(value) {
   if(value === 'Configuration') {
     $scope.divisions = ['Hosts', 'Host group', 'Service'];
     $scope.category = value;
   }
   else if(value == 'Hosts') {
      $http.get(djangoUrl.reverse('hosts-ids')).then(function(response) {
        var data = response.data.ids;
        $scope.sections = [];
        angular.forEach(data, function(value, key) {
          $scope.sections.push(key);
        });
      });
      $scope.division = value;
   }
   else if(value == 'Host group') {
      $http.get(djangoUrl.reverse('hosts-groups')).then(function(response) {
        var data = response.data;
        $scope.sections = [];
        angular.forEach(data, function(value, key) {
          $scope.sections.push(value.alias);
        });
      });
      $scope.division = value;
   }
   else if(value != '') {
     $scope.final_value = value;
   }
 };
})
