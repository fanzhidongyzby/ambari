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
var date = require('utils/date');

App.ApplicationController = Em.Controller.extend(App.UserPref, {

  name: 'applicationController',

  isPollerRunning: false,

  clusterName: function () {
    return (App.router.get('clusterController.clusterName') || 'My Cluster');
  }.property('App.router.clusterController.clusterName'),

  /**
   * set ambari server version from installerController or mainController, making sure version shown up all the time
   */
  ambariVersion: function () {
    return (App.router.get('installerController.ambariServerVersion') || App.router.get('mainController.ambariServerVersion') || Em.I18n.t('common.notAvailable'));
  }.property('App.router.installerController.ambariServerVersion', 'App.router.mainController.ambariServerVersion'),

  clusterDisplayName: function () {
    var name = this.get('clusterName');
    return name.length > 13 ? name.substr(0, 10) + "..." : name;
  }.property('clusterName'),

  isClusterDataLoaded: function() {
    return App.router.get('clusterController.isLoaded') && App.router.get('loggedIn');
  }.property('App.router.clusterController.isLoaded','App.router.loggedIn'),

  isExistingClusterDataLoaded: function () {
    return App.router.get('clusterInstallCompleted') && this.get('isClusterDataLoaded');
  }.property('App.router.clusterInstallCompleted', 'isClusterDataLoaded'),

  init: function(){
    this._super();
  },

  startKeepAlivePoller: function() {
    if (!this.get('isPollerRunning')) {
     this.set('isPollerRunning',true);
      App.updater.run(this, 'getStack', 'isPollerRunning', App.sessionKeepAliveInterval);
    }
  },

  getStack: function(callback) {
    App.ajax.send({
      name: 'router.login.clusters',
      sender: this,
      callback: callback
    });
  },

  dataLoading: function () {
    var dfd = $.Deferred();
    var self = this;
    this.getUserPref(this.persistKey()).complete(function () {
      var curPref = self.get('currentPrefObject');
      self.set('currentPrefObject', null);
      dfd.resolve(curPref);
    });
    return dfd.promise();
  },
  persistKey: function (loginName) {
    if (App.get('testMode')) {
      return 'admin_settings_show_bg';
    }
    if (!loginName)
      loginName = App.router.get('loginName');
    return 'admin-settings-show-bg-' + loginName;
  },
  currentPrefObject: null,

  getUserPrefSuccessCallback: function (response, request, data) {
    if (response != null) {
      console.log('Got persist value from server with key ' + data.key + '. Value is: ' + response);
      this.set('currentPrefObject', response);
      return response;
    }
  },
  getUserPrefErrorCallback: function (request, ajaxOptions, error) {
    // this user is first time login
    if (request.status == 404) {
      console.log('Persist did NOT find the key');
      this.set('currentPrefObject', true);
      this.postUserPref(this.persistKey(), true);
      return true;
    }
  },

  goToAdminView: function () {
    App.router.route("adminView");
  },

  showSettingsPopup: function() {
    // Settings only for admins
    if (!App.isAccessible('upgrade_ADMIN')) return;

    var self = this;
    var curValue = null;
    this.dataLoading().done(function (initValue) {
      App.ModalPopup.show({
        header: Em.I18n.t('common.userSettings'),
        bodyClass: Em.View.extend({
          templateName: require('templates/common/settings'),
          isNotShowBgChecked: !initValue,
          updateValue: function () {
            curValue = !this.get('isNotShowBgChecked');
          }.observes('isNotShowBgChecked')
        }),
        primary: Em.I18n.t('common.save'),
        onPrimary: function() {
          if (curValue == null) {
            curValue = initValue;
          }
          var key = self.persistKey();
          if (!App.get('testMode')) {
            self.postUserPref(key, curValue);
          }
          this.hide();
        }
      })
    });
  },

  showAboutPopup: function() {

    var self = this;
    App.ModalPopup.show({
      header: Em.I18n.t('common.aboutAmbari'),
      secondary: false,
      bodyClass: Em.View.extend({
        templateName: require('templates/common/about'),
        ambariVersion: this.get('ambariVersion')
      })
    });    
  },
  
  showLicense: function() {

    var self = this;
	var url = App.get('apiPrefix') + '/license/';

	$.getJSON(url, function(json){
		if (typeof(json.key) == 'undefined') {
			App.ModalPopup.show({
			  header: '许可信息',
			  bodyClass: Em.View.extend({
				templateName: require('templates/common/edit_license')
			  }),
			  primary : Em.I18n.t('common.save'),
			  onPrimary: function() {
				var data = $('#licenseId').val();
				$.post(url, data, function(){
				});
			  }
			}); 
		
		} else {
			// "customerName":"jerryjzhang","clusterLimit":10,"expirationDate":1467216000000,"key":"NJSXE4TZ-NJ5GQYLO-M4WTCMBN-GIYDCNRP-GA3C6MZQ"}
			App.ModalPopup.show({
			  header: '许可信息',
			  bodyClass: Em.View.extend({
				templateName: require('templates/common/license'),
				expirationDate: date.dateFormat(json.expirationDate),
				customerName : json.customerName,
				clusterLimit : json.clusterLimit,
				key : json.key
			  }),
			  primary : Em.I18n.t('common.save'),
			  onPrimary : function() {
				var _this = this;
					if ($('#modLicenseVal').length > 0) {
						var data = $('#modLicenseVal').val();
						$.post(url, data, function(){
							$('#editInput').html(data);
							_this.hide();
						}).error(function(){
							alert('输入许可证不对');
						});
					} else {
						this.hide();
					}
				}
			}); 
			window.setTimeout(function(){
				$('#modLicenseBtn').click(function(){
					if ($(this).text() == '修改') {
						var val = $('#editInput').text();
						$('#editInput').html('<input type="text" style="wdith:200px;" id="modLicenseVal" value="'+val+'" />');
						//$(this).html('保存');
					} else {
						var data = $('#modLicenseVal').val();
						$.post(url, data, function(){
							$(this).html('修改');
							$('#editInput').html(data);
						});
					}
				});
			}, 500);
			
		}
	}).error(function(){
		App.ModalPopup.show({
		  header: '许可信息',
		  bodyClass: Em.View.extend({
			templateName: require('templates/common/edit_license')
		  }),
		  primary : Em.I18n.t('common.save'),
		  onPrimary: function() {
			var _this = this;
			var data = $('#licenseId').val();
			$.post(url, data, function(){
				_this.hide();
			}).error(function(){
				alert('输入许可证不对');
			});
		  }
		}); 
	});
  }

});