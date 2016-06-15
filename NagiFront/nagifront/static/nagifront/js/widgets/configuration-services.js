angular.module('nagifront')
  .directive('configurationServices', ['$http', 'djangoUrl', function($http, djangoUrl) {
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
                +'</tr>'
                +'<tr ng-repeat="service in lists">'
                +'<td><span>{{service.host}}</span></td>'
                +'<td><span>{{service.display_name}}</span></td>'
                +'<td>{{service.check_command}}</td>'
                +'<td>{{service.notes}}</td>'
                +'<td>{{service.check_period}}</td>'
                +'</tr>'
                +'</table>',
      link: function(scope, element, attrs) {
        scope.$watch('option', function(){
          $http.get(djangoUrl.reverse('hosts-services-configurations')).then(function(response) {
            scope.data = response.data.services;
            if(scope.option === 'All') {
              scope.lists = scope.data;
            }
            else {
              scope.lists = [];
              for(var i = 0; i < scope.data.length; i++) {
                if(scope.data[i].host === scope.option) {
                  scope.lists.push(scope.data[i]);
                }
              }
            }
          });
        });
      },
    };
  }]);
