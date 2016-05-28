angular.module('nagifront')
  .directive('serviceNumberByStateChart',['d3','$http','$interval','djangoUrl',function(d3, $http, $interval, djangoUrl) {
  return {
    restrict: 'EA',
    scope: {
      data: '=',
    },
    template: '<h3>그룹별 서비스 현황</h3><div class="charts">'
        +'<div class="groups" ng-repeat="group in groups">'
          +'<span class="group-name">{{group.alias}}</span>'
          +'<span class="state Ok"><span>{{ group.Ok }}</span>   Ok</span>'
          +'<span class="state Warning"><span>{{ group.Warning }}</span>   Warning</span>'
          +'<span class="state Critical"><span>{{ group.Critical }}</span>   Critical</span>'
        +'</div>'
      +'</div>',
      link: function(scope, element, attrs) {
        getData = function() {
          $http.get(djangoUrl.reverse('host-groups-service-number-by-state')).then(function(response) {
            scope.data = response.data;
            scope.groups = [];
            var i = 0;

            angular.forEach(scope.data, function(value, key) {
              if(i%2===0) scope.groups.push({state: 'even', alias: value.alias, Ok: value.ok, Warning: value.warning, Critical: value.critical});
              else scope.groups.push({state: 'odd', alias: value.alias, Ok: value.ok, Warning: value.warning, Critical: value.critical});
              i++;
            });
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
