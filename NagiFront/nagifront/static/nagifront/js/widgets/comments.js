angular.module('nagifront')
  .directive('comments',['d3','$http','$interval','djangoUrl',function(d3, $http, $interval, djangoUrl) {
  return {
    restrict: 'EA',
    scope: {
    },
    template: '<h3>코멘트 현황</h3><div class="charts">'
        +'<div class="comments" ng-repeat="comment in comments">'
          +'<span class="host">[{{comment.host_name}}]</span>'
          +'<span class="contents">{{comment.contents}}</span>'
          +'<span class="detail">{{comment.time | date: "yyyy/MM/dd HH:mm:ss"}} by <span>{{comment.author}}</span></span>'
        +'</div>'
      +'</div>',
      link: function(scope, element, attrs) {
        getData = function() {
        //  $http.get(djangoUrl.reverse('host-groups-service-number-by-state')).then(function(response) {
        //    scope.data = response.data;
       // });
			 		scope.comments = [{"host_name": "Waffle Choco", "contents":"Notifications for this host are being suppressed because it was detected as having been flapping between different states", "time":"2016-05-03T22:57:39Z", "author":"Seyoung"},
			 											{"host_name": "Uriel", "contents":"Notifications for this host are being suppressed because it was detected as having been flapping between different states. When the host state stabilizes and the flapping stops, notifications will be re-enabled", "time":"2016-05-03T22:57:39Z", "author":"Seyoung"}];
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
