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
require('utils/configs/modification_handlers/modification_handler');

module.exports = App.ServiceConfigModificationHandler.create({
  serviceId : 'HDFS',

  getConfig : function(allConfigs, configName, configFilename, configServiceName) {
    return allConfigs.findProperty("serviceName", configServiceName).get("configs").find(function(config) {
      return configName == config.get('name') && (configFilename == null || configFilename == config.get('filename'));
    });
  },

  getDependentConfigChanges : function(changedConfig, selectedServices, allConfigs, securityEnabled) {
    var affectedProperties = [];
    var newValue = changedConfig.get("value");
    var rangerPluginEnabledName = "ranger-hdfs-plugin-enabled";
    var affectedPropertyName = changedConfig.get("name");
    if (affectedPropertyName == rangerPluginEnabledName) {
      var configDfsPermissionsEnabled = this.getConfig(allConfigs, 'dfs.permissions.enabled', 'hdfs-site.xml', 'HDFS');

      var rangerPluginEnabled = newValue == "Yes";
      var newDfsPermissionsEnabled = rangerPluginEnabled ? "true" : "true";

      // Add Hive-Ranger configs
      if (configDfsPermissionsEnabled != null && newDfsPermissionsEnabled !== configDfsPermissionsEnabled.get('value')) {
        affectedProperties.push({
          serviceName : "HDFS",
          sourceServiceName : "HDFS",
          propertyName : 'dfs.permissions.enabled',
          propertyDisplayName : 'dfs.permissions.enabled',
          newValue : newDfsPermissionsEnabled,
          curValue : configDfsPermissionsEnabled.get('value'),
          changedPropertyName : rangerPluginEnabledName,
          removed : false,
          filename : 'hdfs-site.xml'
        });
      }
    }
    return affectedProperties;
  }
});