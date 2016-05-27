angular.module('nagifront')
	.directive('hostStatus',['d3', '$http', '$interval', 'djangoUrl', function(d3, $http, $inteval, djangoUrl){
		return {
			restrict: 'EA',
			scope: {
				group: '=',
				groupNum: '=',
				data: '=',
			},
			template: '<h3>그룹별 서비스 현황</h3><div class="charts"></div>',
			link: function(scope, element, attrs) {
				getData = function() {
					$http.get(djangoUrl.reverse('host-groups')).then(function(response) {
						groupNum = responce.data.length;	

					});
					$http.get(djangoUrl.reverse('host-groups-serveice-number-by-state')).then(function(response) {
						scope.data = responce.data;
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
					scope.render(scope.data);
				});
				scope.$watch('data', function(newVal, oldVal) {
					scope.render(newVal);
				}, true);

				scope.render = function(data) {
					if(data === undefined) return;

					d3.select(element[0])
						.select('.charts')
						.selectAll('*')
						.remove();
				}
			}
		}
	})
