app.controller('system', function($scope, $window, $location, $http, djangoUrl){
  $scope.categories = ['Configuration'];
  $scope.divisions = [''];
  $scope.type = 'none';
  $scope.sections = [''];
  $scope.ready = false;
  $scope.simple = {};
  $scope.isHosts = function() {
    return $scope.type === 'Hosts';
  }
  $scope.isHostgroups = function() {
    return $scope.type === 'Host groups';
  }
  $scope.isServices = function() {
    return $scope.type === 'Services';
  }
  $scope.show = function() {
   $scope.ready = true;
   $scope.type = $scope.division;
   $scope.option = $scope.section;
  }
  var parseUrl = function(url) {
    var value = '';
    for(var i = 0; i < url.length; i++) {
      if(url[i] === '=') {
        for(var j = i+1;  j < url.length; j++) {
            value = value + url[j];
        }
      }
    }
    return value;
  }
  $scope.init = function() {
    $http.get(djangoUrl.reverse('hosts-ids')).then(function success(response) {
      var ids = response.data.ids;
      var name = ''; 
      var id = parseUrl($location.absUrl()) * 1;
      for(var i=0; i < ids.length; i++) {
        if(ids[i].host_object_id === id) {
          $scope.dategory = 'Configuration';
          $scope.division = 'Hosts';
          $scope.section = ids[i].name;
          $scope.show();
          break;
        }
      }
    });
  }
  $scope.init();
  $scope.isSimple = function(name) {
    if($scope.simple[name] === undefined) $scope.simple[name]=true;
    return $scope.simple[name];
  }
  $scope.toggleSimple = function(name) {
    $scope.simple[name] = !$scope.simple[name];
    console.log($scope.simple[name]);
  }
  $scope.toEdit = function(id) {
    $window.location.href = djangoUrl.reverse('edit-config', {object_id: id})
  }
  $scope.update = function(value) {
    if(value === 'Configuration') {
      $scope.divisions = ['Hosts', 'Host groups', 'Services'];
      $scope.category = value;
    }
    else if(value === 'Hosts') {
      $http.get(djangoUrl.reverse('hosts-ids')).then(function(response) {
        var data = response.data.ids;
        $scope.sections = ['All'];
        angular.forEach(data, function(value, key) {
          $scope.sections.push(value.name);
        });
      });
      $scope.division = value;
    }
    else if(value === 'Host groups') {
      $http.get(djangoUrl.reverse('hosts-groups')).then(function(response) {
        var data = response.data;
        $scope.sections = [];
        angular.forEach(data, function(value, key) {
          $scope.sections.push(value.alias);
        });
      });
      $scope.division = value;
    }
    else if(value === 'Services') {
      $http.get(djangoUrl.reverse('hosts-ids')).then(function(response) {
        var data = response.data.ids;
        $scope.sections = ['All'];
        angular.forEach(data, function(value, key) {
          $scope.sections.push(value.name);
        });
      });
      $scope.division = value;
    }
    else if(value === 'Contacts') {
       $scope.sections = ['All'];
    }
    else if(value === 'Contact groups') {
       $scope.sections = ['All'];
    }
    else if(value === 'Time periods') {
       $scope.sections = ['All'];
    }
    else if(value === 'Commands') {
       $scope.sections = ['All'];
    }
    else if(value !== '') {
      $scope.section = value;
    }
  };
})
