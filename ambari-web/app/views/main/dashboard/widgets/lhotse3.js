/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

var App = require('app');

App.Lhotse3View = App.DashboardWidgetView.extend({
  title: Em.I18n.t('services.service.info.metrics.lhotse.baseRequestCount'),
  id: '32',
  templateName: require('templates/main/dashboard/widgets/cluster_metrics'),
  content: App.ChartLinearTimeView.extend({
	noTitleUnderGraph: true,
	inWidget: true,
	id: "cluster-metrics-Lhotse3",

	ajaxIndex: 'service.metrics.lhotse.base_request_count',

	isTimePagingDisable: true,
	title: Em.I18n.t('services.service.info.metrics.lhotse.baseRequestCount'),
	yAxisFormatter: App.ChartLinearTimeView.CountFormatter,
	renderer: 'line',
	
  transformToSeries: function (jsonData) {
    var seriesArray = [];
    if (jsonData && jsonData.metrics && jsonData.metrics.lhotse_db && jsonData.metrics.lhotse_db.metrics_db && jsonData.metrics.lhotse_db.metrics_db.base_request_count) {
      for ( var name in jsonData.metrics.lhotse_db.metrics_db.base_request_count) {
        var seriesData = jsonData.metrics.lhotse_db.metrics_db.base_request_count[name];
        var displayName = App.lhotse_task_type[name];
        if (seriesData) {
          var s = this.transformData(seriesData, displayName);
          seriesArray.push(s);
        }
      }
    }
    return seriesArray;
  }
	
  })
});
