/**
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements. See the NOTICE file distributed with this
 * work for additional information regarding copyright ownership. The ASF
 * licenses this file to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 * http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations under
 * the License.
 */

var App = require('app');

/**
 * @class
 * 
 * This is a view for showing lhotse issue exception count metrics
 * 
 * @extends App.ChartLinearTimeView
 * @extends Ember.Object
 * @extends Ember.View
 */
App.ChartServiceMetricsLhotse_IssuedExceptCount= App.ChartLinearTimeView.extend({
  id: "service-metrics-lhotse-issued-except-count",
  title: Em.I18n.t('services.service.info.metrics.lhotse.issuedExceptCount'),
  yAxisFormatter: App.ChartLinearTimeView.CountFormatter,
  renderer: 'line',
  ajaxIndex: 'service.metrics.lhotse.issued_except_count',

  transformToSeries: function (jsonData) {
    var seriesArray = [];
    if (jsonData && jsonData.metrics && jsonData.metrics.lhotse_db && jsonData.metrics.lhotse_db.metrics_db && jsonData.metrics.lhotse_db.metrics_db.issued_except_count) {
      var seriesData = jsonData.metrics.lhotse_db.metrics_db.issued_except_count;
      if (seriesData) {
        var s = this.transformData(seriesData, Em.I18n.t('services.service.info.metrics.lhotse.issuedExceptCount.displayName.totalNum'));
        seriesArray.push(s);
      }
    }
    return seriesArray;
  }
});

