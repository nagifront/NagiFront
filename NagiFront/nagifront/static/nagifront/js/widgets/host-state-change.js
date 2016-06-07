angular.module('nagifront')
  .directive('hostStateChange', ['d3', '$http', '$interval', 'djangoUrl', function(d3, $http, $interval, djangoUrl){
    return {
      restrict: 'EA',
      scope: {
      },
      template: '<h3>호스트 상태 변화</h3><div class="charts">'
          +'<scrollable always-visible="true">'
            + '<div class="state-change-item" ng-repeat="host in hosts | orderBy : \'-last_state_change\'">'
              + '<span class="state {{ state[host.state] }}">{{ state[host.state] }}</span>'
              + '<span class="host-name"><span>{{ host.alias }}</span></span>'
              + '<time>{{ host.last_state_change | date : "yyyy/MM/dd HH:mm:ss" }}</time>'
              + '<div class="output" ng-if="host.output!=\'\'"><span>{{ host.output }}</span></div>'
            + '</div>'
          + ' </scrollable>'
        + '</div>',
      link: function(scope, element, attrs){
        getData = function(){
          $http.get(djangoUrl.reverse('hosts-state-change')).then(function(response){
            scope.hosts = response.data.hosts;
          });
        }
        $interval(getData, 30000);
        getData();
        // get data
        
        scope.state = {0: 'up', 1: 'down', 2: 'unreachable', 3: 'indeterminate'}
        // init data

        window.onresize = function(){
          scope.$apply();
        };
        scope.$watch(function(){
          return angular.element(window)[0].innerWidth;
        }, function(){
          scope.$apply();
        });
        // re render
      },
    };
  }]);

