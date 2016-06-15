angular.module('nagifront')
  .directive('hostTrend', ['d3', '$http', '$interval', 'djangoUrl', function(d3, $http, $interval, djangoUrl){
    return {
      restrict: 'EA',
      scope: true,
      template: '<h3>{{ data.host.display_name }}</h3><select ng-model="time"'
        + 'ng-options="type as type.name for type in list track by type.value">'
        + '</select>'
        + '<div class="charts"></div>',
      link: function(scope, element, attrs){
        scope.list = [
          { value: 12 * 60 * 60 * 1000, name: '12 hours' },
          { value: 24 * 60 * 60 * 1000, name: '24 hours' },
          { value: 2 * 24 * 60 * 60 * 1000, name: '2 days' },
          { value: 7 * 24 * 60 * 60 * 1000, name: '7 days' },
          { value: 14 * 24 * 60 * 60 * 1000, name: '2 weeks' },
        ]
        scope.time = scope.list[scope.type|0 * 1]
        // init data

        getData = function(){
          $http.get(djangoUrl.reverse('hosts-id-trend', { host_id: attrs.hostId })).then(function(response){
            scope.data = response.data;
          });
        }
        $interval(getData, 30000);
        getData();
        // get data

        scope.$watch('data', function(newVal){
          scope.render(scope.data);
        }, true);
        scope.$watch('time', function(newVal){
          scope.render(scope.data);
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

          var data_processed = [];
          var now = Date.now()
          var prev = now
          var limit = prev - scope.time.value;
          var last_state = null;
          angular.forEach(data.trends, function(trend){
            var end_time = new Date(trend.end_time).getTime()
            if (end_time < limit){
              if (last_state == null)
                last_state = trend.state;
              return;
            }
            data_processed.push({state: 4 - trend.state, interval: prev - end_time, time: new Date(end_time)});
            prev = end_time
          });
          data_processed.push({state: 4 - last_state, interval: prev - limit, time: new Date(limit)});
          // data process

          var margin = {top: 10, right: 60, bottom: 60, left: 110},
              width = 400 - margin.left - margin.right,
              height = 200 - margin.top - margin.bottom;
          color = [
            '#868686',
            '#f89c59',
            '#ef6a6a',
            '#8dd775',
          ]
          // property

          var svg = d3.select(element[0]).select('.charts').append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom)
            .append('g')
              .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

          var x = d3.scale.linear()
            .range([0, width])
            .domain([limit, now])
          var y = d3.scale.linear()
            .range([height, 0])
            .domain([0, 5]);
          var xAxis = d3.svg.axis()
            .scale(x)
            .orient('bottom')
            .ticks(0)
          var yAxis = d3.svg.axis()
            .scale(y)
            .orient('left')
            .ticks(0)

          svg.append('g')
            .attr('class', 'x axis')
            .attr('transform', 'translate(0, ' + height + ')')
            .call(xAxis)
          svg.append('g')
            .attr('class', 'y axis')
            .attr('trnsform', 'translate(' + width + ', 0)')
            .call(yAxis)

          svg.selectAll('.bar')
            .data(data_processed)
            .enter().append('rect')
              .attr('class', 'bar')
              .attr('x', function(d) { return x(d.time); })
              .attr('width', function(d) { return Math.max((d.interval) / (x.invert(1) - x.invert(0)), 3)})
              .attr('y', function(d) { return y(d.state); })
              .attr('height', function(d) { return height - y(d.state); })
              .attr('fill', function(d) { return color[d.state - 1] })

          var xLabel = [{s: 1, n: 'Indeterminate'}, {s: 2, n: 'Unreachable'}, {s: 3, n: 'Down'}, {s: 4, n: 'Up'}]
          svg.selectAll('.x-gridline')
            .data(xLabel)
            .enter().append('path')
              .attr('class', 'x-gridline')
              .attr('d', function(d) { return 'M' + 0 + ' ' + (y(d.s)) + ' L' + width + ' ' + (y(d.s))})
              .attr('stroke', '#eeeeee')
              .attr('stroke-width', '1')
          svg.selectAll('.x-ticks')
            .data(xLabel)
            .enter().append('text')
              .attr('class', 'x-ticks')
              .text(function(d) { return d.n })
              .attr('x', -10)
              .style('text-anchor', 'end')
              .attr('y', function(d) { return y(d.s) + margin.top })

          var interval = (now - limit) / 3;
          var yLabel = [0, 1, 2, 3]
          svg.selectAll('.y-gridline')
            .data(yLabel)
            .enter().append('path')
              .attr('class', 'y-gridline')
              .attr('d', function(d) { return 'M' + (x(now + interval * (3 - d)) - width) + ' ' + 20 + ' L' + (x(now + interval * (3 - d)) - width) + ' ' + height})
              .attr('stroke', '#000')
              .attr('stroke-opacity', 0.5)
              .attr('stroke-width', '1')
              .attr('stroke-dasharray', 10)
          var yTicks = svg.selectAll('.y-ticks')
            .data(yLabel)
            .enter().append('text')
              .attr('class', 'y-ticks')
              .attr('y', function(d) { return height + margin.top })
          yTicks.append('tspan')
            .text(function(d) {
              var date = new Date(now - interval * d);
              return (date.getMonth() + 1) + '/' + (date.getDate())
            })
            .attr('x', function(d) { return x(now + interval * (3 - d) * 0.9) - width })
            .attr('dy', '1em')
          yTicks.append('tspan')
            .text(function(d) {
              var date = new Date(now - interval * d);
              return date.getHours() + ':' + date.getMinutes() + ':' + date.getSeconds() 
            })
            .attr('x', function(d) { return x(now + interval * (3 - d) * 0.9) - width })
            .attr('dy', '1em')
        };
      },
    };
  }]);

angular.module('nagifront')
  .directive('hostTrendGroup', ['d3', '$http', 'djangoUrl', function(d3, $http, djangoUrl){
    return {
      restrict: 'EA',
      scope: true,
      template: '<h3>호스트 트렌드 - <select name="host-group-id" ng-model="host_group_id"'
        + 'ng-options="hostgroup_id.hostgroup_object_id as hostgroup_id.name for hostgroup_id in hostgroup_ids" ng-disabled="!is_modify_setting"></select></h3>'
        + '<div class="charts" ng-if="!is_modify_setting">'
          + '<scrollable always-visible="true">'
            + '<div ng-repeat="member in members" host-trend host_id="{{ member }}">'
          + '</scrollable>'
        + '</div>'
        + '<div class="widget-padding" ng-if="is_modify_setting"></div>',
      link: function(scope, element, attrs){
        scope.host_group_id = attrs.hostGroupId * 1;
        $http.get(djangoUrl.reverse('hosts-groups') + '&host_group_id' + attrs.hostGroupId).then(function(response){
          scope.members = response.data[attrs.hostGroupId].members
          scope.group_name = response.data[attrs.hostGroupId].alias
        });
        // get data
      },
    };
  }]);
