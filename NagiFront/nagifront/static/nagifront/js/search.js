app.controller('search', function($scope, $http, $location, $window, djangoUrl){
  $scope.type = 'host';
  var parseUrl = function(url) {
    var value = '';
    for(var i = 0; i < url.length; i++) {
      if(url[i] === '=') {
        for(var j = i+1;  j < url.length; j++) {
            if(url[j] == '&') break;
            value = value + url[j];
        }
        break;
      }
    }
    return value;
  };
  $scope.init = function() {
      $http.get(djangoUrl.reverse('hosts-ids')).then(function success(response) {
        var ids = response.data.ids;
        var name='';
        $scope.id = parseUrl($location.absUrl()) * 1;
        for(var i = 0; i < ids.length; i++) {
          if(ids[i].host_object_id === $scope.id){
            $scope.name = ids[i].name;
            break;
           }
        }
      });
  };
  $scope.init();
  $scope.tosystem = function() {
        $http.get(djangoUrl.reverse('system')+'&id='+$scope.id)
        .then(function success(response) {
          $window.location.href = 'system?id='+$scope.id;
        });
  }
  $scope.move = function() {
    if($scope.type === "host") {
      $http.get(djangoUrl.reverse('hosts-ids')).then(function success(response) {
        var ids = response.data.ids;
        var id;
        for(var  i = 0; i < ids.length; i++) {
          if(ids[i].name.substr(0, $scope.name.length) === $scope.name) id = ids[i].host_object_id;
        }
        $http.get(djangoUrl.reverse('search')+'&id='+id+'&type='+$scope.type)
        .then(function success(response) {
          $window.location.href = 'search?id='+id+'&type='+$scope.type;
        });
    });
    }
    else if($scope.type === "hostGroup") {
      $http.get(djangoUrl.reverse('hosts-groups')).then(function success(response) {
        var data = response.data;
        var id = -1;
        angular.forEach(data, function(value, key) {
          if(value.alias === $scope.name) id = key;
        });
        if(id === -1) {
         angular.forEach(data, function(value, key) {
            if(value.alias.substr(0, $scope.name.length) === $scope.name) id = key;
          });
        }
        $http.get(djangoUrl.reverse('search')+'&id='+id+'&type='+$scope.type)
        .then(function success(response) {
          $window.location.href = 'search?id='+id+'&type='+$scope.type;
        });
    });
    }
  }
})
