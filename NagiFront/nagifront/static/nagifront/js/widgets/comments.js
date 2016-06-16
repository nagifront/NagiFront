angular.module('nagifront')
  .directive('comments',['d3','$http','$interval','djangoUrl',function(d3, $http, $interval, djangoUrl) {
  return {
    restrict: 'EA',
    scope: true,
    template: '<h3>코멘트 현황</h3><div class="charts" ng-if="!is_modify_setting">'
        +'<scrollable always-visible="true">'
          +'<div class="comments" ng-repeat="comment in comments">'
            +'<span class="host">[{{comment.host_name}}]</span>'
            +'<span class="contents">{{comment.contents}}</span>'
            +'<span class="detail">{{comment.time | date: "yyyy/MM/dd HH:mm:ss"}} by <span>{{comment.author}}</span></span>'
            +'<div class="output" ng-if="comment.contents.length > 256"><span>{{comment.contents}}</span></div>'
          +'</div>'
        +'</scrollable>'
      +'</div>',
      link: function(scope, element, attrs) {
        getData = function() {
          if(attrs.hasOwnProperty('hostId')) {
            $http.get(djangoUrl.reverse('hosts-comments')+'&host_id='+attrs.hostId).then(function(response) {
              scope.comments = response.data.comments;
              });
          }
          else {
            $http.get(djangoUrl.reverse('configuration-comments')).then(function(response) {
             scope.comments = response.data.comments;
          });
          }
        }
        $interval(getData, 30000);
        getData();
      },
    };
  }]);
