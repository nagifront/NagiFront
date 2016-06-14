angular.module('nagifront')
  .directive('configurationHostgroups', ['$http', 'djangoUrl', function($http, djangoUrl) {
    return {
      restrict: 'EA',
      scope: true,
      template: '<h3>호스트 그룹 설정</h3>'
                +'<table class="charts">'
                +'<tr class="category">'
                +'<th>group name</th>'
                +'<th>description</th>'
                +'<th>host members</th>'
                +'<th>notes</th>'
                +'</tr>'
                +'<tr ng-repeat="group in lists">'
                +'<td><span>{{group.description}}</span></td>'
                +'<td>{{group.group_name}}</td>'
                +'<td>{{group.host_members}}</td>'
                +'<td>{{group.notes}}</td>'
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
          $http.get(djangoUrl.reverse('hosts-groups-configurations')).then(function(response) {
            scope.data = response.data.hostgroups;
            for(var i = 0; i < scope.data.length; i++) {
              if(scope.data[i].description === scope.option) {
                scope.lists = [];
                scope.lists.push(scope.data[i]);
                break;
              }
            }
          });
        });
      },
    };
  }]);
