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


// load all views here

require('views/application');
require('views/common/ajax_default_error_popup_body');
require('views/common/chart');
require('views/common/chart/pie');
require('views/common/chart/linear');
require('views/common/chart/linear_time');
require('views/common/modal_popup');
require('views/common/modal_popups/alert_popup');
require('views/common/modal_popups/confirmation_feedback_popup');
require('views/common/modal_popups/confirmation_popup');
require('views/common/modal_popups/prompt_popup');
require('views/common/modal_popups/reload_popup');
require('views/common/modal_popups/cluster_check_popup');
require('views/common/modal_popups/invalid_KDC_popup');
require('views/common/editable_list');
require('views/common/rolling_restart_view');
require('views/common/select_custom_date_view');
require('views/common/metric');
require('views/common/time_range');
require('views/common/form/field');
require('views/common/quick_view_link_view');
require('views/common/configs/services_config');
require('views/common/configs/service_config_container_view');
require('views/common/configs/service_configs_by_category_view');
require('views/common/configs/service_config_view');
require('views/common/configs/service_config_tab_view');
require('views/common/configs/overriddenProperty_view');
require('views/common/configs/compare_property_view');
require('views/common/configs/config_history_flow');
require('views/common/configs/custom_category_views/notification_configs_view');
require('views/common/filter_combobox');
require('views/common/filter_combo_cleanable');
require('views/common/table_view');
require('views/common/progress_bar_view');
require('views/common/controls_view');
require('views/login');
require('views/main');
require('views/main/menu');
require('views/main/alert_definitions_view');
require('views/main/alerts/definition_details_view');
require('views/main/alerts/alert_definitions_actions_view');
require('views/main/alerts/definition_configs_view');
require('views/main/alerts/manage_alert_groups/select_definitions_popup_body_view');
require('views/main/alerts/add_alert_definition/add_alert_definition_view');
require('views/main/alerts/add_alert_definition/step1_view');
require('views/main/alerts/add_alert_definition/step2_view');
require('views/main/alerts/add_alert_definition/step3_view');
require('views/main/alerts');
require('views/main/alerts/manage_alert_groups_view');
require('views/main/alerts/manage_alert_notifications_view');
require('views/main/charts');
require('views/main/views/details');
require('views/main/host');
require('views/main/host/hosts_table_menu_view');
require('views/main/host/details');
require('views/main/host/details/host_component_view');
require('views/main/host/details/host_component_views/datanode_view');
require('views/main/host/details/host_component_views/nodemanager_view');
require('views/main/host/details/host_component_views/regionserver_view');
require('views/main/host/details/host_component_views/tasktracker_view');
require('views/main/host/menu');
require('views/main/host/summary');
require('views/main/host/configs');
require('views/main/host/configs_service');
require('views/main/host/configs_service_menu');
require('views/main/host/metrics');
require('views/main/host/stack_versions_view');
require('views/main/host/add_view');
require('views/main/host/host_alerts_view');
require('views/main/host/metrics/cpu');
require('views/main/host/metrics/disk');
require('views/main/host/metrics/load');
require('views/main/host/metrics/memory');
require('views/main/host/metrics/network');
require('views/main/host/metrics/processes');
require('views/main/host/addHost/step4_view');
require('views/main/admin');
require('views/main/admin/highAvailability/nameNode/wizard_view');
require('views/main/admin/highAvailability/progress_view');
require('views/main/admin/highAvailability/nameNode/rollback_view');
require('views/main/admin/highAvailability/nameNode/step1_view');
require('views/main/admin/highAvailability/nameNode/step2_view');
require('views/main/admin/highAvailability/nameNode/step3_view');
require('views/main/admin/highAvailability/nameNode/step4_view');
require('views/main/admin/highAvailability/nameNode/step5_view');
require('views/main/admin/highAvailability/nameNode/step6_view');
require('views/main/admin/highAvailability/nameNode/step7_view');
require('views/main/admin/highAvailability/nameNode/step8_view');
require('views/main/admin/highAvailability/nameNode/step9_view');
require('views/main/admin/highAvailability/nameNode/rollbackHA/step1_view');
require('views/main/admin/highAvailability/nameNode/rollbackHA/step2_view');
require('views/main/admin/highAvailability/nameNode/rollbackHA/step3_view');
require('views/main/admin/highAvailability/nameNode/rollbackHA/rollback_wizard_view');
require('views/main/admin/highAvailability/resourceManager/wizard_view');
require('views/main/admin/highAvailability/resourceManager/step1_view');
require('views/main/admin/highAvailability/resourceManager/step2_view');
require('views/main/admin/highAvailability/resourceManager/step3_view');
require('views/main/admin/highAvailability/resourceManager/step4_view');
require('views/main/admin/serviceAccounts_view');
require('views/main/admin/stack_upgrade/upgrade_wizard_view');
require('views/main/admin/stack_upgrade/upgrade_version_box_view');
require('views/main/admin/stack_upgrade/upgrade_group_view');
require('views/main/admin/stack_upgrade/upgrade_task_view');
require('views/main/admin/stack_upgrade/services_view');
require('views/main/admin/stack_upgrade/versions_view');
require('views/main/admin/stack_upgrade/menu_view');
require('views/main/admin/stack_and_upgrade_view');
require('views/main/admin/advanced');
require('views/main/admin/advanced/password');
require('views/main/admin/audit');
require('views/main/admin/authentication');

