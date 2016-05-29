angular.module('nagifront')
  .directive('troubleTrend',['d3', '$http', '$interval', 'djangoUrl', function(d3, $http, $interval, djangoUrl) {
    return {
      restrict: 'EA',
      scope: {
        data: '=',
      },
      template: '<h3>문제 발생 트렌드</h3><div class="charts"></div>',
      link: function(scope, element, attrs) {
        getData = function() {
          $http.get(djangoUrl.reverse('host-groups-trouble-trend') + '&host_group_id=' + attrs.hostGroupId + '&time-scale=' + attrs.timeScale).then(function(response) {
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
          if(data === undefined) return;

          d3.select(element[0])
            .select('.charts')
            .selectAll('*')
            .remove();

					var time_scale = data['time-scale'];
				
					function parseTime(time) {
						var strArray;
						if(time_scale==='week') {
							strArray=time.split('-');
							return strArray[1]+'-'+strArray[2];
						}
						else {
							strArray=time.split('-');
							return strArray[3];
						}
					}

          var data_processed = [];
          angular.forEach(data.time, function(value, key) {
            data_processed.push({time: parseTime(key), warning: value.warning, critical: value.critical});
          });

					data_processed.sort(function(a, b) { 
						return a.time < b.time? -1 : a.time > b.time? 1: 0;	
					});

          var color = d3.scale.ordinal()
            .range([
            '#F1F45A',
            '#EF6A6A'
          ]);

          var margin = {top: 20, right: 20, bottom: 20, left: 40},
            width = 500 - margin.left - margin.right,
            height = 300 - margin.top - margin.bottom;

          var x0 = d3.scale.ordinal()
            .rangeRoundBands([0, width], .1);
          var x1 = d3.scale.ordinal();

          var y = d3.scale.linear()
            .range([height, 0]);

          var xAxis = d3.svg.axis()
            .scale(x0)
            .orient('bottom');

          var yAxis = d3.svg.axis()
            .scale(y)
            .orient('left')
            .tickFormat(d3.format('.2s'));

          var svg = d3.select(element[0]).select('.charts').append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom)
            .append('g')
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');
          var stateName = ['warning', 'critical'];
          data_processed.forEach(function(d) {
            d.state = stateName.map(function(name) {return {name: name, value: +d[name]}; });
          });
          x0.domain(data_processed.map(function(d) {return d.time;}));  
          x1.domain(stateName).rangeRoundBands([0, x0.rangeBand()]);
          y.domain([0, d3.max(data_processed, function(d) {return d3.max(d.state, function(d) {return d.value; }); })+2]);

          svg.append('g')
            .attr('class', 'x axis')
            .attr('transform', 'translate(0,' + height + ')')
            .call(xAxis);

          svg.append('g')
            .attr('class', 'y axis')
            .call(yAxis)
            .append('text')
            .attr('transform', 'rotate(-90)')
            .attr('y', 2)
            .attr('dy', '.51em')
            .style('text-anchor', 'end')
            .text('state number');

          var group = svg.selectAll('.time')
            .data(data_processed)
            .enter().append('g')
            .attr('class','time')
            .attr('transform', function(d) {return 'translate(' + x0(d.time) + ',0)';});
          group.selectAll('rect')
            .data(function(d) {return d.state;})
            .enter().append('rect')
            .attr('width', x1.rangeBand())
            .attr('x', function(d) {return x1(d.name); })
            .attr('y', function(d) {return y(d.value);})
            .attr('height', function(d) {return height - y(d.value);})
            .style('fill', function(d) {return color(d.name)});

          var legend = svg.selectAll('.legend')
            .data(stateName.slice().reverse())
            .enter().append('g')
            .attr('class', 'legend')
            .attr('transform', function(d, i) {return 'translate(0,' + i * 20 + ')';});

          legend.append('rect')
            .attr('x', width-18)
            .attr('width', 18)
            .attr('height', 18)
            .style('fill', color);

          legend.append('text')
            .attr('x', width-24)
            .attr('y', 9)
            .attr('dy', '.35em')
            .style('text-anchor', 'end')
            .text(function(d) {return d;});
        };
      },
    };
    }]);
