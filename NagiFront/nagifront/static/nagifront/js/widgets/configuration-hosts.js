angular.module('nagifront')
  .directive('configurationHosts', ['$http', 'djangoUrl', function($http, djangoUrl) {
    return {
      restrict: 'EA',
      scope: true,
      template: '<h3>호스트 설정</h3>'
                +'<table class="charts">'
                +'<tr class="category">'
                +'<th>host name</th>'
                +'<th>address</th>'
                +'<th>parent hosts</th>'
                +'<th>notes</th>'
                +'<th>check period</th>'
                +'</tr>'
                +'<tr ng-repeat="host in lists">'
                +'<td><span>{{host.alias}}</span></td>'
                +'<td>{{host.address}}</td>'
                +'<td>{{host.parent_host}}</td>'
                +'<td>{{host.notes}}</td>'
                +'<td>{{host.check_period}}</td>'
                +'</tr>'
                +'</table>',
      link: function(scope, element, attrs) {
        window.onresize = function() {
          scope.$apply();
        };
        scope.$watch(function() {
          return angular.element(window)[0].innerWidth;
        }, function() {
          scope.$apply();
        });

        scope.$watch('option', function(){
          $http.get(djangoUrl.reverse('hosts-configurations')).then(function(response) {
            scope.data = response.data.host_configurations;
            if(scope.option === 'All') {
              scope.lists = scope.data;
            }
            else {
              for(var i = 0; i < scope.data.length; i++) {
                if(scope.data[i].alias === scope.option) {
                  scope.lists = [];
                  scope.lists.push(scope.data[i]);
                  break;
                }
              }
            }
          });
        });
      },
    };
  }]);
