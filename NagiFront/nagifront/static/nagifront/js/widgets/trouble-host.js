angular.module('nagifront')
  .directive('troubleHost', ['d3', '$http', '$interval', 'djangoUrl', function(d3, $http, $interval, djangoUrl){
    return {
      restrict: 'EA',
      scope: true,
      template: '<h3>문제 발생 호스트</h3><div class="charts" ng-if="!is_modify_setting">'
          +'<scrollable always-visible="true">'
            + '<div class="trouble-item" ng-repeat="trouble in troubles | orderBy : \'-time\'">'
              + '<span class="state {{ state[trouble.state] }}"></span>'
              + '<span class="trouble-name"><span>[{{ trouble.host_name }}] {{ trouble.service_name }}</span></span>'
              + '<time>{{ trouble.time | date : "yyyy/MM/dd HH:mm:ss" }}</time>'
              + '<div class="output" ng-if="trouble.output!=\'\'"><span>{{ trouble.output }}</span></div>'
            + '</div>'
          + '</scrollable>'
        + '</div>'
        + '<div class="widget-padding" ng-if="is_modify_setting"><p>문제 발생 호스트</p></div>',
      link: function(scope, element, attrs){
        getData = function(){
          $http.get(djangoUrl.reverse('host-groups-trouble-hosts')).then(function(response){
            scope.troubles = response.data.trouble_hosts;
          });
        }
        $interval(getData, 30000);
        getData();
        // get data
        
        scope.state = {0: 'ok', 1: 'warning', 2: 'critical', 3: 'unknown'}
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

