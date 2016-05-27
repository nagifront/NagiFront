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
          $http.get(djangoUrl.reverse('hosts-groups-hosts-state') + '&host_group_id=' + attrs.hostGroupId).then(function(response) {
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
          
          var up = data[attrs.hostGroupId].up;
          var down = data[attrs.hostGroupId].down;
          var unreachable = data[attrs.hostGroupId].unreachable;
          
          var overall_data = [
            {label: 'Up', data: up},
            {label: 'Down', data: down},
            {label: 'Unreachable', data: unreachable},
          ];

          var width = 200, height = 200, radius = 100
          var color = {
            Up: '#8DD775',
            Down: '#EF6A6A',
            Unreachable: '#F89C59',
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
              
            function add_text(i) {
              svg.append('text')
              .text(data[i].label+"  :     "+ data[i].data*100/total+' %    ('+data[i].data+')')
              .attr('dy',(-70+25*i)+'px')
              .attr('dx','240px')
              .style('text-anchor','end')
              .style('font-size', '0.8em');
            };
            add_text(0);
            add_text(1);
            add_text(2);
          };
          draw_chart(overall_data);
        };
      },
    };
  }]);
