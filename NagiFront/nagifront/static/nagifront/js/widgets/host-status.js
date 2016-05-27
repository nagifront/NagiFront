angular.module('nagifront')
	.directive('hostStatus',['d3', '$http', '$interval', 'djangoUrl', function(d3, $http, $interval, djangoUrl) {
		return {
			restrict: 'EA',
			scope: {
				data: '=',
			},
			template: '<h3>호스트 현황</h3><div class="charts"></div>',
			link: function(scope, element, attrs) {
				getData = function() {
					$http.get(djangoUrl.reverse('hosts-groups-hosts-state')+'&host_group_id=189').then(function(response) {
						scope.data = response.data;
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
					if( data === undefined) return;

					d3.select(element[0])
						.select('.charts')
						.selectAll('*')
						.remove();
					
					var up = data['189'].up;
					var down = data['189'].down;
					var unreachable = data['189'].unreachable;
					
					var overall_data = [
						{label: 'up', data: up},
						{label: 'down', data: down},
					  {label: 'unreachable', data: unreachable},
					];

					var width = 200, height = 200, radius = 100
					var color = {
						up: '#8DD775',
						down: '#EF6A6A',
						unreachable: '#F89C59',
					};

					var arc = d3.svg.arc()
						.outerRadius(radius-10)
						.innerRadius(0)
					var pie = d3.layout.pie()
						.value(function(d) { return d.data})
						.sort(null)

					function draw_chart(data) {

					  var total = data[0].data + data[1].data + data[2].data;
						var svg = d3.select(element[0]).select('.charts').append('svg')
							.attr('width', 400)
							.attr('height', height)
							.append('g')
							.attr('transform', 'translate('+(width/2)+','+(height/2)+')');
	
						var defs = svg.append('defs');
						var filter = defs.append('filter')
							.attr('id','drop-shadow')
						filter.append('feGaussianBlur')
							.attr('in','SourceAlpha')
							.attr('stdDeviation', 2)
							.attr('result', 'blur');
						filter.append('feOffset')
							.attr('in','blur')
							.attr('dx', 2)
							.attr('dy', 2)
							.attr('result', 'offsetBlur');
						filter.append('feFlood')
							.attr('in','offsetBlur')
							.attr('flood-color','#2d2d2d')
							.attr('flood-opacity','0.5')
							.attr('result', 'offsetColor');
						filter.append('feComposite')
							.attr('in', 'offsetColor')
							.attr('in2','offsetBlur')
							.attr('operator', 'in')
							.attr('result', 'offsetBlur');
						var feMerge = filter.append('feMerge');
						feMerge.append('feMergeNode')
							.attr('in','offsetBlur')
						feMerge.append('feMergeNode')
							.attr('in', 'SourceGraphic');

						var path = svg.selectAll('path')
							.data(pie(data))
							.enter()
							.append('path')
							.attr('d', arc)
							.style('filter','url(#drop-shadow)')
							.attr('fill', function(d, i) {
								return color[d.data.label];
							});

						svg.append('text')
						.text('Up:    '+ data[0].data*100/total+' %    ('+data[0].data+')')
						.attr('dy','-70px')
						.attr('dx','230px')
						.style('text-anchor','end')
						.style('font-size', '0.8em')
						svg.append('text')
						.text('Down:    '+ data[1].data*100/total+' %    ('+data[1].data+')')
						.attr('dy','-45px')
				  	.attr('dx','230px')
						.style('text-anchor','end')
						.style('font-size', '0.8em')
						svg.append('text')
						.text('Unreachable:    '+ data[2].data*100/total+' %    ('+data[2].data+')')
						.attr('dy','-20px')
						.attr('dx','230px')
						.style('text-anchor','end')
						.style('font-size', '0.8em')
					};
					draw_chart(overall_data);
				};
			},
		};
	}]);
