app.controller('dashboard', function($scope, $http, $compile, djangoUrl){
  $scope.is_modify_setting = false;
  $scope.modify_enable = function(){
    $scope.is_modify_setting = true;
    $scope.backup = JSON.parse(JSON.stringify($scope.user_setting.widget_setting));
  }
  $scope.save = function(){
    var dashboard = angular.element(document.querySelector( '#widgets' ))
    var widget_setting = [];
    angular.forEach(dashboard.children(), function(widget_row){
      var widget_row_information = [];
      angular.forEach(widget_row.children, function(widget){
        var widget_config = {};
        widget_config['name'] = widget.attributes[0].name;
        var selects = angular.element(widget).find('select')
        var attr = {};
        angular.forEach(selects, function(select){
          if (select.name !== ''){
            attr[select.name] = select.value.split(':')[1];
          }
        })
        widget_config['attr'] = attr;
        widget_row_information.push(widget_config);
      })
      widget_setting.push(widget_row_information);
    })
    $scope.user_setting.widget_setting = widget_setting;
    draw_widgets($scope.user_setting.widget_setting);
    $scope.is_modify_setting = false;
  }
  $scope.cancel = function(){
    $scope.is_modify_setting = false;
    $scope.user_setting.widget_setting = JSON.parse(JSON.stringify($scope.backup));
  }
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
          name: 'overall-host',
          attr: {},
        }
      ],
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
    var dashboard = angular.element(document.querySelector( '#widgets' ))
    var innerHTML = '';
    angular.forEach(widget_setting, function(widget_row){
      var widget_row_element = '<div class="widget_row">';
      angular.forEach(widget_row, function(widget){
        var widget_element = '<div ';
        widget_element += widget.name;
        angular.forEach(widget.attr, function(value, key){
          widget_element += ' ' + key + '=' + value;
        })
        widget_element += '></div>';
        widget_row_element += widget_element;
      })
      widget_row_element += '</div>';
      innerHTML += widget_row_element;
    })
    dashboard.html(innerHTML);
    $compile(dashboard)($scope)
  }
  draw_widgets($scope.user_setting.widget_setting);

  $scope.widget_num = {};
  angular.forEach($scope.user_setting.widget_setting, function(widget_row){
    angular.forEach(widget_row, function(widget){
      if ($scope.widget_num[widget.name] === undefined) $scope.widget_num[widget.name] = 1;
      else $scope.widget_num[widget.name] += 1;
    })
  })
  
  $scope.widget_list = [
    { name: 'check-schedules', attr: {} },
    { name: 'host-list', attr: {} },
    { name: 'host-status', attr: {} },
    { name: 'scheduled-downtime', attr: {} },
    { name: 'host-state-change', attr: {} },
    { name: 'comments', attr: {} },
    { name: 'map', attr: {} },
    { name: 'service-number-by-state', attr: {} },
    { name: 'trouble-trend', attr: {} },
    { name: 'host-trend-group', attr: {} },
    { name: 'overall-host', attr: {} },
    { name: 'service-number-by-state-chart', attr: {} },
    { name: 'trouble-host', attr: {} },
  ];
  $scope.widget_name_map = {
    'check-schedules': '체크 스케쥴',
    'host-list': '호스트 목록',
    'host-status': '호스트 현황',
    'scheduled-downtime': '다운타임 스케쥴',
    'host-state-change': '호스트 상태 변화',
    'comments': '코멘트 현황',
    'map': '맵',
    'service-number-by-state': '그룹별 서비스 현황',
    'trouble-trend': '문제 발생 트렌드',
    'host-trend-group': '호스트 트렌드',
    'overall-host': '호스트 상태',
    'service-number-by-state-chart': '그룹별 서비스 현황 (그래프)',
    'trouble-host': '문제 발생 호스트',
  };
})
