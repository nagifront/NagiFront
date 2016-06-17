angular.module('nagifront')
  .directive('dynamicSelect', ['$http', '$interval', 'djangoUrl', function($http, $interval, djangoUrl) {
    return {
      restrict: 'EA',
      scope: true,
      template: '<select ng-model="selected" ng-change="update(selected)">'
          +'<option ng-repeat="item in lists" value="{{ item }}">{{ item }}</option>'
          +'</select>',
      link: function(scope, element, attrs) {
        function updateData() {
          scope.alias = attrs.alias;
          scope.lists = scope.$eval(attrs.lists);
        };
        $interval(updateData, 1000);
        updateData();
      },
     };
   }]);
