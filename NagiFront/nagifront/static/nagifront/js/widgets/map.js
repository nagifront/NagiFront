angular.module('nagifront')
  .directive('map', ['d3', '$http', '$interval', 'djangoUrl', function(d3, $http, $interval, djangoUrl){
    return {
      restrict: 'EA',
      scope: true,
      template: '<h3>맵</h3><div class="charts"><div class="map-wrapper"></div></div><div class="tooltip"></div>',
      link: function(scope, element, attrs){
        getData = function(){
          $http.get(djangoUrl.reverse('hosts-parent-information')).then(function(response){
            scope.dependency = response.data.host_dependency;
            scope.render();
          });
          $http.get(djangoUrl.reverse('hosts-status')).then(function(response){
            scope.hosts = response.data.hosts;
            scope.render();
          });
        }
        $interval(getData, 30000);
        getData();
        // get data
        
        window.onresize = function() {
          scope.$apply();
        };
        scope.$watch(function() {
        return angular.element(window)[0].innerWidth;
        }, function() {
          scope.render();
        });

        var map_wrapper = element[0].children[1].children[0];
        var tooltip = element[0].children[2];

        var is_first = true;
        scope.render = function() {
          if (scope.dependency === undefined || scope.hosts === undefined) return;
          
          d3.select(element[0])
            .select('.charts')
            .select('.map-wrapper')
            .selectAll('*')
            .remove();
          // erase all element
          
          var hosts_processed = {};
          angular.forEach(scope.hosts, function(h, k){
            hosts_processed[h.host_object_id] = h;
          });

          var dependency_processed = {};
          angular.forEach(scope.dependency, function(e){
            e['children'] = [];
            e['host'] = hosts_processed[e.host_object_id];
            dependency_processed[e.host_object_id] = e;
          });
          dependency_processed[null] = {children: [], }; // add root node
          angular.forEach(dependency_processed, function(d, k){
            var node = dependency_processed[d.parent_host_object_id];
            if (node !== undefined)
              node.children.push(d.host_object_id);
          });
          // set children nodes

          var root = dependency_processed[null];
          var level = 0;
          var max_level = 0;
          var www = 0;
          var startw = 0;
          var cal = function (node){
            level++;
            if (node.children.length === 0){
              node['weight'] = 1;
              node['startw'] = startw;
              startw++;
            } else {
              node['weight'] = 0;
              node['startw'] = startw;
              for (var i = 0; i < node.children.length; i++){
                node['weight'] += cal(dependency_processed[node.children[i]]);
              }
            }
            node['level'] = level;
            if (max_level < level) max_level = level;
            level--;
            return node['weight'];
          }
          // calculate 
          var total_weight = cal(root);
          // data process

          var radius = 75,
              width = max_level * radius * 2,
              height = max_level * radius * 2;
          var color = {
            null: 'white', // root
            0: '#8DD775', // up
            1: '#EF6A6A', // down
            2: '#F89C59', // unreachable
          };
          // property

          var arc = d3.svg.arc()
            .startAngle(function(d) { return d.data.startw * 2 * Math.PI / total_weight; })
            .endAngle(function(d) { return (d.data.startw + d.data.weight) * 2 * Math.PI / total_weight; })
            .innerRadius(function(d) { return radius * (d.data.level - 1.5) })
            .outerRadius(function(d) { return radius * (d.data.level - 0.5) });
          var pie = d3.layout.pie()
            .value(function(d){ return d.weight })
            .sort(null)
          // arc, pie

          var svg = d3.select(element[0]).select('.charts')
            .select('.map-wrapper').append('svg')
            .attr('width', width)
            .attr('height', height)
            .append('g')
            .attr('transform', 'translate(' + (width / 2) + 
              ',' + (height / 2) + ')');

          Object.values = function(data){
            var arr = [];
            angular.forEach(data, function(v, k){
              arr.push(v);
            });
            return arr;
          }
          function show_information(alias, host){
            tooltip.innerHTML = '<h4>Host Information</h4>'
                + '<table>'
                  + '<tr><th>'+ 'Alias' +'</th>'
                  + '<td>'+ alias +'</td></tr>'
                  + '<tr><th>'+ 'Stat Info' +'</th>'
                  + '<td>'+ host.output +'</td></tr>'
                  + '<tr><th>'+ 'Last Check' +'</th>'
                  + '<td>'+ host.last_check +'</td></tr>'
                  + '<tr><th>'+ 'Last Change' +'</th>'
                  + '<td>'+ host.last_state_change +'</td></tr>'
                  + '<tr><th>'+ 'Immediate Child Host' +'</th>'
                  + '<td>'+ dependency_processed[host.host_object_id].children.length +'</td></tr>'
                + '</table>'
            tooltip.style.display = 'block';
            tooltip.style.top = (window.scrollY + event.clientY - element[0].offsetTop - 170) + 'px';
            tooltip.style.left = (window.scrollX + event.clientX - element[0].offsetLeft - 40) + 'px';
          }
          function hide_information(){
            tooltip.style.display = 'none';
          }
          var wrap = function (word){
            if (word.length < 16)
              return word;
            else {
              word = word.substring(0, 15);
              word += '...';
              return word;
            }
          }
          // set functions

          delete dependency_processed[null];
          var path = svg.selectAll('path')
            .data(pie(Object.values(dependency_processed)))
            .enter()
            .append('path')
            .attr('d', arc)
            .attr('fill', function(d){
                return color[d.data.host.current_state];
              })
            .attr('stroke', '#e6e6e6')
          svg.selectAll('image')
            .data(Object.values(dependency_processed))
            .enter()
            .append('image')
            .attr('fill', 'transparent')
            .attr('x', function(d){
              return Math.cos((d.startw + d.startw + d.weight) * (Math.PI / total_weight) - 1.570796) * ((d.level - 1) * radius) - 20
            })
            .attr('y', function(d){
              return Math.sin((d.startw + d.startw + d.weight) * (Math.PI / total_weight) - 1.570796) * ((d.level - 1) * radius) - 20
            })
            .attr('xlink:href', host_image_url)
            .attr('width', '40px')
            .attr('height', '40px')
            .style('cursor', 'pointer')
            .on('mouseenter', function(d){ show_information(d.alias, d.host); })
            .on('mouseleave', function(d){ hide_information(); })
          svg.selectAll('text')
            .data(Object.values(dependency_processed))
            .enter()
            .append('text')
            .text(function(d){ return wrap(d.alias) })
            .attr('text-anchor', 'middle')
            .attr('font-size', '0.75em')
            .attr('font-weight', 'bold')
            .attr('x', function(d){
              return Math.cos((d.startw + d.startw + d.weight) * (Math.PI / total_weight) - 1.570796) * ((d.level - 1) * radius)
            })
            .attr('y', function(d){
              return Math.sin((d.startw + d.startw + d.weight) * (Math.PI / total_weight) - 1.570796) * ((d.level - 1) * radius) + 33
            })

          if (is_first){
            map_wrapper.scrollTop = width / 2 - (element[0].children[1].children[0].offsetWidth / 2)
            map_wrapper.scrollLeft = height / 2 - (element[0].children[1].children[0].offsetHeight /2 )
            is_first = false;
          }
        }
      },
    };
  }]);
