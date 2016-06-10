angular.module('nagifront')
  .directive('aHostStatusDetail',['d3','$http','$interval','djangoUrl',function(d3, $http, $interval, djangoUrl) {
  return {
    restrict: 'EA',
    scope: {
    },
    template: 
          '<td class="state {{state[host.current_state]}}"><span>{{host.alias}}</span></td>'
          +'<td class="last_check" >{{host.last_check | date:"yyyy/MM/dd HH:mm:ss"}}</td>'
          +'<td class="duration">{{host.duration}}</td>'
          +'<td class="info">{{host.output}}</td>',
      link: function(scope, element, attrs) {
        scope.state = {0: 'up', 2: 'unreachable', 1: 'down'};
        var time = [1000 * 60 * 60 * 24, 1000 * 60 * 60, 1000 * 60, 1000];
        getData = function() {
          $http.get(djangoUrl.reverse('hosts-status')+'&host_id='+attrs.hostId).then(function(response) {
          scope.host = response.data.hosts[0];
          var milisec = new Date(scope.host.last_check) - new Date(scope.host.last_state_change);
          var day = parseInt(milisec / time[0]);
          var hour = parseInt((milisec - day * time[0]) / time[1]);
          var min = parseInt((milisec - day * time[0] - hour * time[1]) / time[2]);
          var sec = parseInt((milisec - day * time[0] - hour * time[1] - min * time[2]) / time[3]);
          scope.host.duration = day + 'd ' + hour + 'h ' + min + 'm ' + sec + 's '; 
        });
        }
        $interval(getData, 30000);
        getData();

        window.onresize = function() {
          scope.$apply();
        };
        scope.$watch(function() {
          return angular.element(window)[0].innerWidth;
        }, function() {
          scope.$apply();
        });
      }
    };
  }]);
angular.module('nagifront')
  .directive('hostStatusDetail',['d3','$http','$interval','djangoUrl',function(d3, $http, $interval, djangoUrl) {
    return {
     restrict: 'EA',
     scope: {
      data: '=',
     },
     template: '<h3>호스트 현황</h3><table class="charts">'
                +'<tr>'
                   +'<th>Host</th>'
                    +'<th>Last Check</th>'
                    +'<th>Duration</th>'
                   +'<th>Status Information</th>'
                 +'</tr>'
                +'<tr class="hosts" ng-repeat="host in hosts" a-host-status-detail host_id="{{ host }}">'
                +'</tr>'
                +'</table>', 
     link: function(scope, element, attrs) {
      $http.get(djangoUrl.reverse('hosts-groups')).then(function(response) {
        scope.hosts = response.data[attrs.hostGroupId].members;
      });
     },
     };
  }]);

