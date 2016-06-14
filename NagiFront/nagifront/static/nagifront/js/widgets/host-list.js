angular.module('nagifront')
  .directive('hostServiceState', ['d3', '$http', '$interval', 'djangoUrl', function(d3, $http, $interval, djangoUrl) {
    return {
      restrict: 'EA',
      scope: true,
      template: '<span class="host-name">{{alias}}</span>'
        +'<span class="state Ok"><span>{{Ok}}</span> Ok</span>'
        +'<span class="state Warning"><span>{{Warning}}</span> Warning</span>'
        +'<span class="state Critical"><span>{{Critical}}</span> Critical</span>',
      link: function(scope, element, attrs) {
        $http.get(djangoUrl.reverse('hosts-status')+'&host_id='+attrs.hostId).then(function(response_status) {
          scope.alias = response_status.data.hosts[0].alias;
         });

        getData = function() {
          $http.get(djangoUrl.reverse('hosts-services')+'&host_id='+attrs.hostId).then(function(response_services) {
            host_value = response_services.data.state_number;
            scope.Ok = host_value.Ok;
            scope.Warning = host_value.Warning;
            scope.Critical = host_value.Critical;
          });
        }

        $interval(getData, 30000);
        getData();

        window.onresize = function(){
          scope.$apply();
        };

        scope.$watch(function(){
          return angular.element(window)[0].innerWidth;
        }, function() {
          scope.$apply();
        });
      },
    };
  }]);

angular.module('nagifront')
  .directive('hostList',['d3','$http','$interval','djangoUrl',function(d3, $http, $interval, djangoUrl) {
    return {
      restrict: 'EA',
      scope: true,
      template: '<h3>호스트 목록 - <select name="host-group-id" ng-model="host_group_id"'
        + 'ng-options="hostgroup_id.hostgroup_object_id as hostgroup_id.name for hostgroup_id in hostgroup_ids" ng-disabled="!is_modify_setting"></select></h3><div class="charts" ng-if="!is_modify_setting">'
        +'<scrollable always-visible="true">'
          +'<div class="hosts" ng-repeat="host in hosts" host-service-state host_id="{{ host }}">'
          +'</div>'
        +'</scrollable>'
        +'</div>'
        + '<div class="widget-padding" ng-if="is_modify_setting"></div>',
      link: function(scope, element, attrs) {
        scope.host_group_id = attrs.hostGroupId * 1;
        $http.get(djangoUrl.reverse('hosts-groups')).then(function(response) {
          scope.hosts = response.data[attrs.hostGroupId].members;
        });
      },
    };
  }]);
