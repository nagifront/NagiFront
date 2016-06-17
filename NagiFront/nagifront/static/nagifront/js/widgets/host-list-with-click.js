angular.module('nagifront')
  .directive('hostServiceStateWithClick', ['d3', '$http', '$interval', 'djangoUrl', function(d3, $http, $interval, djangoUrl) {
    return {
      restrict: 'EA',
      scope: true,
      template: '<button class="host-name" ng-click="move(id)"><span>▶ {{alias}}</span></button>'
        +'<span class="state Ok"><span>{{Ok}}</span> Ok</span>'
        +'<span class="state Warning"><span>{{Warning}}</span> Warning</span>'
        +'<span class="state Critical"><span>{{Critical}}</span> Critical</span>',
      link: function(scope, element, attrs) {
        getData = function() {
          $http.get(djangoUrl.reverse('hosts-services')+'&host_id='+attrs.hostId).then(function(response_services) {
            host_value = response_services.data.state_number;
            scope.id = attrs.hostId;
            scope.Ok = host_value.Ok;
            scope.Warning = host_value.Warning;
            scope.Critical = host_value.Critical;
          });
        }

        $http.get(djangoUrl.reverse('hosts-status')+'&host_id='+attrs.hostId).then(function(response_status) {
          scope.alias = response_status.data.hosts[0].alias;
         }).then(getData());
        $interval(getData, 100000);
        getData();
      },
    };
  }]);

angular.module('nagifront')
  .directive('hostListWithClick',['d3','$http','$interval','djangoUrl',function(d3, $http, $interval, djangoUrl) {
    return {
      restrict: 'EA',
      scope: true,
      template: '<h3>{{ alias }}</h3><div class="charts">'
        +'<scrollable always-visible="true">'
          +'<div class="hosts" ng-repeat="host in hosts" host-service-state-with-click host_id="{{ host }}">'
          +'</div>'
        +'</scrollable>'
        +'</div>',
      link: function(scope, element, attrs) {
        scope.lastChange = -1;
        getData = function(){
          if(scope.lastChange != attrs.hostGroupId)
          {
            scope.lastChange = attrs.hostGroupId;
            $http.get(djangoUrl.reverse('hosts-groups')).then(function(response) {
              scope.hosts = response.data[attrs.hostGroupId].members;
              scope.alias = response.data[attrs.hostGroupId].alias;
            });
          }
        }
        $interval(getData, 1000);
        getData();
      },
    };
  }]);
