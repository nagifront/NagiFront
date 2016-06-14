angular.module('nagifront')
  .directive('scheduledDowntime',['d3','$http','$interval','djangoUrl',function(d3, $http, $interval, djangoUrl) {
  return {
    restrict: 'EA',
    scope: true,
    template: '<h3>다운타임 스케쥴</h3><div class="charts" ng-if="!is_modify_setting">'
        +'<scrollable always-visible="true">'
          +'<table class="tables">'
            +'<tr>'
              +'<th>Host name</th>'
              +'<th>Entry Time</th>'
              +'<th>Comments</th>'
              +'<th>Start Time</th>'
              +'<th>End Time</th>'
            +'</tr>'
            +'<tr class="downtimes" ng-repeat="downtime in downtimes">'
              +'<td><span>{{downtime.host_name}}</span></td>'
              +'<td>{{downtime.entry_time | date:"yyyy/MM/dd HH:mm:ss"}}</td>'
              +'<td>{{downtime.comment_data}}</td>'
              +'<td>{{downtime.scheduled_start_time | date:"yyyy/MM/dd HH:mm:ss"}}</td>'
              +'<td>{{downtime.scheduled_end_time | date:"yyyy/MM/dd HH:mm:ss"}}</td>'
            +'</tr>'
          +'</table>'
        +'</scrollable>'
      +'</div>'
        + '<div class="widget-padding" ng-if="is_modify_setting"></div>',
      link: function(scope, element, attrs) {
        getData = function() {
          $http.get(djangoUrl.reverse('configuration-scheduled-downtime')).then(function(response) {
          scope.downtimes = response.data.scheduled_downtime;
        });
        }
        $interval(getData, 30000);
        getData();
      },
    };
  }]);
