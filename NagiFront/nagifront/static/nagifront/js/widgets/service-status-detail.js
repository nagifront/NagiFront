angular.module('nagifront')
  .directive('serviceStatusDetail',['d3','$http','$interval','djangoUrl',function(d3, $http, $interval, djangoUrl) {
  return {
    restrict: 'EA',
    scope: {
    },
    template: '<h3>서비스 현황</h3><table class="charts">'
            +'<tr>'
              +'<th>Service</th>'
              +'<th>Last Check</th>'
              +'<th>Duration</th>'
              +'<th>Attempt</th>'
              +'<th>Status Information</th>'
            +'</tr>'
        +'<tr class="services" ng-repeat="service in services">'
          +'<td class="state {{state[service.current_state]}}"><span>{{service.display_name}}</span></td>'
          +'<td class="last_check" >{{service.last_check | date:"yyyy/MM/dd HH:mm:ss"}}</td>'
          +'<td class="duration">{{service.duration}}</td>'
          +'<td class="attempt">{{service.current_check_attempt}} / {{service.max_check_attempts}}</td>'
          +'<td class="info">{{service.output}}</td>'
        +'</tr>'
      +'</table>',
      link: function(scope, element, attrs) {
        scope.state = {0: 'ok', 1: 'warning', 2: 'critical'};
        var time = [1000 * 60 * 60 * 24, 1000 * 60 * 60, 1000 * 60, 1000];
        getData = function() {
          $http.get(djangoUrl.reverse('hosts-services')+'&host_id='+attrs.hostId).then(function(response) {
          scope.services = response.data.services;
          for(var i =0; i < scope.services.length; i++) {
          var milisec = new Date(scope.services[i].last_check) - new Date(scope.services[i].last_state_change);
          var day = parseInt(milisec / time[0]);
          var hour = parseInt((milisec - day * time[0]) / time[1]);
          var min = parseInt((milisec - day * time[0] - hour * time[1]) / time[2]);
          var sec = parseInt((milisec - day * time[0] - hour * time[1] - min * time[2]) / time[3]);
          scope.services[i].duration = day + 'd ' + hour + 'h ' + min + 'm ' + sec + 's '; }
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