require('views/main/admin/kerberos');
require('views/main/admin/kerberos/disable_view');
require('views/main/admin/kerberos/wizard_view');
require('views/main/admin/kerberos/progress_view');
require('views/main/admin/kerberos/step1_view');
require('views/main/admin/kerberos/step2_view');
require('views/main/admin/kerberos/step3_view');
require('views/main/admin/kerberos/step4_view');
require('views/main/admin/kerberos/step5_view');
require('views/main/admin/kerberos/step6_view');
require('views/main/admin/kerberos/step7_view');

require('views/main/admin/security');
require('views/main/admin/security/disable');
require('views/main/admin/security/add/menu');
require('views/main/admin/security/add/step1');
require('views/main/admin/security/add/step2');
require('views/main/admin/security/add/step3');
require('views/main/admin/security/add/step4');

require('views/main/dashboard');
require('views/main/dashboard/cluster_metrics/cpu');
require('views/main/dashboard/cluster_metrics/load');
require('views/main/dashboard/cluster_metrics/memory');
require('views/main/dashboard/cluster_metrics/network');

require('views/main/dashboard/widget');
require('views/main/dashboard/widgets');
require('views/main/dashboard/widgets/text_widget');
require('views/main/dashboard/widgets/uptime_text_widget');
require('views/main/dashboard/widgets/links_widget');
require('views/main/dashboard/widgets/pie_chart_widget');
require('views/main/dashboard/widgets/cluster_metrics_widget');
require('views/main/dashboard/widgets/namenode_heap');
require('views/main/dashboard/widgets/namenode_cpu');
require('views/main/dashboard/widgets/hdfs_capacity');
require('views/main/dashboard/widgets/datanode_live');
require('views/main/dashboard/widgets/namenode_rpc');
require('views/main/dashboard/widgets/metrics_memory');
require('views/main/dashboard/widgets/metrics_network');
require('views/main/dashboard/widgets/metrics_cpu');
require('views/main/dashboard/widgets/metrics_load');
require('views/main/dashboard/widgets/namenode_uptime');
require('views/main/dashboard/widgets/hdfs_links');
require('views/main/dashboard/widgets/yarn_links');
require('views/main/dashboard/widgets/hbase_links');
require('views/main/dashboard/widgets/hbase_master_heap');
require('views/main/dashboard/widgets/hbase_average_load');
require('views/main/dashboard/widgets/hbase_regions_in_transition');
require('views/main/dashboard/widgets/hbase_master_uptime');
require('views/main/dashboard/widgets/resource_manager_heap');
require('views/main/dashboard/widgets/resource_manager_uptime');
require('views/main/dashboard/widgets/node_managers_live');
require('views/main/dashboard/widgets/yarn_memory');
require('views/main/dashboard/widgets/supervisor_live');
require('views/main/dashboard/widgets/flume_agent_live');
require('views/main/dashboard/widgets/lhotse1');
require('views/main/dashboard/widgets/lhotse2');
require('views/main/dashboard/widgets/lhotse3');
require('views/main/dashboard/config_history_view');


