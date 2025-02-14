(function () {
    'use strict';
  
    angular.module('WordcountApp', [])
      .controller('WordcountController', ['$scope', '$log', '$http', '$timeout', 
        function($scope, $log, $http, $timeout) {
            $scope.submitButtonText = 'Submit';
            $scope.loading = false;
            
          $scope.getResults = function() {
            $log.log("test");
            var userInput = $scope.url;
            $http.post('/start', {"url": userInput})
                .success(function(results) {
                    $log.log(results);
                    getWordCount(results);
                    $scope.wordcounts = null;
                    $scope.loading = true;
                    $scope.submitButtonText = 'Loading...';
                }).
                error(function(error) {
                    $log.log(error);
                });
          };
  
          function getWordCount(jobID) {
            var timeout = "";
            var poller = function() {
                // fire another request
                $http.get('/results/'+jobID)
                  .success(function(data, status, headers, config) {
                    if(status === 202) {
                      $log.log(data, status);
                    } else if (status === 200){
                      $log.log(data);
                      $scope.loading = false;
                      $scope.submitButtonText = "Submit";
                      $scope.wordcounts = data;
                      $timeout.cancel(timeout);
                      return false;
                    }
                    // continue to call the poller() function every 2 seconds
                    // until the timeout is cancelled
                    timeout = $timeout(poller, 2000);
                  });
              };  
            poller(); // Start polling
          }
        }
      ])
      .directive('wordCountChart', ['$parse', function ($parse) {
        return {
            restrict: 'E',
            replace: true,
            template: '<div id="chart"></div>',
            link: function (scope) {
                scope.$watch('wordcounts', function() {
                  d3.select('#chart').selectAll('*').remove();
                  var data = scope.wordcounts;
                  for (var word in data) {
                    var key = data[word][0];
                    var value = data[word][1];
                    d3.select('#chart')
                      .append('div')
                      .selectAll('div')
                      .data(word)
                      .enter()
                      .append('div')
                      .style('width', function() {
                        return (value * 3) + 'px';
                      })
                      .text(function(d){
                        return key;
                      });
                  }
                }, true);
              }
        };
        }]);
  }());
  
  