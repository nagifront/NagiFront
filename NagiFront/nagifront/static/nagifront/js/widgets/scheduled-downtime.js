angular.module('nagifront')
  .directive('scheduledDowntime',['d3','$http','$interval','djangoUrl',function(d3, $http, $interval, djangoUrl) {
  return {
    restrict: 'EA',
    scope: {
    },
    template: '<h3>다운타임 스케쥴</h3><table class="charts">'
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
      +'</table>',
      link: function(scope, element, attrs) {
        getData = function() {
          $http.get(djangoUrl.reverse('configuration-scheduled-downtime')).then(function(response) {
          scope.downtimes = response.data.scheduled_downtime;
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
