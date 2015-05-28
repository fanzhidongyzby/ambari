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

var cmp = Ember.computed;

App.QueuesController = Ember.ArrayController.extend({
  sortProperties: ['name'],
  sortAscending: true,
  actions:{
    goToQueue:function (queue) {
      this.transitionToRoute('queue',queue)
    },
    askPath:function () {
      this.set('isWaitingPath',true);
    },
    addQ:function (parentPath,name) {
      if (!parentPath || this.get('hasNewQueue')) {
        return;
      }
      name = name || '';
      var newQueue = this.store.createRecord('queue',{
        name:name,
        parentPath: parentPath,
        depth: parentPath.split('.').length,
        isNewQueue:true
      });
      this.set('newQueue',newQueue);
      if (name) {
        this.send('goToQueue',newQueue);
        this.send('createQ',newQueue);
      } else {
        this.send('goToQueue',newQueue);
      }
    },
    createQ:function (record) {
      record.save().then(Em.run.bind(this,this.set,'newQueue',null));
    },
    delQ:function (record) {
      if (record.get('isNew')) {
        this.set('newQueue',null);
      }
      if (!record.get('isNewQueue')) {
        this.set('hasDeletedQueues',true);
      }
      if (record.isCurrent) {
        this.transitionToRoute('queue',record.get('parentPath'));
      }
      this.store.deleteRecord(record);
    },
    saveConfig:function (mark) {
      if (mark == 'restart') {
        this.get('store').markForRestart();
      } else if (mark == 'refresh') {
        this.get('store').markForRefresh();
      }

      var hadDeletedQueues = this.get('hasDeletedQueues'),
          scheduler = this.get('scheduler').save(),
          model = this.get('model').save(),
          all = Em.RSVP.Promise.all([model,scheduler]);

      all.catch(Em.run.bind(this,this.saveError,hadDeletedQueues));

      this.set('hasDeletedQueues',false);
    },
    clearAlert:function () {
      this.set('alertMessage',null);
    }
  },

  alertMessage:null,
  saveError:function (hadDeletedQueues,error) {
    this.set('hasDeletedQueues',hadDeletedQueues);
    var response = JSON.parse(error.responseText);
    this.set('alertMessage',response);
  },

  isOperator:false,
  isNotOperator:cmp.not('isOperator'),

  isWaitingPath:false,
  
  /**
   * check if RM needs refresh
   * @type {bool}
   */
  needRefresh: cmp.and('needRefreshProps','noNeedRestart'),

  /**
   * props for 'needRefresh'
   */
  dirtyQueues: cmp.filterBy('content', 'isDirty', true),
  dirtyScheduler: cmp.bool('scheduler.isDirty'),
  newQueues: cmp.filterBy('content', 'isNewQueue', true),
  hasChanges: cmp.notEmpty('dirtyQueues.[]'),
  hasNewQueues: cmp.notEmpty('newQueues.[]'),

  needRefreshProps: cmp.any('hasChanges', 'hasNewQueues','dirtyScheduler'),
  noNeedRestart: cmp.not('needRestart'),
  
  /**
   * check if RM needs restart 
   * @type {bool}
   */
  needRestart: cmp.any('hasDeletedQueues', 'hasRenamedQueues'),
  
  /**
   * props for 'needRestart'
   */
  hasDeletedQueues:false,
  hasRenamedQueues: cmp.notEmpty('renamedQueues.[]'),
  renamedQueues:function () {
    return this.content.filter(function(queue){
      var attr = queue.changedAttributes();
      return attr.hasOwnProperty('name') && !queue.get('isNewQueue');
    });
  }.property('content.@each.name'),

  /**
   * check if can save configs
   * @type {bool}
   */
  canNotSave: cmp.any('hasOverCapacity', 'hasUncompetedAddings','hasNotValid','isNotOperator'),

  /**
   * props for canNotSave
   */
  notValid:cmp.filterBy('content','isValid',false),
  overCapacityQ:cmp.filterBy('content','overCapacity',true),
  uncompetedAddings:cmp.filterBy('content', 'isNew', true),
  hasNotValid:cmp.notEmpty('notValid.[]'),
  hasOverCapacity:cmp.notEmpty('overCapacityQ.[]'),
  hasUncompetedAddings:cmp.notEmpty('uncompetedAddings.[]'),

  /**
   * check there is some changes for save
   * @type {bool}
   */
  needSave: cmp.any('needRestart', 'needRefresh'),

  newQueue:null,
  hasNewQueue: cmp.bool('newQueue'),
  trackNewQueue:function () {
    var newQueue = this.get('newQueue');
    if (Em.isEmpty(newQueue)){
      return;
    }
    var name = newQueue.get('name');
    var parentPath = newQueue.get('parentPath');

    this.get('newQueue').setProperties({
      name:name.replace(/\s/g, ''),
      path:parentPath+'.'+name,
      id:(parentPath+'.'+name).dasherize()
    });

  }.observes('newQueue.name'),

  configNote:function (arg,val) {
    if (arguments.length > 1) {
      this.set('store.configNote',val);
    }
    return this.get('store.configNote');
  }.property('store.configNote')
});
