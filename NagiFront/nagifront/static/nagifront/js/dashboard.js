app.controller('dashboard', function($scope, $http, $compile, djangoUrl){
  $scope.is_modify_setting = false;
  $scope.modify_enable = function(){
    $scope.is_modify_setting = true;
    $scope.backup = JSON.parse(JSON.stringify($scope.user_setting.widget_setting));
    $scope.load_widget(true);
    draw_widgets($scope.user_setting.widget_setting);
  }
  $scope.save = function(){
    $scope.load_widget(false);
    draw_widgets($scope.user_setting.widget_setting);
    $http.post(djangoUrl.reverse('update-user'), {
      data: $scope.user_setting,
    }).then(function(response){
      if (response.data.result){
        $scope.is_modify_setting = false;
        $scope.show_modal = true;
        $scope.message = '저장되었습니다';
      } else {
        $scope.show_modal = true;
        $scope.message = '저장에 실패했습니다. 다시 시도해주세요';
      }
    })
  }
  $scope.cancel = function(){
    $scope.is_modify_setting = false;
    $scope.user_setting.widget_setting = JSON.parse(JSON.stringify($scope.backup));
    draw_widgets($scope.user_setting.widget_setting);
  }
  $scope.load_widget = function(is_adding_empty_row){
    var dashboard = angular.element(document.querySelector( '#widgets' ))
    var widget_setting = [];
    angular.forEach(dashboard.children(), function(widget_row){
      var widget_row_information = [];
      var num = 0;
      angular.forEach(widget_row.children, function(widget_wrapper){
        var widget = widget_wrapper.children[1];
        var widget_config = {};
        widget_config['name'] = widget.attributes[1].name;
        var selects = angular.element(widget).find('select')
        var attr = {};
        angular.forEach(selects, function(select){
          if (select.name !== ''){
            attr[select.name] = select.value.split(':')[1];
          }
        })
        widget_config['attr'] = attr;
        if (num++ >= 2){
          $scope.widget_limit_modal_enable();
          return;
        }
        widget_row_information.push(widget_config);
      })
      widget_setting.push(widget_row_information);
    })
    // load
    widget_setting_reformed = [[]];
    angular.forEach(widget_setting, function(row){
      if (row.length !== 0){
        widget_setting_reformed.push(row);
        if (is_adding_empty_row)
          widget_setting_reformed.push([]);
      }
    })
    $scope.user_setting.widget_setting = widget_setting_reformed;
  }
  $http.get(djangoUrl.reverse('hosts-ids')).then(function(response) {
    $scope.host_ids = response.data.ids;
  });
  $http.get(djangoUrl.reverse('hosts-groups-ids')).then(function(response) {
    $scope.hostgroup_ids = response.data.ids;
  });
  $scope.user_setting = user_setting;
  /*{
    widget_setting: [
      [
      ], // row
    ],
  };*/

  function draw_widgets(widget_setting){
    var dashboard = angular.element(document.querySelector( '#dashboard' ))
    var widgets = angular.element(document.querySelector( '#widgets' ))
    var innerHTML = '';
    angular.forEach(widget_setting, function(widget_row, i){
      var widget_row_element = '<div class="widget-row" ng-model="user_setting.widget_setting['+ i +']" '
        + 'data-drop="true" jqyoui-droppable="{ multiple: true, onDrop: \'redraw\' }" '
        + 'data-jqyoui-options="{accept: \'.new-widget\'}">';
      angular.forEach(widget_row, function(widget, j){
        var widget_element = '<div class="widgets-wrapper">';
        widget_element += '<span ng-show="is_modify_setting" class="delete-button" ng-click="erase('+ i +', '+ j +')">X</span>';
        widget_element += '<div class="widgets" ';
        widget_element += widget.name;
        angular.forEach(widget.attr, function(value, key){
          widget_element += ' ' + key + '=' + value;
        })
        widget_element += '></div>';
        widget_element += '</div>';
        widget_row_element += widget_element;
      })
      widget_row_element += '</div>';
      innerHTML += widget_row_element;
    })
    widgets.html(innerHTML);
    $compile(dashboard)($scope)
  }
  draw_widgets($scope.user_setting.widget_setting);
  $scope.redraw = function(){
    widget_setting_reformed = [[]];
    angular.forEach($scope.user_setting.widget_setting, function(row){
      if (row.length !== 0){
        if (row.length > 2){
          row = row.slice(0, 2);
          $scope.widget_limit_modal_enable();
        }
        widget_setting_reformed.push(row);
        widget_setting_reformed.push([]);
      }
    })
    $scope.user_setting.widget_setting = widget_setting_reformed;
    draw_widgets($scope.user_setting.widget_setting);
  }
  $scope.erase = function(i, j){
    if ($scope.is_modify_setting){
      if (confirm('정말로 삭제할까요?')){
        $scope.user_setting.widget_setting[i].splice(j, 1);
        $scope.redraw()
      }
    }
  }

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
    { name: 'service-number-by-state-chart', attr: {} },
    { name: 'trouble-host', attr: {} },
    { name: 'service-trend-host', attr: {} },
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
    'service-trend-host': '서비스 트렌드',
  };

  $scope.show_modal = false;
  $scope.widget_limit_modal_enable = function(){
    $scope.show_modal = true;
    $scope.message = '한 줄에 2개 이상의 위젯을 둘 순 없습니다';
  }
  $scope.close_modal = function(){
    $scope.show_modal = false;
  }
})
