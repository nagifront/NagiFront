app.controller('dashboard', function($scope, $http, djangoUrl){
  $http.get(djangoUrl.reverse('hosts-ids')).then(function(response) {
    scope.host_ids = response.data.ids;
  });
  $http.get(djangoUrl.reverse('hosts-groups-ids')).then(function(response) {
    scope.hostgroup_ids = response.data.ids;
  });
})
