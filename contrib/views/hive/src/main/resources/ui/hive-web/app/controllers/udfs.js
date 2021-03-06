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

import Ember from 'ember';
import FilterableMixin from 'hive/mixins/filterable';
import constants from 'hive/utils/constants';

export default Ember.ArrayController.extend(FilterableMixin, {
  itemController: constants.namingConventions.udf,

  sortAscending: true,
  sortProperties: [],

  init: function () {
    this._super();

    this.set('columns', Ember.ArrayProxy.create({ content: Ember.A([
      Ember.Object.create({
        caption: 'placeholders.udfs.name',
        property: 'name'
      }),
      Ember.Object.create({
        caption: 'placeholders.udfs.className',
        property: 'classname'
      })
    ])}));
  },

  //row buttons
  links: [
      'buttons.edit',
      'buttons.delete'
  ],

  model: function () {
    return this.filter(this.get('udfs'));
  }.property('udfs', 'filters.@each'),

  actions: {
    sort: function (property) {
      //if same column has been selected, toggle flag, else default it to true
      if (this.get('sortProperties').objectAt(0) === property) {
        this.set('sortAscending', !this.get('sortAscending'));
      } else {
        this.set('sortAscending', true);
        this.set('sortProperties', [ property ]);
      }
    },

    add: function () {
      this.store.createRecord(constants.namingConventions.udf);
    }
  }
});
