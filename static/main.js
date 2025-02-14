(function () {
    'use strict';

    angular.module('WordcountApp', [])
      .controller('WordcountController', ['$scope', '$log', '$http', '$timeout', 
        function($scope, $log, $http, $timeout) {
            $scope.submitButtonText = 'Submit';
            $scope.loading = false;
            $scope.urlPattern = /^(https?|ftp):\/\/[^\s/$.?#].[^\s]*$/i;  // Regex for URL validation

            $scope.getResults = function() {
                var userInput = $scope.url;
                $http.post('/start', {"url": userInput})
                    .then(function(response) {
                        $log.log(response);
                        getWordCount(response.data);
                        $scope.wordcounts = null;
                        $scope.loading = true;
                        $scope.submitButtonText = 'Loading...';
                    })
                    .catch(function(error) {
                        $log.log(error);
                    });
            };
            function getWordCount(jobID) {
              var timeout;
              var poller = function() {
                  $http.get('/results/' + jobID)
                      .then(function(response) {
                          if (response.status === 202) {
                              $log.log('Still processing...');
                          }
                          else if (response.status === 200) {
                              $log.log('Job complete. Data received:', response.data);
                              $scope.wordcounts = response.data;
                              $scope.loading = false;
                              $scope.submitButtonText = "Submit";
                              $timeout.cancel(timeout);
                              return false;
                          }
                          timeout = $timeout(poller, 2000);
                      })
                      .catch(function(error) {
                          $log.error('Error in polling:', error);
                          $timeout.cancel(timeout);
                      });
              };
              poller();
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
