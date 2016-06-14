angular.module('nagifront')
  .directive('overallHost', ['d3', '$http', '$interval', 'djangoUrl', function(d3, $http, $interval, djangoUrl){
    return {
      restrict: 'EA',
      scope: true,
      template: '<h3>호스트 상태</h3><div class="charts" ng-if="!is_modify_setting"></div>'
        + '<div class="widget-padding" ng-if="is_modify_setting"></div>',
      link: function(scope, element, attrs){
        getData = function(){
          $http.get(djangoUrl.reverse('hosts-overall')).then(function(response){
            scope.data = response.data;
          });
        }
        $interval(getData, 30000);
        getData();
        // get data

        scope.$watch('data', function(newVal, oldVal){
          scope.render(newVal);
        }, true);
        // re render

        scope.render = function(data){
          if (data === undefined) return;
          // ignore data unbinding

          d3.select(element[0])
            .select('.charts')
            .selectAll('*')
            .remove();
          // erase all element

          var all = data.all;
          var up = data.up;
          var warning = data.warning;
          var critical = data.critical;

          var overall_data = [
            {label: 'up', data: up},
            {label: 'base', data: all - up}
          ];
          var warning_data = [
            {label: 'warning', data: warning},
            {label: 'up_base', data: up - warning},
            {label: 'base', data: all - up},
          ];
          var critical_data = [
            {label: 'critical', data: critical},
            {label: 'up_base', data: up - critical},
            {label: 'base', data: all - up},
          ];
          // data process

          var width = 200, height = 200, radius = 100
          var color = {
            base: '#C4C4C4',
            up_base: '#919191',
            up: '#5BB6FF',
            critical: '#FD6860',
            warning: '#FEEA5B',
          };
          // property

          var arc = d3.svg.arc()
            .outerRadius(radius - 10)
            .innerRadius(radius - 30)
          var pie = d3.layout.pie()
            .value(function(d){ return d.data })
            .sort(null)
          // arc, pie elements

          function draw_chart(title, data){
            var data1 = data[0].data;
            var data2 = data[1].data + data[0].data;
            var svg = d3.select(element[0]).select('.charts').append('svg')
              .attr('width', width)
              .attr('height', height)
              .append('g')
              .attr('transform', 'translate(' + (width / 2) + 
                ',' + (height / 2) + ')');
            var path = svg.selectAll('path')
              .data(pie(data))
              .enter()
              .append('path')
              .attr('d', arc)
              .attr('fill', function(d, i) {
                return color[d.data.label];
              });
            svg.append('text')
              .text(title)
              .attr('dy', '-2em')
              .style('text-anchor', 'middle')
              .style('font-size', '0.8em')
            svg.append('text')
              .text(data1)
              .attr('dy', '30px')
              .style('text-anchor', 'end')
              .style('font-size', Math.clamp((7.2 / data1.toString().length), 0, 3.6) + 'em')
            svg.append('text')
              .text('/' + data2)
              .attr('dy', '30px')
              .style('text-anchor', 'start')
              .style('font-size', Math.clamp((7.2 / (data2.toString().length + 1)), 0, 2.4) + 'em')
          };

          draw_chart('모니터링 호스트', overall_data);
          draw_chart('Critical 호스트', critical_data);
          draw_chart('Warning 호스트', warning_data);
        };
      },
    };
  }]);