require('views/main/service');
require('views/main/service/service');
require('views/main/service/services/hdfs');
require('views/main/service/services/yarn');
require('views/main/service/services/mapreduce2');
require('views/main/service/services/hbase');
require('views/main/service/services/hive');
require('views/main/service/services/zookeeper');
require('views/main/service/services/oozie');
require('views/main/service/services/flume');
require('views/main/service/services/storm');
require('views/main/service/services/ranger');
require('views/main/service/all_services_actions');
require('views/main/service/menu');
require('views/main/service/item');
require('views/main/service/reconfigure');
require('views/main/service/info/components_list_view');
require('views/main/service/info/menu');
require('views/main/service/info/summary');
require('views/main/service/info/configs');
require('views/main/service/info/metric_graphs_view');
require('views/main/service/info/metrics/hdfs/jvm_threads');
require('views/main/service/info/metrics/hdfs/jvm_heap');
require('views/main/service/info/metrics/hdfs/io');
require('views/main/service/info/metrics/hdfs/rpc');
require('views/main/service/info/metrics/hdfs/file_operations');
require('views/main/service/info/metrics/hdfs/gc');
require('views/main/service/info/metrics/hdfs/space_utilization');
require('views/main/service/info/metrics/hdfs/block_status');
require('views/main/service/info/metrics/yarn/gc');
require('views/main/service/info/metrics/yarn/jvm_threads');
require('views/main/service/info/metrics/yarn/jvm_heap');
require('views/main/service/info/metrics/yarn/rpc');
require('views/main/service/info/metrics/yarn/allocated');
require('views/main/service/info/metrics/yarn/allocated_container');
require('views/main/service/info/metrics/yarn/apps_current_states');
require('views/main/service/info/metrics/yarn/apps_finished_states');
require('views/main/service/info/metrics/yarn/nms');
require('views/main/service/info/metrics/yarn/qmr');
require('views/main/service/info/metrics/hbase/cluster_requests');
require('views/main/service/info/metrics/hbase/regionserver_rw_requests');
require('views/main/service/info/metrics/hbase/regionserver_regions');
require('views/main/service/info/metrics/hbase/regionserver_queuesize');
require('views/main/service/info/metrics/hbase/hlog_split_time');
require('views/main/service/info/metrics/hbase/hlog_split_size');
require('views/main/service/info/metrics/flume/channel_sum');
require('views/main/service/info/metrics/flume/channel_size_mma');
require('views/main/service/info/metrics/flume/flume_incoming_sum');
require('views/main/service/info/metrics/flume/flume_incoming_mma');
require('views/main/service/info/metrics/flume/flume_outgoing_sum');
require('views/main/service/info/metrics/flume/flume_outgoing_mma');
require('views/main/service/info/metrics/flume/channel_fill_pct');
require('views/main/service/info/metrics/flume/channel_size');
require('views/main/service/info/metrics/flume/sink_connection_failed');
require('views/main/service/info/metrics/flume/sink_drain_success');
require('views/main/service/info/metrics/flume/source_accepted');
require('views/main/service/info/metrics/flume/gc');
require('views/main/service/info/metrics/flume/jvm_heap');
require('views/main/service/info/metrics/flume/jvm_threads_runnable');
require('views/main/service/info/metrics/flume/cpu_user');
require('views/main/service/info/metrics/flume/flume_metric_graph');
require('views/main/service/info/metrics/flume/flume_metric_graphs');
require('views/main/service/info/metrics/storm/slots_number_metric');
require('views/main/service/info/metrics/storm/executors_metric');
require('views/main/service/info/metrics/storm/tasks_metric');
require('views/main/service/info/metrics/storm/topologies_metric');
require('views/main/service/info/metrics/kafka/broker_topic');
require('views/main/service/info/metrics/kafka/kafka_controller');
require('views/main/service/info/metrics/kafka/controller_status');
require('views/main/service/info/metrics/kafka/replica_manager');
require('views/main/service/info/metrics/kafka/replica_fetcher');
require('views/main/service/info/metrics/kafka/kafka_log_flush');

