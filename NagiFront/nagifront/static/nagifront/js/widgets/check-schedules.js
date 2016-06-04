angular.module('nagifront')
  .directive('checkSchedules',['d3','$http','$interval','djangoUrl',function(d3, $http, $interval, djangoUrl) {
  return {
    restrict: 'EA',
    scope: {
    },
    template: '<h3>체크 스케쥴</h3><div class="charts">'
        +'<div class="schedule" ng-repeat="schedule in schedules">'
          +'<span class="nextCheck">{{schedule.next_check_time | date: "yyyy/MM/dd HH:mm:ss"}}</span>'
          +'<span class="host"><span>[{{schedule.host_name}}]</span>: {{schedule.service_name}}</span>'
          +'<span class="lastCheck">last check: {{schedule.last_check_time | date: "yyyy/MM/dd HH:mm:ss" }}</span>'
	  +'<div class="output" ng-if="(schedule.host_name+schedule.service_name).length>30"><span>[{{schedule.host_name}}]: {{schedule.service_name}}</span></div>'
        +'</div>'
      +'</div>',
      link: function(scope, element, attrs) {
        getData = function() {
          if(attrs.hasOwnProperty('hostGroupId')) $http.get(djangoUrl.reverse('host-groups-check-schedules') + '&host_group_id=' + attrs.hostGroupId).then(function(response) {
          scope.schedules = response.data.check_schedules;
          });
          else $http.get(djangoUrl.reverse('host-groups-check-schedules')).then(function(response) {
          scope.schedules = response.data.check_schedules;
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

      },
    };
  }]);
