angular.module('nagifront')
  .directive('hostStatusInformation',['d3','$http','$interval','djangoUrl',function(d3, $http, $interval, djangoUrl) {
  return {
    restrict: 'EA',
    scope: {
    },
    template: '<h3>호스트 상세 정보</h3><div class="charts">'
          +'<div class = "info">'
          +'<div><span class="category">Host </span><span class="name">{{host.alias}}</span></div>'
          +'<div><span class="category">Host Status </span><span class="state {{state[host.current_state]}}">{{state[host.current_state]}}</span> (for {{host.duration}})</div>'
          +'<div><span class="category">Status Information </span>{{host.output}}</div>'
          +'<div><span class="category">Current Attempt </span>{{host.current_check_attempt}} / {{host.max_check_attempts}}</div>'
          +'<div><span class="category">Last Check Time </span>{{host.last_check | date:"yyyy/MM/dd HH:mm:ss"}}</div>'
          +'<div><span class="category">Check Type </span>{{check_type[host.check_type]}}</div>'
          +'<div><span class="category">Check Latency / Duration </span>{{host.latency}} \ {{host.execution_time}}</div>'
          +'<div><span class="category">Next Check Time </span>{{host.next_check | date:"yyyy/MM/dd HH:mm:ss"}}</div>'
          +'<div><span class="category">Last State Change </span>{{host.last_state_change | date:"yyyy/MM/dd HH:mm:ss"}}</div>'
          +'<div><span class="category">Flapping </span><span class="state {{binary[host.is_flapping]}}">{{binary[host.is_flapping]}}</span></div>'
          +'<div><span class="category">Last Update </span>{{host.status_update_time | date:"yyyy/MM/dd HH:mm:ss"}}</div>'
          +'</div>'
          +'<div class = "enable_check">'
         +'<div><span class="category">Active Checks </span><span class="check {{enable[host.active_checks_enabled]}}">{{enable[host.active_checks_enabled]}}</span></div>'
          +'<div><span class="category">Passive Checks </span><span class="check {{enable[host.passive_checks_enabled]}}">{{enable[host.passive_checks_enabled]}}</span></div>'
          +'<div><span class="category">Failure Prediction </span><span class="check {{enable[host.failure_prediction_enabled]}}">{{enable[host.failure_prediction_enabled]}}</span></div>'
          +'<div><span class="category">Notification </span><span class="check {{enable[host.notifications_enabled]}}">{{enable[host.notifications_enabled]}}</span></div>'
          +'<div><span class="category">Event Handler </span><span class="check {{enable[host.event_handler_enabled]}}">{{enable[host.event_handler_enabled]}}</span></div>'
          +'<div><span class="category">Flap Detection </span><span class="check {{enable[host.flap_detection_enabled]}}">{{enable[host.flap_detection_enabled]}}</span></div>'
      +'</div>'
      +'</div>',
      link: function(scope, element, attrs) {
        scope.check_type = {0: 'ACTIVE', 1: 'PASSIVE'};
        scope.enable = {0: 'DISABLED', 1: 'ENABLED'};
        scope.binary = {0: 'NO', 1: 'YES'};
        scope.state = {0: 'UP', 2: 'UNREACHABLE', 1: 'DOWN'};
        var time = [1000 * 60 * 60 * 24, 1000 * 60 * 60, 1000 * 60, 1000];
        getData = function() {
          $http.get(djangoUrl.reverse('hosts-status')+'&host_id='+attrs.hostId).then(function(response) {
          scope.host = response.data.hosts[0];
          var milisec = new Date(scope.host.status_update_time) - new Date(scope.host.last_state_change);
          var day = parseInt(milisec / time[0]);
          var hour = parseInt((milisec - day * time[0]) / time[1]);
          var min = parseInt((milisec - day * time[0] - hour * time[1]) / time[2]);
          var sec = parseInt((milisec - day * time[0] - hour * time[1] - min * time[2]) / time[3]);
          scope.host.duration = day + 'd ' + hour + 'h ' + min + 'm ' + sec + 's ';
        });
        }
        $interval(getData, 30000);
        getData();
      }
    };
  }]);
