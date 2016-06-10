angular.module('nagifront')
  .directive('comments',['d3','$http','$interval','djangoUrl',function(d3, $http, $interval, djangoUrl) {
  return {
    restrict: 'EA',
    scope: {
    },
    template: '<h3>코멘트 현황</h3><div class="charts">'
        +'<scrollable always-visible="true">'
          +'<div class="comments" ng-repeat="comment in comments">'
            +'<span class="host">[{{comment.host_name}}]</span>'
            +'<span class="contents">{{comment.contents}}</span>'
            +'<span class="detail">{{comment.time | date: "yyyy/MM/dd HH:mm:ss"}} by <span>{{comment.author}}</span></span>'
            +'<div class="output" ng-if="comment.contents.length > 143"><span>{{comment.contents}}</span></div>'
          +'</div>'
        +'</scrollable>'
      +'</div>',
      link: function(scope, element, attrs) {
        getData = function() {
          $http.get(djangoUrl.reverse('configuration-comments')).then(function(response) {
            scope.comments = response.data.comments;
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
