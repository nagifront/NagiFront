angular.module('nagifront')
  .directive('configurationHostgroups', ['$http', 'djangoUrl', function($http, djangoUrl) {
    return {
      restrict: 'EA',
      scope: true,
      template: '<div class="block" ng-repeat="group in lists">'
                +'<h3>호스트 그룹 설정: {{ group.description }}</h3>'
                +'<button class="edit" ng-click="toEdit(group.hostgroup_object_id)"></button>'
                +'<table class="simple-charts">'
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
                +'</table>'
                +'</div>',
      link: function(scope, element, attrs) {
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
