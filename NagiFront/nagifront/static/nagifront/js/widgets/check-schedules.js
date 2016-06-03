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
        +'</div>'
      +'</div>',
      link: function(scope, element, attrs) {
        getData = function() {
          //$http.get(djangoUrl.reverse('host-groups-check-schedules') + '&host_group_id=' + attrs.hostGroupId).then(function(response) {
          //  scope.schedules = response.data[check_schedules];
        //  });
          scope.schedules =   [{"host_name": "WaffleStudio Choco", "service_name": "Current Users", "next_check_time": "2016-06-03T13:40:03Z", "last_check_time": "2016-06-03T13:38:03Z"}, {"host_name": "WaffleStudio Choco", "service_name": "Mem Load", "next_check_time": "2016-06-03T13:40:03Z", "last_check_time": "2016-06-03T13:38:03Z"}, {"host_name": "WaffleStudio Choco", "service_name": "Total Process", "next_check_time": "2016-06-03T13:40:03Z", "last_check_time": "2016-06-03T13:38:03Z"}, {"host_name": "WaffleStudio Dev.", "service_name": "Current Users", "next_check_time": "2016-06-03T13:40:03Z", "last_check_time": "2016-06-03T13:38:03Z"}, {"host_name": "WaffleStudio Dev.", "service_name": "CPU Load", "next_check_time": "2016-06-03T13:40:03Z", "last_check_time": "2016-06-03T13:38:03Z"}, {"host_name": "WaffleStudio Dev.", "service_name": "Mem Load", "next_check_time": "2016-06-03T13:40:03Z", "last_check_time": "2016-06-03T13:38:03Z"}, {"host_name": "WaffleStudio Choco", "service_name": "CPU Load", "next_check_time": "2016-06-03T13:40:03Z", "last_check_time": "2016-06-03T13:38:03Z"}, {"host_name": "WaffleStudio Dev.", "service_name": "Total Process", "next_check_time": "2016-06-03T13:40:03Z", "last_check_time": "2016-06-03T13:38:03Z"}, {"host_name": "WaffleStudio Linode", "service_name": "IO rate", "next_check_time": "2016-06-03T13:40:05Z", "last_check_time": "2016-06-03T13:35:05Z"}, {"host_name": "WaffleStudio Linode", "service_name": "Disk Space", "next_check_time": "2016-06-03T13:41:01Z", "last_check_time": "2016-06-03T13:36:01Z"}, {"host_name": "WaffleStudio Linode", "service_name": "Current Users", "next_check_time": "2016-06-03T13:41:05Z", "last_check_time": "2016-06-03T13:36:05Z"}, {"host_name": "uriel", "service_name": "Disk Space", "next_check_time": "2016-06-03T13:41:05Z", "last_check_time": "2016-06-03T13:36:05Z"}, {"host_name": "uriel", "service_name": "CPU Load", "next_check_time": "2016-06-03T13:41:05Z", "last_check_time": "2016-06-03T13:36:05Z"}, {"host_name": "WaffleStudio Linode", "service_name": "Total Processes", "next_check_time": "2016-06-03T13:41:22Z", "last_check_time": "2016-06-03T13:36:22Z"}, {"host_name": "localhost", "service_name": "Disk Space", "next_check_time": "2016-06-03T13:41:57Z", "last_check_time": "2016-06-03T13:36:57Z"}, {"host_name": "localhost", "service_name": "Total Processes", "next_check_time": "2016-06-03T13:41:57Z", "last_check_time": "2016-06-03T13:36:57Z"}, {"host_name": "localhost", "service_name": "SSH", "next_check_time": "2016-06-03T13:41:57Z", "last_check_time": "2016-06-03T13:36:57Z"}, {"host_name": "localhost", "service_name": "Current Load", "next_check_time": "2016-06-03T13:41:57Z", "last_check_time": "2016-06-03T13:36:57Z"}];
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
