angular.module('nagifront')
  .directive('configurationServices', ['$http', 'djangoUrl', function($http, djangoUrl) {
    return {
      restrict: 'EA',
      scope: true,
      template: '<div class="block" ng-repeat="service in lists">'
                +'<h3>서비스 설정: {{service.host}} - {{ service.display_name }}</h3>'
                +'<button class="edit" ng-click="toEdit(service.service_object_id)"></button>'
                +'<table class="simple-charts">'
                +'<tr class="category">'
                +'<th>host</th>'
                +'<th>description</th>'
                +'<th>check command</th>'
                +'<th>notes</th>'
                +'<th>check period</th>'
                +'</tr>'
                +'<tr>'
                +'<td><span>{{service.host}}</span></td>'
                +'<td><span>{{service.display_name}}</span></td>'
                +'<td>{{service.check_command}}</td>'
                +'<td>{{service.notes}}</td>'
                +'<td>{{service.check_period}}</td>'
                +'</tr>'
                +'</table>'
                +'<button class="detailed-button" ng-click="toggleSimple(service.host+service.display_name)"><span ng-if="isSimple(service.host+service.display_name)">show more</span><span ng-if="!isSimple(service.host+service.display_name)">hide</span></button>'
                +'<div class="detail-contents" ng-if="!isSimple(service.host+service.display_name)">'
                +'<table class="detailed-charts">'
                +'<tr class="category">'
                +'<th>default contacts</th><th>max check attempts</th><th>check interval</th><th>retry interval</th><th>check check command</th>'
                +'<tr>'
                +'<td>{{service.contact_group}}</td><td>{{service.max_check_attempts}}</td><td>{{service.check_interval}} m</td><td>{{service.retry_interval}} m</td><td>{{service.check_command}}</td>'
                +'</tr></table>'
                +'<table class="detailed-charts">'
                +'<tr class="category">'
                +'<th>notification period</th><th>notification interval</th><th>first notification delay</th><th>notification option</th><th>enable notification</th>'
                +'<tr>'
                +'<td>{{service.notification_period}}</td><td>{{service.notification_interval}} m</td><td>{{service.first_notification_delay}} m</td><td>{{warning[service.notify_on_warning]}} {{critical[service.notify_on_critical]}} {{recovery[service.nofity_on_recovery]}} {{unknown[service.notify_on_unknown]}} {{flapping[service.notify_on_flapping]}} {{downtime[service.notify_on_downtime]}}</td><td>{{binary[service.notifications_enabled]}}</td>'
                +'</tr></table>'
                +'<table class="detailed-charts">'
                +'<tr class="category">'
                +'<th>enable active check</th><th>enable passive check</th><th>enable flap detection</th><th>enable freshness checks</th><th>enable event handler</th>'
                +'<tr>'
                +'<td>{{binary[service.active_checks_enabled]}}</td><td>{{binary[service.passive_checks_enabled]}}</td><td>{{binary[service.flap_detection_enabled]}}</td><td>{{binary[service.freshness_checks_enabled]}}</td><td>{{binary[service.event_handler_enabled]}}</td>'
                +'</tr></table>'
                +'</div>'
                +'</div>',
      link: function(scope, element, attrs) {
        scope.binary = {'0': 'No', '1':'Yes'};
        scope.critical = {'0': '', '1':'critical'};
        scope.warning = {'0': '', '1':'warning'};
        scope.downtime = {'0': '', '1':'downtime'};
        scope.recovery = {'0': '', '1':'recovery'};
        scope.flapping = {'0': '', '1':'flapping'};
        scope.unknown = {'0': '', '1':'unknown'};
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
