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
require('views/common/chart/pie');
require('views/common/configs/services_config');

describe('App.ServiceConfigView', function () {

  var controller = App.WizardStep7Controller.create({
    selectedServiceObserver: Em.K,
    switchConfigGroupConfigs: Em.K
  });

  var view = App.ServiceConfigView.create({
    controller: controller
  });

  var testCases = [
    {
      title: 'selectedConfigGroup is null',
      result: {
        'category1': false,
        'category2': true,
        'category3': false
      },
      selectedConfigGroup: null,
      selectedService: {
        serviceName: 'TEST',
        configCategories: [
          App.ServiceConfigCategory.create({ name: 'category1', canAddProperty: false}),
          App.ServiceConfigCategory.create({ name: 'category2', siteFileName: 'xml', canAddProperty: true}),
          App.ServiceConfigCategory.create({ name: 'category3', siteFileName: 'xml', canAddProperty: false})
        ]
      }
    },
    {
      title: 'selectedConfigGroup is default group',
      result: {
        'category1': true,
        'category2': true,
        'category3': false
      },
      selectedConfigGroup: {isDefault: true},
      selectedService: {
        serviceName: 'TEST',
        configCategories: [
          App.ServiceConfigCategory.create({ name: 'category1', canAddProperty: true}),
          App.ServiceConfigCategory.create({ name: 'category2', siteFileName: 'xml', canAddProperty: true}),
          App.ServiceConfigCategory.create({ name: 'category3', siteFileName: 'xml', canAddProperty: false})
        ]
      }
    }
  ];

  describe('#checkCanEdit', function () {
    testCases.forEach(function (test) {
      it(test.title, function () {
        controller.set('selectedService', test.selectedService);
        controller.set('selectedConfigGroup', test.selectedConfigGroup);
        view.checkCanEdit();
        controller.get('selectedService.configCategories').forEach(function (category) {
          expect(category.get('canAddProperty')).to.equal(test.result[category.get('name')]);
        });
      });
    });
  });

});
