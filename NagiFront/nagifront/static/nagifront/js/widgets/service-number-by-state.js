angular.module('nagifront')
  .directive('serviceNumberByState',['d3', '$http', '$interval', 'djangoUrl', function(d3, $http, $interval, djangoUrl) {
    return {
      restrict: 'EA',
      scope: true,
      template: '<h3>그룹별 서비스 현황</h3><div class="charts" ng-if="!is_modify_setting"><scrollable always-visible="true"></scrollable></div>'
        + '<div class="widget-padding" ng-if="is_modify_setting"></div>',
      link: function(scope, element, attrs) {
        getData = function() {
          $http.get(djangoUrl.reverse('host-groups-service-number-by-state')).then(function(response) {
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

          var data_processed = [];
          angular.forEach(data, function(value, key) {
            data_processed.push({group: value.alias, Ok: value.ok, Warning: value.warning, Critical: value.critical});
          });

          var color = d3.scale.ordinal()
            .range([
            '#8DD775',
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
          var stateName = ['Ok', 'Warning', 'Critical'];
          data_processed.forEach(function(d) {
            d.state = stateName.map(function(name) {return {name: name, value: +d[name]}; });
          });
          x0.domain(data_processed.map(function(d) {return d.group;}));  
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

          var group = svg.selectAll('.group')
            .data(data_processed)
            .enter().append('g')
            .attr('class','group')
            .attr('transform', function(d) {return 'translate(' + x0(d.group) + ',0)';});
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
