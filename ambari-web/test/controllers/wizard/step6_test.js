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

var Ember = require('ember');
var App = require('app');
require('utils/helper');
require('controllers/wizard/step6_controller');
var controller,
  services = [
    Em.Object.create({
      serviceName: 'YARN',
      isSelected: true
    }),
    Em.Object.create({
      serviceName: 'HBASE',
      isSelected: true
    }),
    Em.Object.create({
      serviceName: 'HDFS',
      isSelected: true
    }),
    Em.Object.create({
      serviceName: 'STORM',
      isSelected: true
    }),
    Em.Object.create({
      serviceName: 'FLUME',
      isSelected: true
    })
  ];
describe('App.WizardStep6Controller', function () {

  beforeEach(function () {
    controller = App.WizardStep6Controller.create();
    controller.set('content', Em.Object.create({
      hosts: {},
      masterComponentHosts: {},
      services: services
    }));

    var h = {}, m = [];
    Em.A(['host0', 'host1', 'host2', 'host3']).forEach(function (hostName) {
      var obj = Em.Object.create({
        name: hostName,
        hostName: hostName,
        bootStatus: 'REGISTERED'
      });
      h[hostName] = obj;
      m.push(obj);
    });

    controller.set('content.hosts', h);
    controller.set('content.masterComponentHosts', m);
    controller.set('isMasters', false);

  });

  describe('#isAddHostWizard', function () {
    it('true if content.controllerName is addHostController', function () {
      controller.set('content.controllerName', 'addHostController');
      expect(controller.get('isAddHostWizard')).to.equal(true);
    });
    it('false if content.controllerName is not addHostController', function () {
      controller.set('content.controllerName', 'mainController');
      expect(controller.get('isAddHostWizard')).to.equal(false);
    });
  });

  describe('#isInstallerWizard', function () {
    it('true if content.controllerName is addHostController', function () {
      controller.set('content.controllerName', 'installerController');
      expect(controller.get('isInstallerWizard')).to.equal(true);
    });
    it('false if content.controllerName is not addHostController', function () {
      controller.set('content.controllerName', 'mainController');
      expect(controller.get('isInstallerWizard')).to.equal(false);
    });
  });

  describe('#isAddServiceWizard', function () {
    it('true if content.controllerName is addServiceController', function () {
      controller.set('content.controllerName', 'addServiceController');
      expect(controller.get('isAddServiceWizard')).to.equal(true);
    });
    it('false if content.controllerName is not addServiceController', function () {
      controller.set('content.controllerName', 'mainController');
      expect(controller.get('isAddServiceWizard')).to.equal(false);
    });
  });

  describe('#clearStep', function () {
    beforeEach(function () {
      sinon.stub(controller, 'clearError', Em.K);
    });
    afterEach(function () {
      controller.clearError.restore();
    });
    it('should call clearError', function () {
      controller.clearStep();
      expect(controller.clearError.calledOnce).to.equal(true);
    });
    it('should clear hosts', function () {
      controller.set('hosts', [
        {},
        {}
      ]);
      controller.clearStep();
      expect(controller.get('hosts')).to.eql([]);
    });
    it('should clear headers', function () {
      controller.set('headers', [
        {},
        {}
      ]);
      controller.clearStep();
      expect(controller.get('headers')).to.eql([]);
    });
    it('should set isLoaded to false', function () {
      controller.set('isLoaded', true);
      controller.clearStep();
      expect(controller.get('isLoaded')).to.equal(false);
    });
  });

  describe('#checkCallback', function () {
    beforeEach(function () {
      sinon.stub(controller, 'clearError', Em.K);
    });
    afterEach(function () {
      controller.clearError.restore();
    });
    it('should call clearError', function () {
      controller.checkCallback('');
      expect(controller.clearError.calledOnce).to.equal(true);
    });
    Em.A([
        {
          m: 'all checked, isInstalled false',
          headers: Em.A([
            Em.Object.create({name: 'c1'})
          ]),
          hosts: Em.A([
            Em.Object.create({
              checkboxes: Em.A([
                Em.Object.create({
                  component: 'c1',
                  isInstalled: false,
                  checked: true
                })
              ])
            })
          ]),
          component: 'c1',
          e: {
            allChecked: true,
            noChecked: false
          }
        },
        {
          m: 'all checked, isInstalled true',
          headers: Em.A([
            Em.Object.create({name: 'c1'})
          ]),
          hosts: Em.A([
            Em.Object.create({
              checkboxes: Em.A([
                Em.Object.create({
                  component: 'c1',
                  isInstalled: true,
                  checked: true
                })
              ])
            })
          ]),
          component: 'c1',
          e: {
            allChecked: true,
            noChecked: true
          }
        },
        {
          m: 'no one checked',
          headers: Em.A([
            Em.Object.create({name: 'c1'})
          ]),
          hosts: Em.A([
            Em.Object.create({
              checkboxes: Em.A([
                Em.Object.create({
                  component: 'c1',
                  isInstalled: false,
                  checked: false
                })
              ])
            })
          ]),
          component: 'c1',
          e: {
            allChecked: false,
            noChecked: true
          }
        },
        {
          m: 'some checked',
          headers: Em.A([
            Em.Object.create({name: 'c1'})
          ]),
          hosts: Em.A([
            Em.Object.create({
              checkboxes: Em.A([
                Em.Object.create({
                  component: 'c1',
                  isInstalled: false,
                  checked: true
                }),
                Em.Object.create({
                  component: 'c1',
                  isInstalled: false,
                  checked: false
                })
              ])
            })
          ]),
          component: 'c1',
          e: {
            allChecked: false,
            noChecked: false
          }
        },
        {
          m: 'some checked, some isInstalled true',
          headers: Em.A([
            Em.Object.create({name: 'c1'})
          ]),
          hosts: Em.A([
            Em.Object.create({
              checkboxes: Em.A([
                Em.Object.create({
                  component: 'c1',
                  isInstalled: true,
                  checked: true
                }),
                Em.Object.create({
                  component: 'c1',
                  isInstalled: true,
                  checked: true
                })
              ])
            })
          ]),
          component: 'c1',
          e: {
            allChecked: true,
            noChecked: true
          }
        },
        {
          m: 'some checked, some isInstalled true (2)',
          headers: Em.A([
            Em.Object.create({name: 'c1'})
          ]),
          hosts: Em.A([
            Em.Object.create({
              checkboxes: Em.A([
                Em.Object.create({
                  component: 'c1',
                  isInstalled: false,
                  checked: false
                }),
                Em.Object.create({
                  component: 'c1',
                  isInstalled: true,
                  checked: true
                })
              ])
            })
          ]),
          component: 'c1',
          e: {
            allChecked: false,
            noChecked: true
          }
        }
      ]).forEach(function (test) {
        it(test.m, function () {
          controller.clearStep();
          controller.set('headers', test.headers);
          controller.set('hosts', test.hosts);
          controller.checkCallback(test.component);
          var header = controller.get('headers').findProperty('name', test.component);
          expect(header.get('allChecked')).to.equal(test.e.allChecked);
          expect(header.get('noChecked')).to.equal(test.e.noChecked);
        });
      });
  });

  describe('#getHostNames', function () {
    var tests = Em.A([
      {
        hosts: {
          h1: {bootStatus: 'REGISTERED', name: 'h1'},
          h2: {bootStatus: 'REGISTERED', name: 'h2'},
          h3: {bootStatus: 'REGISTERED', name: 'h3'}
        },
        m: 'All REGISTERED',
        e: ['h1', 'h2', 'h3']
      },
      {
        hosts: {
          h1: {bootStatus: 'REGISTERED', name: 'h1'},
          h2: {bootStatus: 'FAILED', name: 'h2'},
          h3: {bootStatus: 'REGISTERED', name: 'h3'}
        },
        m: 'Some REGISTERED',
        e: ['h1', 'h3']
      },
      {
        hosts: {
          h1: {bootStatus: 'FAILED', name: 'h1'},
          h2: {bootStatus: 'FAILED', name: 'h2'},
          h3: {bootStatus: 'FAILED', name: 'h3'}
        },
        m: 'No one REGISTERED',
        e: []
      },
      {
        hosts: {},
        m: 'Empty hosts',
        e: []
      }
    ]);
    tests.forEach(function (test) {
      it(test.m, function () {
        controller.set('content.hosts', test.hosts);
        var r = controller.getHostNames();
        expect(r).to.eql(test.e);
      });
    });
  });

  describe('#getMasterComponentsForHost', function () {
    var tests = Em.A([
      {
        masterComponentHosts: Em.A([
          {hostName: 'h1', component: 'c1'}
        ]),
        hostName: 'h1',
        m: 'host exists',
        e: ['c1']
      },
      {
        masterComponentHosts: Em.A([
          {hostName: 'h1', component: 'c1'}
        ]),
        hostName: 'h2',
        m: 'host donesn\'t exists',
        e: []
      }
    ]);
    tests.forEach(function (test) {
      it(test.m, function () {
        controller.set('content.masterComponentHosts', test.masterComponentHosts);
        var r = controller.getMasterComponentsForHost(test.hostName);
        expect(r).to.eql(test.e);
      });
    });
  });

  describe('#selectMasterComponents', function () {
    var tests = Em.A([
      {
        masterComponentHosts: Em.A([
          {
            hostName: 'h1',
            component: 'c1'
          }
        ]),
        hostsObj: [
          Em.Object.create({
            hostName: 'h1',
            checkboxes: [
              Em.Object.create({
                component: 'c1',
                checked: false
              })
            ]
          })
        ],
        e: true,
        m: 'host and component exist'
      },
      {
        masterComponentHosts: Em.A([
          {
            hostName: 'h1',
            component: 'c2'
          }
        ]),
        hostsObj: [
          Em.Object.create({
            hostName: 'h1',
            checkboxes: [
              Em.Object.create({
                component: 'c1',
                checked: false
              })
            ]
          })
        ],
        e: false,
        m: 'host exists'
      },
      {
        masterComponentHosts: Em.A([
          {
            hostName: 'h2',
            component: 'c2'
          }
        ]),
        hostsObj: [
          Em.Object.create({
            hostName: 'h1',
            checkboxes: [
              Em.Object.create({
                component: 'c1',
                checked: false
              })
            ]
          })
        ],
        e: false,
        m: 'host and component don\'t exist'
      }
    ]);
    tests.forEach(function (test) {
      it(test.m, function () {
        controller.set('content.masterComponentHosts', test.masterComponentHosts);
        var r = controller.selectMasterComponents(test.hostsObj);
        expect(r.findProperty('hostName', 'h1').get('checkboxes').findProperty('component', 'c1').get('checked')).to.equal(test.e);
      });
    });
  });

  describe('#getCurrentMastersBlueprint', function () {
    var tests = Em.A([
      {
        masterComponentHosts: Em.A([
          {hostName: 'h1', component: 'c1'}
        ]),
        hosts: {'h1': {}},
        m: 'one host and one component',
        e:{
          blueprint: {
            host_groups: [
              {
                name: 'host-group-1',
                components: [
                  { name: 'c1' }
                ]
              }
            ]
          },
          blueprint_cluster_binding: {
            host_groups: [
              {
                name: 'host-group-1',
                hosts: [
                  { fqdn: 'h1' }
                ]
              }
            ]
          }
        }
      },
      {
        masterComponentHosts: Em.A([
          {hostName: 'h1', component: 'c1'},
          {hostName: 'h2', component: 'c2'},
          {hostName: 'h2', component: 'c3'}
        ]),
        hosts: {'h1': {}, 'h2': {}, 'h3': {}},
        m: 'multiple hosts and multiple components',
        e: {
          blueprint: {
            host_groups: [
              {
                name: 'host-group-1',
                components: [
                  { name: 'c1' }
                ]
              },
              {
                name: 'host-group-2',
                components: [
                  { name: 'c2' },
                  { name: 'c3' }
                ]
              },
              {
                name: 'host-group-3',
                components: []
              }
            ]
          },
          blueprint_cluster_binding: {
            host_groups: [
              {
                name: 'host-group-1',
                hosts: [
                  { fqdn: 'h1' }
                ]
              },
              {
                name: 'host-group-2',
                hosts: [
                  { fqdn: 'h2' }
                ]
              },
              {
                name: 'host-group-3',
                hosts: [
                  { fqdn: 'h3' }
                ]
              }
            ]
          }
        }
      }
    ]);
    tests.forEach(function (test) {
      it(test.m, function () {
        controller.set('content.masterComponentHosts', test.masterComponentHosts);
        controller.set('content.hosts', test.hosts);
        var r = controller.getCurrentMastersBlueprint();
        expect(r).to.eql(test.e);
      });
    });
  });

  describe('#callServerSideValidation', function () {

    var cases = [
        {
          controllerName: 'installerController',
          hosts: [
            {
              hostName: 'h0'
            },
            {
              hostName: 'h1'
            }
          ],
          expected: [
            ['c0', 'c6'],
            ['c1', 'c3', 'c8']
          ]
        },
        {
          controllerName: 'addServiceController',
          hosts: [
            {
              hostName: 'h0'
            },
            {
              hostName: 'h1'
            }
          ],
          expected: [
            ['c0', 'c6'],
            ['c1', 'c3', 'c8']
          ]
        },
        {
          controllerName: 'addHostController',
          hosts: [
            {
              hostName: 'h0'
            }
          ],
          expected: [
            ['c0', 'c2', 'c5', 'c6'],
            ['c1', 'c2', 'c3', 'c5', 'c8']
          ]
        }
      ],
      expectedHostGroups = [
        {
          name: 'host-group-1',
          fqdn: 'h0'
        },
        {
          name: 'host-group-2',
          fqdn: 'h1'
        }
      ];

    beforeEach(function () {
      controller.get('content').setProperties({
        recommendations: {
          blueprint: {
            host_groups: [
              {
                components: [
                  {
                    name: 'c6'
                  }
                ],
                name: 'host-group-1'
              },
              {
                components: [
                  {
                    name: 'c8'
                  }
                ],
                name: 'host-group-2'
              }
            ]
          },
          blueprint_cluster_binding: {
            host_groups: [
              {
                hosts: [
                  {
                    fqdn: 'h0'
                  }
                ],
                name: 'host-group-1'
              },
              {
                hosts: [
                  {
                    fqdn: 'h1'
                  }
                ],
                name: 'host-group-2'
              }]
          }
        },
        clients: [
          {
            component_name: 'c3'
          }
        ]
      });
      sinon.stub(App.StackService, 'find', function () {
        return [
          Em.Object.create({
            serviceName: 's0',
            isSelected: true
          }),
          Em.Object.create({
            serviceName: 's1',
            isInstalled: true,
            isSelected: true
          })
        ];
      });
      sinon.stub(App.StackServiceComponent, 'find', function () {
        return [
          Em.Object.create({
            componentName: 'c0',
            isSlave: true
          }),
          Em.Object.create({
            componentName: 'c1',
            isSlave: true,
            isShownOnInstallerSlaveClientPage: true
          }),
          Em.Object.create({
            componentName: 'c2',
            isSlave: true,
            isShownOnInstallerSlaveClientPage: false
          }),
          Em.Object.create({
            componentName: 'c3',
            isClient: true
          }),
          Em.Object.create({
            componentName: 'c4',
            isClient: true,
            isRequiredOnAllHosts: false
          }),
          Em.Object.create({
            componentName: 'c5',
            isClient: true,
            isRequiredOnAllHosts: true
          }),
          Em.Object.create({
            componentName: 'c6',
            isMaster: true,
            isShownOnInstallerAssignMasterPage: true
          }),
          Em.Object.create({
            componentName: 'c7',
            isMaster: true,
            isShownOnInstallerAssignMasterPage: false
          }),
          Em.Object.create({
            componentName: 'c8',
            isMaster: true,
            isShownOnAddServiceAssignMasterPage: true
          }),
          Em.Object.create({
            componentName: 'c9',
            isMaster: true,
            isShownOnAddServiceAssignMasterPage: false
          })
        ];
      });
      sinon.stub(controller, 'getCurrentBlueprint', function () {
        return {
          blueprint: {
            host_groups: [
              {
                components: [
                  {
                    name: 'c0'
                  }
                ],
                name: 'host-group-1'
              },
              {
                components: [
                  {
                    name: 'c1'
                  },
                  {
                    name: 'c3'
                  }
                ],
                name: 'host-group-2'
              }
            ]
          },
          blueprint_cluster_binding: {
            host_groups: [
              {
                hosts: [
                  {
                    fqdn: 'h0'
                  }
                ],
                name: 'host-group-1'
              },
              {
                hosts: [
                  {
                    fqdn: 'h1'
                  }
                ],
                name: 'host-group-2'
              }]
          }
        };
      });
      sinon.stub(controller, 'getCurrentMastersBlueprint', function () {
        return {
          blueprint: {
            host_groups: [
              {
                components: [
                  {
                    name: 'c6'
                  }
                ],
                name: 'host-group-1'
              },
              {
                components: [
                  {
                    name: 'c8'
                  }
                ],
                name: 'host-group-2'
              }
            ]
          },
          blueprint_cluster_binding: {
            host_groups: [
              {
                hosts: [
                  {
                    fqdn: 'h0'
                  }
                ],
                name: 'host-group-1'
              },
              {
                hosts: [
                  {
                    fqdn: 'h1'
                  }
                ],
                name: 'host-group-2'
              }]
          }
        };
      });
      sinon.stub(App, 'get').withArgs('components.clients').returns(['c3', 'c4']);
      sinon.stub(controller, 'getCurrentMasterSlaveBlueprint', function () {
        return {
          blueprint: {
            host_groups: [
              {
                components: [
                  {
                    name: 'c6'
                  }
                ],
                name: 'host-group-1'
              },
              {
                components: [
                  {
                    name: 'c8'
                  }
                ],
                name: 'host-group-2'
              }
            ]
          },
          blueprint_cluster_binding: {
            host_groups: [
              {
                hosts: [
                  {
                    fqdn: 'h0'
                  }
                ],
                name: 'host-group-1'
              },
              {
                hosts: [
                  {
                    fqdn: 'h1'
                  }
                ],
                name: 'host-group-2'
              }]
          }
        };
      });
      sinon.stub(App.Host, 'find', function () {
        return [
          {
            hostName: 'h1'
          }
        ];
      });
      sinon.stub(App.ajax, 'send', function () {
        return {
          then: Em.K
        };
      });
    });

    afterEach(function () {
      App.StackService.find.restore();
      App.StackServiceComponent.find.restore();
      controller.getCurrentBlueprint.restore();
      controller.getCurrentMastersBlueprint.restore();
      App.get.restore();
      controller.getCurrentMasterSlaveBlueprint.restore();
      App.Host.find.restore();
      App.ajax.send.restore();
    });

    cases.forEach(function (item) {
      it(item.controllerName, function () {
        controller.set('hosts', item.hosts);
        controller.set('content.controllerName', item.controllerName);
        controller.callServerSideValidation();
        expect(controller.get('content.recommendationsHostGroups.blueprint.host_groups.length')).to.equal(expectedHostGroups.length);
        expect(controller.get('content.recommendationsHostGroups.blueprint_cluster_binding.host_groups.length')).to.equal(expectedHostGroups.length);
        controller.get('content.recommendationsHostGroups.blueprint.host_groups').forEach(function (group, index) {
          expect(group.components.mapProperty('name').sort()).to.eql(item.expected[index]);
        });
        expectedHostGroups.forEach(function (group) {
          var bpGroup = controller.get('content.recommendationsHostGroups.blueprint_cluster_binding.host_groups').findProperty('name', group.name);
          expect(bpGroup.hosts).to.have.length(1);
          expect(bpGroup.hosts[0].fqdn).to.equal(group.fqdn);
        });
      });
    });

  });

});
