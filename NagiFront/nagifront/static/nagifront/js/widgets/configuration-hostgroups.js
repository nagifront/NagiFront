angular.module('nagifront')
  .directive('configurationHostgroups', ['$http', '$interval', 'djangoUrl', function($http, $interval, djangoUrl) {
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
                +'<th></th>'
                +'</tr>'
                +'<tr ng-repeat="group in lists">'
                +'<td>{{group.alias}}</td>'
                +'<td>{{group.address}}</td>'
                +'<td>{{group.parent_host}}</td>'
                +'<td>{{group.notes}}</td>'
                +'<td>{{group.check_period}}</td>'
                +'</tr>'
                +'</table>',
      link: function(scope, element, attrs) {
        scope.option = 'none';
        function getData() {
          if(scope.option !== attrs.option) {
             scope.option = attrs.option;
             $http.get(djangoUrl.reverse('hosts-groups-configurations')).then(function(response) {
                scope.data = response.data.hostgroups;
                  for(var i = 0; i < scope.data.length; i++) {
                    if(scope.data[i].group_name === scope.option) {
                      scope.lists = [];
                      scope.lists.push(scope.data[i]);
                      break;
                    }
                  }
             });
          }
        };
        $interval(getData, 1000);
        getData();

        window.onresize = function() {
          scope.$apply();
        };
        scope.$watch(function() {
          return angular.element(window)[0].innerWidth;
        }, function() {
          scope.$apply();
        });
      },
     };
   }]);
