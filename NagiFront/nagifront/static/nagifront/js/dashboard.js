app.controller('dashboard', function($scope, $http, $compile, djangoUrl){
  $http.get(djangoUrl.reverse('hosts-ids')).then(function(response) {
    $scope.host_ids = response.data.ids;
  });
  $http.get(djangoUrl.reverse('hosts-groups-ids')).then(function(response) {
    $scope.hostgroup_ids = response.data.ids;
  });
  $scope.user_setting = {
    widget_setting: [
      [
        {
          name: 'map',
          attr: {},
        },
        {
          name: 'trouble-host',
          attr: {},
        },
      ], // row
      [
        {
          name: 'host-state-change',
          attr: {},
        },
        {
          name: 'host-status',
          attr: { host_group_id: 189 },
        },
      ],
      [
        {
          name: 'host-status',
          attr: { host_group_id: 185 },
        },
      ],
      [
        {
          name: 'host-trend-group',
          attr: { host_group_id: 189 },
        },
        {
          name: 'host-trend-group',
          attr: { host_group_id: 185 },
        },
      ],
      [
        {
          name: 'service-number-by-state',
          attr: {},
        },
        {
          name: 'service-number-by-state-chart',
          attr: {},
        },
      ],
      [
        {
          name: 'scheduled-downtime',
          attr: {},
        },
      ],
      [
        {
          name: 'check-schedules',
          attr: {},
        },
      ],
      [
        {
          name: 'comments',
          attr: {},
        },
      ],
      [
        {
          name: 'host-list',
          attr: { host_group_id: 189, },
        },
        {
          name: 'host-list',
          attr: { host_group_id: 185, },
        },
      ],
      [
        {
          name: 'trouble-trend',
          attr: { host_group_id: 185, 'time-scale': 'week' },
        },
        {
          name: 'trouble-trend',
          attr: { host_group_id: 189, 'time-scale': 'day' },
        },
      ],
    ],
  };

  function draw_widgets(widget_setting){
    var dashboard = angular.element(document.querySelector( '#dashboard' ))
    var innerHTML = '<div class="widget_row"><div class="widgets" overall-host></div></div>';
    angular.forEach(widget_setting, function(widget_row){
      var widget_row_element = '<div class="widget_row">';
      angular.forEach(widget_row, function(widget){
        var widget_element = '<div ';
        widget_element += widget.name;
        angular.forEach(widget.attr, function(value, key){
          widget_element += ' ' + key + '=' + value;
        })
        widget_element += ' configuration=' + JSON.stringify(widget) + '></div>';
        widget_row_element += widget_element;
      })
      widget_row_element += '</div>';
      innerHTML += widget_row_element;
    })
    dashboard.html(innerHTML);
    $compile(dashboard)($scope)
  }
  draw_widgets($scope.user_setting.widget_setting);
})
