angular.module('nagifront')
  .directive('configurationHosts', ['$http', 'djangoUrl', function($http, djangoUrl) {
    return {
      restrict: 'EA',
      scope: true,
      template: '<div class="block" ng-repeat="host in lists">'
                +'<h3>호스트 설정: {{ host.alias }}</h3>'
                +'<table class="simple-charts">'
                +'<tr class="category">'
                +'<th>host name</th><th>address</th><th>parent hosts</th><th>notes</th><th>check period</th>'
                +'</tr>'
                +'<tr>'
                +'<td><span>{{host.alias}}</span></td><td>{{host.address}}</td><td>{{host.parent_host}}</td><td>{{host.notes}}</td><td>{{host.check_period}}</td>'
                +'</tr></table>'
                +'<button class="detailed-button" ng-click="toggleSimple(host.alias)"><span ng-if="isSimple(host.alias)">show more</span><span ng-if="!isSimple(host.alias)">hide</span></button>'
                +'<div class="detail-contents" ng-if="!isSimple(host.alias)">'
                +'<table class="detailed-charts">'
                +'<tr class="category">'
                +'<th>default contacts</th><th>max check attempts</th><th>check interval</th><th>retry interval</th><th>host check command</th>'
                +'<tr>'
                +'<td>{{host.contact_group}}</td><td>{{host.max_check_attempts}}</td><td>{{host.check_interval}} m</td><td>{{host.retry_interval}} m</td><td>TODO</td>'
                +'</tr></table>'
                +'<table class="detailed-charts">'
                +'<tr class="category">'
                +'<th>notification period</th><th>notification interval</th><th>first notification delay</th><th>notification option</th><th>enable notification</th>'
                +'<tr>'
                +'<td>{{host.notification_period}}</td><td>{{host.notification_interval}} m</td><td>{{host.first_notification_delay}} m</td><td>{{down[host.notify_on_down]}} {{recovery[host.nofity_on_recovery]}} {{unreachable[host.notify_on_unreachable]}} {{flapping[host.notify_on_flapping]}} {{downtime[host.notify_on_downtime]}}</td><td>{{binary[host.notifications_enabled]}}</td>'
                +'</tr></table>'
                +'<table class="detailed-charts">'
                +'<tr class="category">'
                +'<th>enable active check</th><th>enable passive check</th><th>enable flap detection</th><th>enable freshness checks</th><th>enable event handler</th>'
                +'<tr>'
                +'<td>{{binary[host.active_checks_enabled]}}</td><td>{{binary[host.passive_checks_enabled]}}</td><td>{{binary[host.flap_detection_enabled]}}</td><td>{{binary[host.freshness_checks_enabled]}}</td><td>{{binary[host.event_handler_enabled]}}</td>'
                +'</tr></table>'
                +'</div>'
                +'</div>',
      link: function(scope, element, attrs) {
        scope.binary = {'0': 'No', '1':'Yes'};
        scope.down = {'0': '', '1':'down'};
        scope.downtime = {'0': '', '1':'downtime'};
        scope.recovery = {'0': '', '1':'recovery'};
        scope.flapping = {'0': '', '1':'flapping'};
        scope.unreachable = {'0': '', '1':'unreachable'};
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
