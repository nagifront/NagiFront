angular.module('nagifront')
  .directive('configurationServices', ['$http', '$interval', 'djangoUrl', function($http, $interval, djangoUrl) {
    return {
      restrict: 'EA',
      scope: true,
      template: '<h3>서비스 설정</h3>'
                +'<table class="charts">'
                +'<tr class="category">'
                +'<th>host</th>'
                +'<th>description</th>'
                +'<th>check command</th>'
                +'<th>notes</th>'
                +'<th>check period</th>'
                +'<th></th>'
                +'</tr>'
                +'<tr ng-repeat="service in lists">'
                +'<td>{{service.alias}}</td>'
                +'<td>{{service.display_name}}</td>'
                +'<td>{{service.check_command}}</td>'
                +'<td>{{service.notes}}</td>'
                +'<td>{{service.check_period}}</td>'
                +'</tr>'
                +'</table>',
      link: function(scope, element, attrs) {
        scope.option = 'none';
        function getData() {
          if(scope.option !== attrs.option) {
             scope.option = attrs.option;
             $http.get(djangoUrl.reverse('hosts-services-configurations')).then(function(response) {
                scope.data = response.data.services;
                if(scope.option === 'All') {
                  scope.lists = scope.data;
                }
                else {
                  for(var i = 0; i < scope.data.length; i++) {
                    scope.lists = [];
                    if(scope.data[i].host === scope.option) {
                      scope.lists.push(scope.data[i]);
                    }
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