require('views/main/service/info/metrics/lhotse/issue_avg_time');
require('views/main/service/info/metrics/lhotse/base_request_count');
require('views/main/service/info/metrics/lhotse/issued_instance_count');
require('views/main/service/info/metrics/lhotse/issued_except_count');
require('views/main/service/info/metrics/lhotse/running_instance_count');
require('views/main/service/info/metrics/lhotse/failed_instance_count');
require('views/main/service/info/metrics/lhotse/waiting_instance_count');
require('views/main/service/info/metrics/lhotse/ready_instance_count');
require('views/main/service/info/metrics/lhotse/new_instance_count');
require('views/main/service/info/metrics/lhotse/succ_instance_count');
require('views/main/service/info/metrics/lhotse/alive_runner_count');

require('views/main/service/info/metrics/pgxz/connection_count');
require('views/main/service/info/metrics/pgxz/transaction_count');
require('views/main/service/info/metrics/pgxz/statistic');

require('views/main/service/add_view');
require('views/main/service/reassign_view');
require('views/main/service/reassign/step1_view');
require('views/main/service/reassign/step2_view');
require('views/main/service/reassign/step3_view');
require('views/main/service/reassign/step4_view');
require('views/main/service/reassign/step5_view');
require('views/main/service/reassign/step6_view');
require('views/main/service/manage_config_groups_view');
require('views/main/charts/menu');
require('views/main/charts/heatmap');
require('views/main/charts/heatmap/heatmap_rack');
require('views/main/charts/heatmap/heatmap_host');
require('views/main/charts/heatmap/heatmap_host_detail');

// ADD NEW METRICS HERE
require('views/main/service/info/metrics/lhotse/issue_avg_time');
require('views/main/service/info/metrics/lhotse/base_request_count');
require('views/main/service/info/metrics/lhotse/issued_instance_count');
require('views/main/service/info/metrics/lhotse/issued_except_count');
require('views/main/service/info/metrics/lhotse/running_instance_count');
require('views/main/service/info/metrics/lhotse/failed_instance_count');
require('views/main/service/info/metrics/lhotse/waiting_instance_count');
require('views/main/service/info/metrics/lhotse/ready_instance_count');
require('views/main/service/info/metrics/lhotse/new_instance_count');
require('views/main/service/info/metrics/lhotse/succ_instance_count');
require('views/main/service/info/metrics/lhotse/succ_avg_time');
require('views/main/service/info/metrics/lhotse/alive_runner_count');

require('views/main/views_view');

require('views/installer');
require('views/wizard/step0_view');
require('views/wizard/step1_view');
require('views/wizard/step2_view');
require('views/wizard/step3_view');
require('views/wizard/step3/hostLogPopupBody_view');
require('views/wizard/step3/hostWarningPopupBody_view');
require('views/wizard/step3/hostWarningPopupFooter_view');
require('views/wizard/step4_view');
require('views/wizard/step5_view');
require('views/wizard/step6_view');
require('views/wizard/step7_view');
require('views/main/service/reassign/step7_view');
require('views/wizard/step8_view');
require('views/wizard/step9_view');
require('views/wizard/step9/hostLogPopupBody_view');
require('views/wizard/step10_view');
require('views/loading');

require('views/experimental');
