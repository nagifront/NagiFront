app.controller('system', function($scope, $http, djangoUrl){
  $scope.categories = ['Configuration'];
  $scope.divisions = [''];
  $scope.type = 'none';
  $scope.sections = [''];
  $scope.ready = false;
  $scope.isHosts = function() {
    return $scope.type === 'Hosts';
  }
  $scope.isHostgroups = function() {
    return $scope.type === 'Host groups';
  }
  $scope.isServices = function() {
    return $scope.type === 'Services';
  }
  $scope.isContacts = function() {
    return $scope.type === 'Contacts';
  }
  $scope.isContactgroups = function() {
    return $scope.type === 'Contact groups';
  }
  $scope.isTimeperiods = function() {
    return $scope.type === 'Time periods';
  }
  $scope.isCommands = function() {
    return $scope.type === 'Commands';
  }
  $scope.show = function() {
   $scope.ready = true;
   $scope.type = $scope.division;
   $scope.option = $scope.section;
  }
  $scope.update = function(value) {
    if(value === 'Configuration') {
      $scope.divisions = ['Hosts', 'Host groups', 'Services', 'Contacts', 'Contact groups', 'Time periods', 'Commands'];
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
