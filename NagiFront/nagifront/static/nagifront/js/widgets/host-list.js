angular.module('nagifront')
  .directive('hostList',['d3','$http','$interval','djangoUrl',function(d3, $http, $interval, djangoUrl) {
  return {
    restrict: 'EA',
    scope: {
      data: '=',
    },
    template: '<h3>호스트 목록</h3><div class="charts">'
        +'<div class="hosts" ng-repeat="host in hosts">'
          +'<span class="host-name">{{host.alias}}</span>'
          +'<span class="state Ok"><span>{{host.Ok}}</span> Ok</span>'
          +'<span class="state Warning"><span>{{host.Warning}}</span> Warning</span>'
          +'<span class="state Critical"><span>{{host.Critical}}</span> Critical</span>'
        +'</div>'
      +'</div>',
      link: function(scope, element, attrs) {
        getData = function() {
          $http.get(djangoUrl.reverse('hosts-groups')).then(function(response) {
            scope.data = response.data[attrs.hostGroupId].members;
            scope.hosts = [];
						for(var i = 0; i < scope.data.length; i++) {
          		$http.get(djangoUrl.reverse('hosts-status')+'&host_id='+scope.data[i]).then(function(response) {
								var host_alias = response.data.hosts.alias;
          			$http.get(djangoUrl.reverse('hosts-services')+'&host_id='+scope.data[i]).then(function(response) {
									var host_value = response.data.state_number;
             			 scope.hosts.push({alias: host_alias, Ok: host_value.Ok, Warning: host_value.Warning, Critical: host_value.Critical});
								});
							});
						}
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
