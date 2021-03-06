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
package org.apache.ambari.server.configuration;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.util.EnumSet;
import java.util.HashMap;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Properties;

import org.apache.ambari.server.AmbariException;
import org.apache.ambari.server.orm.JPATableGenerationStrategy;
import org.apache.ambari.server.orm.PersistenceType;
import org.apache.ambari.server.security.ClientSecurityType;
import org.apache.ambari.server.security.authorization.LdapServerProperties;
import org.apache.ambari.server.security.encryption.CredentialProvider;
import org.apache.ambari.server.utils.ShellCommandUtil;
import org.apache.commons.io.FileUtils;
import org.apache.commons.lang.RandomStringUtils;
import org.apache.commons.lang.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.google.inject.Singleton;


/**
 * Ambari configuration.
 * Reads properties from tbds.properties
 */
@Singleton
public class Configuration {

  public static final String CONFIG_FILE = "tbds.properties";
  public static final String BOOTSTRAP_DIR = "bootstrap.dir";

  /**
   *  PREFIX_DIR is shared in ambari-agent.ini and should only be called by unit tests.
   *  For all server-side processing, it should be retrieved from <code>HostImpl.getPrefix()</code>
   */
  public static final String PREFIX_DIR = "/var/lib/ambari-agent/data";

  public static final String BOOTSTRAP_DIR_DEFAULT = "/var/run/tbds-server/bootstrap";
  public static final String VIEWS_DIR = "views.dir";
  public static final String VIEWS_DIR_DEFAULT = "/var/lib/tbds-server/resources/views";
  public static final String VIEWS_VALIDATE = "views.validate";
  public static final String VIEWS_VALIDATE_DEFAULT = "false";
  public static final String WEBAPP_DIR = "webapp.dir";
  public static final String BOOTSTRAP_SCRIPT = "bootstrap.script";
  public static final String BOOTSTRAP_SCRIPT_DEFAULT = "/usr/bin/ambari_bootstrap";
  public static final String BOOTSTRAP_SETUP_AGENT_SCRIPT = "bootstrap.setup_agent.script";
  public static final String BOOTSTRAP_SETUP_AGENT_PASSWORD = "bootstrap.setup_agent.password";
  public static final String BOOTSTRAP_MASTER_HOSTNAME = "bootstrap.master_host_name";
  public static final String RECOMMENDATIONS_DIR = "recommendations.dir";
  public static final String RECOMMENDATIONS_DIR_DEFAULT = "/var/run/tbds-server/stack-recommendations";
  public static final String STACK_ADVISOR_SCRIPT = "stackadvisor.script";
  public static final String STACK_ADVISOR_SCRIPT_DEFAULT = "/var/lib/tbds-server/resources/scripts/stack_advisor.py";
  public static final String AMBARI_PYTHON_WRAP_KEY = "ambari.python.wrap";
  public static final String AMBARI_PYTHON_WRAP_DEFAULT = "ambari-python-wrap";
  public static final String API_AUTHENTICATE = "api.authenticate";
  public static final String API_USE_SSL = "api.ssl";
  public static final String API_CSRF_PREVENTION_KEY = "api.csrfPrevention.enabled";
  public static final String SRVR_TWO_WAY_SSL_KEY = "security.server.two_way_ssl";
  public static final String SRVR_TWO_WAY_SSL_PORT_KEY = "security.server.two_way_ssl.port";
  public static final String SRVR_ONE_WAY_SSL_PORT_KEY = "security.server.one_way_ssl.port";
  public static final String SRVR_KSTR_DIR_KEY = "security.server.keys_dir";
  public static final String SRVR_CRT_NAME_KEY = "security.server.cert_name";
  public static final String SRVR_CSR_NAME_KEY = "security.server.csr_name";
  public static final String SRVR_KEY_NAME_KEY = "security.server.key_name";
  public static final String KSTR_NAME_KEY = "security.server.keystore_name";
  public static final String SRVR_CRT_PASS_FILE_KEY = "security.server.crt_pass_file";
  public static final String SRVR_CRT_PASS_KEY = "security.server.crt_pass";
  public static final String SRVR_CRT_PASS_LEN_KEY = "security.server.crt_pass.len";
  public static final String PASSPHRASE_ENV_KEY = "security.server.passphrase_env_var";
  public static final String PASSPHRASE_KEY = "security.server.passphrase";
  public static final String SRVR_DISABLED_CIPHERS = "security.server.disabled.ciphers";
  public static final String SRVR_DISABLED_PROTOCOLS = "security.server.disabled.protocols";
  public static final String RESOURCES_DIR_KEY = "resources.dir";
  public static final String METADETA_DIR_PATH = "metadata.path";
  public static final String COMMON_SERVICES_DIR_PATH = "common.services.path";
  public static final String SERVER_VERSION_FILE = "server.version.file";
  public static final String SERVER_VERSION_KEY = "version";
  public static final String JAVA_HOME_KEY = "java.home";
  public static final String JDK_NAME_KEY = "jdk.name";
  public static final String JCE_NAME_KEY = "jce.name";
  public static final String CLIENT_SECURITY_KEY = "client.security";
  public static final String CLIENT_API_PORT_KEY = "client.api.port";
  public static final String CLIENT_API_SSL_PORT_KEY = "client.api.ssl.port";
  public static final String CLIENT_API_SSL_KSTR_DIR_NAME_KEY = "client.api.ssl.keys_dir";
  public static final String CLIENT_API_SSL_KSTR_NAME_KEY = "client.api.ssl.keystore_name";
  public static final String CLIENT_API_SSL_CRT_NAME_KEY = "client.api.ssl.cert_name";
  public static final String CLIENT_API_SSL_CRT_PASS_FILE_NAME_KEY = "client.api.ssl.cert_pass_file";
  public static final String CLIENT_API_SSL_CRT_PASS_KEY = "client.api.ssl.crt_pass";
  public static final String CLIENT_API_SSL_KEY_NAME_KEY = "client.api.ssl.key_name";
  public static final String SERVER_DB_NAME_KEY = "server.jdbc.database_name";
  public static final String SERVER_DB_NAME_DEFAULT = "ambari";
  public static final String REQUEST_READ_TIMEOUT = "views.request.read.timeout.millis";
  public static final String REQUEST_READ_TIMEOUT_DEFAULT= "10000";
  public static final String REQUEST_CONNECT_TIMEOUT = "views.request.connect.timeout.millis";
  public static final String REQUEST_CONNECT_TIMEOUT_DEFAULT = "5000";
  public static final String SERVER_JDBC_POSTGRES_SCHEMA_NAME = "server.jdbc.postgres.schema";
  public static final String OJDBC_JAR_NAME_KEY = "db.oracle.jdbc.name";
  public static final String OJDBC_JAR_NAME_DEFAULT = "ojdbc6.jar";
  public static final String MYSQL_JAR_NAME_KEY = "db.mysql.jdbc.name";
  public static final String MYSQL_JAR_NAME_DEFAULT = "mysql-connector-java.jar";
  public static final String IS_LDAP_CONFIGURED = "ambari.ldap.isConfigured";
  public static final String LDAP_USE_SSL_KEY = "authentication.ldap.useSSL";
  public static final String LDAP_PRIMARY_URL_KEY = "authentication.ldap.primaryUrl";
  public static final String LDAP_SECONDARY_URL_KEY = "authentication.ldap.secondaryUrl";
  public static final String LDAP_BASE_DN_KEY = "authentication.ldap.baseDn";
  public static final String LDAP_BIND_ANONYMOUSLY_KEY = "authentication.ldap.bindAnonymously";
  public static final String LDAP_MANAGER_DN_KEY = "authentication.ldap.managerDn";
  public static final String LDAP_MANAGER_PASSWORD_KEY = "authentication.ldap.managerPassword";
  public static final String LDAP_DN_ATTRIBUTE_KEY = "authentication.ldap.dnAttribute";
  public static final String LDAP_USERNAME_ATTRIBUTE_KEY = "authentication.ldap.usernameAttribute";
  public static final String LDAP_USER_BASE_KEY = "authentication.ldap.userBase";
  public static final String LDAP_USER_OBJECT_CLASS_KEY = "authentication.ldap.userObjectClass";
  public static final String LDAP_GROUP_BASE_KEY = "authentication.ldap.groupBase";
  public static final String LDAP_GROUP_OBJECT_CLASS_KEY = "authentication.ldap.groupObjectClass";
  public static final String LDAP_GROUP_NAMING_ATTR_KEY = "authentication.ldap.groupNamingAttr";
  public static final String LDAP_GROUP_MEMEBERSHIP_ATTR_KEY = "authentication.ldap.groupMembershipAttr";
  public static final String LDAP_ADMIN_GROUP_MAPPING_RULES_KEY = "authorization.ldap.adminGroupMappingRules";
  public static final String LDAP_GROUP_SEARCH_FILTER_KEY = "authorization.ldap.groupSearchFilter";
  public static final String LDAP_REFERRAL_KEY = "authentication.ldap.referral";
  public static final String SERVER_EC_CACHE_SIZE = "server.ecCacheSize";
  public static final String SERVER_STALE_CONFIG_CACHE_ENABLED_KEY = "server.cache.isStale.enabled";
  public static final String SERVER_PERSISTENCE_TYPE_KEY = "server.persistence.type";
  public static final String SERVER_JDBC_USER_NAME_KEY = "server.jdbc.user.name";
  public static final String SERVER_JDBC_USER_PASSWD_KEY = "server.jdbc.user.passwd";
  public static final String SERVER_JDBC_DRIVER_KEY = "server.jdbc.driver";
  public static final String SERVER_JDBC_URL_KEY = "server.jdbc.url";
  public static final String SERVER_JDBC_PROPERTIES_PREFIX = "server.jdbc.properties.";

  public static final String SERVER_JDBC_CONNECTION_POOL = "server.jdbc.connection-pool";
  public static final String SERVER_JDBC_CONNECTION_POOL_MIN_SIZE = "server.jdbc.connection-pool.min-size";
  public static final String SERVER_JDBC_CONNECTION_POOL_MAX_SIZE = "server.jdbc.connection-pool.max-size";
  public static final String SERVER_JDBC_CONNECTION_POOL_AQUISITION_SIZE = "server.jdbc.connection-pool.acquisition-size";
  public static final String SERVER_JDBC_CONNECTION_POOL_MAX_AGE = "server.jdbc.connection-pool.max-age";
  public static final String SERVER_JDBC_CONNECTION_POOL_MAX_IDLE_TIME = "server.jdbc.connection-pool.max-idle-time";
  public static final String SERVER_JDBC_CONNECTION_POOL_MAX_IDLE_TIME_EXCESS = "server.jdbc.connection-pool.max-idle-time-excess";
  public static final String SERVER_JDBC_CONNECTION_POOL_IDLE_TEST_INTERVAL = "server.jdbc.connection-pool.idle-test-interval";

  public static final String SERVER_JDBC_RCA_USER_NAME_KEY = "server.jdbc.rca.user.name";
  public static final String SERVER_JDBC_RCA_USER_PASSWD_KEY = "server.jdbc.rca.user.passwd";
  public static final String SERVER_JDBC_RCA_DRIVER_KEY = "server.jdbc.rca.driver";
  public static final String SERVER_JDBC_RCA_URL_KEY = "server.jdbc.rca.url";
  public static final String SERVER_JDBC_GENERATE_TABLES_KEY = "server.jdbc.generateTables";
  public static final String JDBC_UNIT_NAME = "ambari-server";
  public static final String JDBC_LOCAL_URL = "jdbc:postgresql://localhost/";
  public static final String JDBC_LOCAL_DRIVER = "org.postgresql.Driver";
  public static final String JDBC_IN_MEMORY_URL = "jdbc:derby:memory:myDB/ambari;create=true";
  public static final String JDBC_IN_MEMROY_DRIVER = "org.apache.derby.jdbc.EmbeddedDriver";
  public static final String HOSTNAME_MACRO = "{hostname}";
  public static final String JDBC_RCA_LOCAL_URL = "jdbc:postgresql://" + HOSTNAME_MACRO + "/ambarirca";
  public static final String JDBC_RCA_LOCAL_DRIVER = "org.postgresql.Driver";
  public static final String OS_FAMILY_KEY = "server.os_family";
  public static final String OS_VERSION_KEY = "server.os_type";
  public static final String SRVR_HOSTS_MAPPING = "server.hosts.mapping";
  // Command parameter names
  public static final String UPGRADE_FROM_STACK = "source_stack_version";
  public static final String UPGRADE_TO_STACK = "target_stack_version";
  public static final String SSL_TRUSTSTORE_PATH_KEY = "ssl.trustStore.path";
  public static final String SSL_TRUSTSTORE_PASSWORD_KEY = "ssl.trustStore.password";
  public static final String SSL_TRUSTSTORE_TYPE_KEY = "ssl.trustStore.type";
  public static final String JAVAX_SSL_TRUSTSTORE = "javax.net.ssl.trustStore";
  public static final String JAVAX_SSL_TRUSTSTORE_PASSWORD = "javax.net.ssl.trustStorePassword";
  public static final String JAVAX_SSL_TRUSTSTORE_TYPE = "javax.net.ssl.trustStoreType";
  public static final String GANGLIA_HTTPS_KEY = "ganglia.https";
  public static final String SRVR_TWO_WAY_SSL_PORT_DEFAULT = "8441";
  public static final String SRVR_ONE_WAY_SSL_PORT_DEFAULT = "8440";
  public static final String SRVR_CRT_NAME_DEFAULT = "ca.crt";
  public static final String SRVR_KEY_NAME_DEFAULT = "ca.key";
  public static final String SRVR_CSR_NAME_DEFAULT = "ca.csr";
  public static final String KSTR_NAME_DEFAULT = "keystore.p12";
  public static final String CLIENT_API_SSL_KSTR_NAME_DEFAULT = "https.keystore.p12";
  public static final String CLIENT_API_SSL_CRT_PASS_FILE_NAME_DEFAULT = "https.pass.txt";
  public static final String CLIENT_API_SSL_KEY_NAME_DEFAULT = "https.key";
  public static final String CLIENT_API_SSL_CRT_NAME_DEFAULT = "https.crt";
  public static final String GLOBAL_CONFIG_TAG = "global";
  public static final String MAPREDUCE2_LOG4J_CONFIG_TAG = "mapreduce2-log4j";
  public static final String RCA_ENABLED_PROPERTY = "rca_enabled";
  public static final String HIVE_CONFIG_TAG = "hive-site";
  public static final String HIVE_METASTORE_PASSWORD_PROPERTY = "javax.jdo.option.ConnectionPassword";
  public static final String MASTER_KEY_PERSISTED = "security.master.key.ispersisted";
  public static final String MASTER_KEY_LOCATION = "security.master.key.location";
  public static final String MASTER_KEY_ENV_PROP = "TBDS_SECURITY_MASTER_KEY";
  public static final String MASTER_KEY_FILENAME_DEFAULT = "master";

  /**
   * Key for repo validation suffixes.
   */
  public static final String REPO_SUFFIX_KEY_UBUNTU = "repo.validation.suffixes.ubuntu";
  public static final String REPO_SUFFIX_KEY_DEFAULT = "repo.validation.suffixes.default";

  public static final String EXECUTION_SCHEDULER_CLUSTERED = "server.execution.scheduler.isClustered";
  public static final String EXECUTION_SCHEDULER_THREADS = "server.execution.scheduler.maxThreads";
  public static final String EXECUTION_SCHEDULER_CONNECTIONS = "server.execution.scheduler.maxDbConnections";
  public static final String EXECUTION_SCHEDULER_MISFIRE_TOLERATION = "server.execution.scheduler.misfire.toleration.minutes";
  public static final String EXECUTION_SCHEDULER_START_DELAY = "server.execution.scheduler.start.delay.seconds";
  public static final String DEFAULT_SCHEDULER_THREAD_COUNT = "5";
  public static final String DEFAULT_SCHEDULER_MAX_CONNECTIONS = "5";
  public static final String DEFAULT_EXECUTION_SCHEDULER_MISFIRE_TOLERATION = "480";
  public static final String DEFAULT_SCHEDULER_START_DELAY_SECONDS = "120";
  public static final String SERVER_TMP_DIR_KEY = "server.tmp.dir";
  public static final String SERVER_TMP_DIR_DEFAULT = "/var/lib/tbds-server/tmp";
  public static final String EXTERNAL_SCRIPT_TIMEOUT_KEY = "server.script.timeout";
  public static final String EXTERNAL_SCRIPT_TIMEOUT_DEFAULT = "5000";
  public static final String DEF_ARCHIVE_EXTENSION;
  public static final String DEF_ARCHIVE_CONTENT_TYPE;

  /**
   * Kerberos related configuration options
   */
  public static final String KDC_PORT_KEY = "default.kdcserver.port";
  public static final String KDC_PORT_KEY_DEFAULT = "88";
  public static final String KDC_CONNECTION_CHECK_TIMEOUT_KEY = "kdcserver.connection.check.timeout";
  public static final String KDC_CONNECTION_CHECK_TIMEOUT_DEFAULT = "10000";
  public static final String KERBEROS_KEYTAB_CACHE_DIR_KEY = "kerberos.keytab.cache.dir";
  public static final String KERBEROS_KEYTAB_CACHE_DIR_DEFAULT = "/var/lib/tbds-server/data/cache";
  /**
   * This key defines whether stages of parallel requests are executed in
   * parallel or sequentally. Only stages from different requests
   * running on not interfering host sets may be executed in parallel.
   */
  public static final String PARALLEL_STAGE_EXECUTION_KEY = "server.stages.parallel";
  public static final String AGENT_TASK_TIMEOUT_KEY = "agent.task.timeout";
  public static final String AGENT_PACKAGE_INSTALL_TASK_TIMEOUT_KEY = "agent.package.install.task.timeout";
  public static final String AGENT_TASK_TIMEOUT_DEFAULT = "900";
  public static final String AGENT_PACKAGE_INSTALL_TASK_TIMEOUT_DEFAULT = "1800";

  public static final String CUSTOM_ACTION_DEFINITION_KEY = "custom.action.definitions";
  public static final String SHARED_RESOURCES_DIR_KEY = "shared.resources.dir";
  private static final String CUSTOM_ACTION_DEFINITION_DEF_VALUE = "/var/lib/tbds-server/resources/custom_action_definitions";

  private static final long SERVER_EC_CACHE_SIZE_DEFAULT = 10000L;
  private static final String SERVER_STALE_CONFIG_CACHE_ENABLED_DEFAULT = "true";
  private static final String SERVER_JDBC_USER_NAME_DEFAULT = "ambari";
  private static final String SERVER_JDBC_USER_PASSWD_DEFAULT = "bigdata";
  private static final String SERVER_JDBC_RCA_USER_NAME_DEFAULT = "mapred";
  private static final String SERVER_JDBC_RCA_USER_PASSWD_DEFAULT = "mapred";
  private static final String SRVR_TWO_WAY_SSL_DEFAULT = "false";
  private static final String SRVR_KSTR_DIR_DEFAULT = ".";
  private static final String API_CSRF_PREVENTION_DEFAULT = "true";
  private static final String SRVR_CRT_PASS_FILE_DEFAULT = "pass.txt";
  private static final String SRVR_CRT_PASS_LEN_DEFAULT = "50";
  private static final String SRVR_DISABLED_CIPHERS_DEFAULT = "";
  private static final String SRVR_DISABLED_PROTOCOLS_DEFAULT = "";
  private static final String PASSPHRASE_ENV_DEFAULT = "AMBARI_PASSPHRASE";
  private static final String RESOURCES_DIR_DEFAULT = "/var/lib/tbds-server/resources/";
  private static final String SHARED_RESOURCES_DIR_DEFAULT = "/usr/lib/tbds-server/lib/ambari_commons/resources";
  private static final String ANONYMOUS_AUDIT_NAME_KEY = "anonymous.audit.name";

  private static final int CLIENT_API_PORT_DEFAULT = 8080;
  private static final int CLIENT_API_SSL_PORT_DEFAULT = 8443;
  private static final String LDAP_BIND_ANONYMOUSLY_DEFAULT = "true";

  /**
   * !!! TODO: For embedded server only - should be removed later
   */
  private static final String LDAP_PRIMARY_URL_DEFAULT = "localhost:33389";
  private static final String LDAP_BASE_DN_DEFAULT = "dc=ambari,dc=apache,dc=org";
  private static final String LDAP_USERNAME_ATTRIBUTE_DEFAULT = "uid";
  private static final String LDAP_DN_ATTRIBUTE_DEFAULT = "dn";
  private static final String LDAP_USER_BASE_DEFAULT = "ou=people,dc=ambari,dc=apache,dc=org";
  private static final String LDAP_USER_OBJECT_CLASS_DEFAULT = "person";
  private static final String LDAP_GROUP_BASE_DEFAULT = "ou=groups,dc=ambari,dc=apache,dc=org";
  private static final String LDAP_GROUP_OBJECT_CLASS_DEFAULT = "group";
  private static final String LDAP_GROUP_NAMING_ATTR_DEFAULT = "cn";
  private static final String LDAP_GROUP_MEMBERSHIP_ATTR_DEFAULT = "member";
  private static final String LDAP_ADMIN_GROUP_MAPPING_RULES_DEFAULT = "Ambari Administrators";
  private static final String LDAP_GROUP_SEARCH_FILTER_DEFAULT = "";
  private static final String LDAP_REFERRAL_DEFAULT = "follow";

  /**
   * !!! TODO: for development purposes only, should be changed to 'false'
   */
  private static final String IS_LDAP_CONFIGURED_DEFAULT = "false";

  private static final String SERVER_PERSISTENCE_TYPE_DEFAULT = "local";
  private static final String SERVER_CONNECTION_MAX_IDLE_TIME = "server.connection.max.idle.millis";

  private static final String UBUNTU_OS = "ubuntu12";

  /**
   * Default for repo validation suffixes.
   */
  private static final String REPO_SUFFIX_DEFAULT = "/repodata/repomd.xml";
  private static final String REPO_SUFFIX_UBUNTU = "/dists/%s/Release";

  private static final String PARALLEL_STAGE_EXECUTION_DEFAULT = "true";

  private static final String CLIENT_THREADPOOL_SIZE_KEY = "client.threadpool.size.max";
  private static final int CLIENT_THREADPOOL_SIZE_DEFAULT = 25;
  private static final String AGENT_THREADPOOL_SIZE_KEY = "agent.threadpool.size.max";
  private static final int AGENT_THREADPOOL_SIZE_DEFAULT = 25;

  private static final String VIEW_EXTRACTION_THREADPOOL_MAX_SIZE_KEY = "view.extraction.threadpool.size.max";
  private static final int VIEW_EXTRACTION_THREADPOOL_MAX_SIZE_DEFAULT = 20;
  private static final String VIEW_EXTRACTION_THREADPOOL_CORE_SIZE_KEY = "view.extraction.threadpool.size.core";
  private static final int VIEW_EXTRACTION_THREADPOOL_CORE_SIZE_DEFAULT = 10;
  private static final String VIEW_EXTRACTION_THREADPOOL_TIMEOUT_KEY = "view.extraction.threadpool.timeout";
  private static final long VIEW_EXTRACTION_THREADPOOL_TIMEOUT_DEFAULT = 100000L;

  private static final String SERVER_HTTP_SESSION_INACTIVE_TIMEOUT = "server.http.session.inactive_timeout";

  // database pooling defaults
  private static final String DEFAULT_JDBC_POOL_MIN_CONNECTIONS = "5";
  private static final String DEFAULT_JDBC_POOL_MAX_CONNECTIONS = "32";
  private static final String DEFAULT_JDBC_POOL_ACQUISITION_SIZE = "5";
  private static final String DEFAULT_JDBC_POOL_MAX_IDLE_TIME_SECONDS = "14400";
  private static final String DEFAULT_JDBC_POOL_EXCESS_MAX_IDLE_TIME_SECONDS = "0";
  private static final String DEFAULT_JDBC_POOL_MAX_AGE_SECONDS = "0";
  private static final String DEFAULT_JDBC_POOL_IDLE_TEST_INTERVAL = "7200";
  
  //bootstrap init config
  private static final String BOOTSTRAP_AGENT_DEFAULT_LOGIN_USER_KEY="bootstarp_agent_default_login_user";
  private static final String BOOTSTRAP_AGENT_DEFAULT_LOGIN_USER_DEFAULT="tencent";
  private static final String BOOTSTRAP_AGENT_DEFAULT_LOGIN_PASSWROD_KEY="bootstarp_agent_default_login_password";
  private static final String BOOTSTRAP_AGENT_DEFAULT_LOGIN_PASSWROD_DEFAULT="tencent";
  private static final String BOOTSTRAP_SSH_USER_KEY="bootstarp_ssh_user";
  private static final String BOOTSTRAP_SSH_USER_DEFAULT="tencent";

  /**
   * The full path to the XML file that describes the different alert templates.
   */
  private static final String ALERT_TEMPLATE_FILE = "alerts.template.file";

  private static final Logger LOG = LoggerFactory.getLogger(
      Configuration.class);

  private Properties properties;
  private Map<String, String> configsMap;
  private CredentialProvider credentialProvider = null;
  private volatile boolean credentialProviderInitialized = false;
  private Map<String, String> customDbProperties = null;

  static {
    if (System.getProperty("os.name").contains("Windows")) {
      DEF_ARCHIVE_EXTENSION = ".zip";
      DEF_ARCHIVE_CONTENT_TYPE = "application/zip";
    }
    else {
      DEF_ARCHIVE_EXTENSION = ".tar.gz";
      DEF_ARCHIVE_CONTENT_TYPE = "application/x-ustar";
    }
  }

  /**
   * The {@link DatabaseType} enum represents the database being used.
   */
  public enum DatabaseType {
    POSTGRES("postgres"),
    ORACLE("oracle"),
    MYSQL("mysql"),
    DERBY("derby"),
    SQL_SERVER("sqlserver");

    private static final Map<String, DatabaseType> m_mappedTypes =
        new HashMap<String, Configuration.DatabaseType>(5);

    static {
      for (DatabaseType databaseType : EnumSet.allOf(DatabaseType.class)) {
        m_mappedTypes.put(databaseType.getName(), databaseType);
      }
    }

    /**
     * The JDBC URL type name.
     */
    private String m_databaseType;

    /**
     * Constructor.
     *
     */
    private DatabaseType(String databaseType) {
      m_databaseType = databaseType;
    }

    /**
     * Gets an internal name for this database type.
     *
     * @return the internal name for this database type.
     */
    public String getName() {
      return m_databaseType;
    }

    public DatabaseType get(String databaseTypeName) {
      return m_mappedTypes.get(databaseTypeName);
    }
  }

  /**
   * The {@link ConnectionPoolType} is used to define which pooling mechanism
   * JDBC should use.
   */
  public enum ConnectionPoolType {
    INTERNAL("internal"), C3P0("c3p0");

    /**
     * The connection pooling name.
     */
    private String m_name;

    /**
     * Constructor.
     *
     * @param name
     */
    private ConnectionPoolType(String name) {
      m_name = name;
    }

    /**
     * Gets an internal name for this connection pool type.
     *
     * @return the internal name for this connection pool type.
     */
    public String getName() {
      return m_name;
    }
  }

  public Configuration() {
    this(readConfigFile());
  }

  /**
   * This constructor is called from default constructor and
   * also from most tests.
   * @param properties properties to use for testing and in production using
   * the Conf object.
   */
  public Configuration(Properties properties) {
    this.properties = properties;

    configsMap = new HashMap<String, String>();
    configsMap.put(AMBARI_PYTHON_WRAP_KEY, properties.getProperty(
        AMBARI_PYTHON_WRAP_KEY, AMBARI_PYTHON_WRAP_DEFAULT));
    configsMap.put(SRVR_TWO_WAY_SSL_KEY, properties.getProperty(
        SRVR_TWO_WAY_SSL_KEY, SRVR_TWO_WAY_SSL_DEFAULT));
    configsMap.put(SRVR_TWO_WAY_SSL_PORT_KEY, properties.getProperty(
        SRVR_TWO_WAY_SSL_PORT_KEY, SRVR_TWO_WAY_SSL_PORT_DEFAULT));
    configsMap.put(SRVR_ONE_WAY_SSL_PORT_KEY, properties.getProperty(
        SRVR_ONE_WAY_SSL_PORT_KEY, SRVR_ONE_WAY_SSL_PORT_DEFAULT));
    configsMap.put(SRVR_KSTR_DIR_KEY, properties.getProperty(
        SRVR_KSTR_DIR_KEY, SRVR_KSTR_DIR_DEFAULT));
    configsMap.put(SRVR_CRT_NAME_KEY, properties.getProperty(
        SRVR_CRT_NAME_KEY, SRVR_CRT_NAME_DEFAULT));
    configsMap.put(SRVR_KEY_NAME_KEY, properties.getProperty(
      SRVR_KEY_NAME_KEY, SRVR_KEY_NAME_DEFAULT));
    configsMap.put(SRVR_CSR_NAME_KEY, properties.getProperty(
      SRVR_CSR_NAME_KEY, SRVR_CSR_NAME_DEFAULT));
    configsMap.put(KSTR_NAME_KEY, properties.getProperty(
        KSTR_NAME_KEY, KSTR_NAME_DEFAULT));
    configsMap.put(SRVR_CRT_PASS_FILE_KEY, properties.getProperty(
        SRVR_CRT_PASS_FILE_KEY, SRVR_CRT_PASS_FILE_DEFAULT));
    configsMap.put(PASSPHRASE_ENV_KEY, properties.getProperty(
        PASSPHRASE_ENV_KEY, PASSPHRASE_ENV_DEFAULT));
    configsMap.put(PASSPHRASE_KEY, System.getenv(configsMap.get(
        PASSPHRASE_ENV_KEY)));
    configsMap.put(RESOURCES_DIR_KEY, properties.getProperty(
        RESOURCES_DIR_KEY, RESOURCES_DIR_DEFAULT));
    configsMap.put(SRVR_CRT_PASS_LEN_KEY, properties.getProperty(
        SRVR_CRT_PASS_LEN_KEY, SRVR_CRT_PASS_LEN_DEFAULT));
    configsMap.put(SRVR_DISABLED_CIPHERS, properties.getProperty(
        SRVR_DISABLED_CIPHERS, SRVR_DISABLED_CIPHERS_DEFAULT));
    configsMap.put(SRVR_DISABLED_PROTOCOLS, properties.getProperty(
        SRVR_DISABLED_PROTOCOLS, SRVR_DISABLED_PROTOCOLS_DEFAULT));

    configsMap.put(CLIENT_API_SSL_KSTR_DIR_NAME_KEY, properties.getProperty(
      CLIENT_API_SSL_KSTR_DIR_NAME_KEY, configsMap.get(SRVR_KSTR_DIR_KEY)));
    configsMap.put(CLIENT_API_SSL_KSTR_NAME_KEY, properties.getProperty(
      CLIENT_API_SSL_KSTR_NAME_KEY, CLIENT_API_SSL_KSTR_NAME_DEFAULT));
    configsMap.put(CLIENT_API_SSL_CRT_PASS_FILE_NAME_KEY, properties.getProperty(
      CLIENT_API_SSL_CRT_PASS_FILE_NAME_KEY, CLIENT_API_SSL_CRT_PASS_FILE_NAME_DEFAULT));
    configsMap.put(CLIENT_API_SSL_KEY_NAME_KEY, properties.getProperty(
      CLIENT_API_SSL_KEY_NAME_KEY, CLIENT_API_SSL_KEY_NAME_DEFAULT));
    configsMap.put(CLIENT_API_SSL_CRT_NAME_KEY, properties.getProperty(
      CLIENT_API_SSL_CRT_NAME_KEY, CLIENT_API_SSL_CRT_NAME_DEFAULT));
    configsMap.put(JAVA_HOME_KEY, properties.getProperty(
        JAVA_HOME_KEY));
    configsMap.put(PARALLEL_STAGE_EXECUTION_KEY, properties.getProperty(
            PARALLEL_STAGE_EXECUTION_KEY, PARALLEL_STAGE_EXECUTION_DEFAULT));
    configsMap.put(SERVER_TMP_DIR_KEY, properties.getProperty(
            SERVER_TMP_DIR_KEY, SERVER_TMP_DIR_DEFAULT));
    configsMap.put(EXTERNAL_SCRIPT_TIMEOUT_KEY, properties.getProperty(
            EXTERNAL_SCRIPT_TIMEOUT_KEY, EXTERNAL_SCRIPT_TIMEOUT_DEFAULT));

    configsMap.put(SHARED_RESOURCES_DIR_KEY, properties.getProperty(
       SHARED_RESOURCES_DIR_KEY, SHARED_RESOURCES_DIR_DEFAULT));

    configsMap.put(KDC_PORT_KEY, properties.getProperty(
        KDC_PORT_KEY, KDC_PORT_KEY_DEFAULT));


    File passFile = new File(configsMap.get(SRVR_KSTR_DIR_KEY) + File.separator
        + configsMap.get(SRVR_CRT_PASS_FILE_KEY));
    String password = null;

    if (!passFile.exists()) {
      LOG.info("Generation of file with password");
      try {
        password = RandomStringUtils.randomAlphanumeric(Integer
            .parseInt(configsMap.get(SRVR_CRT_PASS_LEN_KEY)));
        FileUtils.writeStringToFile(passFile, password);
        ShellCommandUtil.setUnixFilePermissions(
               ShellCommandUtil.MASK_OWNER_ONLY_RW, passFile.getAbsolutePath());
      } catch (IOException e) {
        e.printStackTrace();
        throw new RuntimeException(
            "Error reading certificate password from file");
      }
    } else {
      LOG.info("Reading password from existing file");
      try {
        password = FileUtils.readFileToString(passFile);
        password = password.replaceAll("\\p{Cntrl}", "");
      } catch (IOException e) {
        e.printStackTrace();
      }
    }
    configsMap.put(SRVR_CRT_PASS_KEY, password);

    if (getApiSSLAuthentication()) {
      LOG.info("API SSL Authentication is turned on.");
      File httpsPassFile = new File(configsMap.get(CLIENT_API_SSL_KSTR_DIR_NAME_KEY)
        + File.separator + configsMap.get(CLIENT_API_SSL_CRT_PASS_FILE_NAME_KEY));

      if (httpsPassFile.exists()) {
        LOG.info("Reading password from existing file");
        try {
          password = FileUtils.readFileToString(httpsPassFile);
          password = password.replaceAll("\\p{Cntrl}", "");
        } catch (IOException e) {
          e.printStackTrace();
          throw new RuntimeException("Error reading certificate password from" +
            " file " + httpsPassFile.getAbsolutePath());
        }
      } else {
        LOG.error("There is no keystore for https UI connection.");
        LOG.error("Run \"tbds-server setup-https\" or set " + Configuration.API_USE_SSL + " = false.");
        throw new RuntimeException("Error reading certificate password from " +
          "file " + httpsPassFile.getAbsolutePath());

      }

      configsMap.put(CLIENT_API_SSL_CRT_PASS_KEY, password);
    }

    loadSSLParams();
  }

  /**
   * Get the property value for the given key.
   *
   * @return the property value
   */
  public String getProperty(String key) {
    return properties.getProperty(key);
  }

  /**
   * Loads trusted certificates store properties
   */
  protected void loadSSLParams(){
    if (properties.getProperty(SSL_TRUSTSTORE_PATH_KEY) != null) {
      System.setProperty(JAVAX_SSL_TRUSTSTORE, properties.getProperty(SSL_TRUSTSTORE_PATH_KEY));
    }
    if (properties.getProperty(SSL_TRUSTSTORE_PASSWORD_KEY) != null) {
      String ts_password = readPasswordFromStore(
              properties.getProperty(SSL_TRUSTSTORE_PASSWORD_KEY));
      if (ts_password != null) {
        System.setProperty(JAVAX_SSL_TRUSTSTORE_PASSWORD, ts_password);
      } else {
        System.setProperty(JAVAX_SSL_TRUSTSTORE_PASSWORD,
                properties.getProperty(SSL_TRUSTSTORE_PASSWORD_KEY));
      }
    }
    if (properties.getProperty(SSL_TRUSTSTORE_TYPE_KEY) != null) {
      System.setProperty(JAVAX_SSL_TRUSTSTORE_TYPE, properties.getProperty(SSL_TRUSTSTORE_TYPE_KEY));
    }
  }

  private synchronized void loadCredentialProvider() {
    if (!credentialProviderInitialized) {
      try {
        credentialProvider = new CredentialProvider(null,
          getMasterKeyLocation(), isMasterKeyPersisted());
      } catch (Exception e) {
        LOG.info("Credential provider creation failed. Reason: " + e.getMessage());
        if (LOG.isDebugEnabled()) {
          e.printStackTrace();
        }
        credentialProvider = null;
      }
      credentialProviderInitialized = true;
    }
  }

  /**
   * Find, read, and parse the configuration file.
   * @return the properties that were found or empty if no file was found
   */
  private static Properties readConfigFile() {
    Properties properties = new Properties();

    //Get property file stream from classpath
    InputStream inputStream = Configuration.class.getClassLoader().getResourceAsStream(CONFIG_FILE);

    if (inputStream == null) {
      throw new RuntimeException(CONFIG_FILE + " not found in classpath");
    }

    // load the properties
    try {
      properties.load(inputStream);
      inputStream.close();
    } catch (FileNotFoundException fnf) {
      LOG.info("No configuration file " + CONFIG_FILE + " found in classpath.", fnf);
    } catch (IOException ie) {
      throw new IllegalArgumentException("Can't read configuration file " +
          CONFIG_FILE, ie);
    }

    return properties;
  }

  /**
   * Get the views directory.
   *
   * @return the views directory
   */
  public File getViewsDir() {
    String fileName = properties.getProperty(VIEWS_DIR, VIEWS_DIR_DEFAULT);
    return new File(fileName);
  }

  /**
   * Determine whether or not view validation is enabled.
   *
   * @return true if view validation is enabled
   */
  public boolean isViewValidationEnabled() {
    return "true".equalsIgnoreCase(properties.getProperty(VIEWS_VALIDATE, VIEWS_VALIDATE_DEFAULT));
  }

  public File getBootStrapDir() {
    String fileName = properties.getProperty(BOOTSTRAP_DIR, BOOTSTRAP_DIR_DEFAULT);
    return new File(fileName);
  }

  public String getBootStrapScript() {
    return properties.getProperty(BOOTSTRAP_SCRIPT, BOOTSTRAP_SCRIPT_DEFAULT);
  }

  public String getBootSetupAgentScript() {
    return properties.getProperty(BOOTSTRAP_SETUP_AGENT_SCRIPT,
        "/usr/lib/python2.6/site-packages/ambari_server/setupAgent.py");
  }
  
  public String getAgentDefaultLoginUser(){
	  return properties.getProperty(BOOTSTRAP_AGENT_DEFAULT_LOGIN_USER_KEY, BOOTSTRAP_AGENT_DEFAULT_LOGIN_USER_DEFAULT);
  }
  
  public String getAgentDefaultLoginPassword(){
	  return properties.getProperty(BOOTSTRAP_AGENT_DEFAULT_LOGIN_PASSWROD_KEY, BOOTSTRAP_AGENT_DEFAULT_LOGIN_PASSWROD_DEFAULT);
  }
  
  public String getBootstrapSSHUser(){
	  return properties.getProperty(BOOTSTRAP_SSH_USER_KEY, BOOTSTRAP_SSH_USER_DEFAULT);
  }

  public String getBootSetupAgentPassword() {
    String pass = configsMap.get(PASSPHRASE_KEY);

    if (null != pass) {
      return pass;
    }

    // fallback
    return properties.getProperty(BOOTSTRAP_SETUP_AGENT_PASSWORD, "password");
  }

  public File getRecommendationsDir() {
    String fileName = properties.getProperty(RECOMMENDATIONS_DIR, RECOMMENDATIONS_DIR_DEFAULT);
    return new File(fileName);
  }

  public String getStackAdvisorScript() {
    return properties.getProperty(STACK_ADVISOR_SCRIPT, STACK_ADVISOR_SCRIPT_DEFAULT);
  }

  /**
   * Get the map with server config parameters.
   * Keys - public constants of this class
   * @return the map with server config parameters
   */
  public Map<String, String> getConfigsMap() {
    return configsMap;
  }

  /**
   * Checks if CSRF protection enabled
   * @return true if CSRF protection filter should be enabled
   */
  public boolean csrfProtectionEnabled() {
    return "true".equalsIgnoreCase(properties.getProperty(API_CSRF_PREVENTION_KEY, API_CSRF_PREVENTION_DEFAULT));
  }

  /**
   * Gets client security type
   * @return appropriate ClientSecurityType
   */
  public ClientSecurityType getClientSecurityType() {
    return ClientSecurityType.fromString(properties.getProperty(CLIENT_SECURITY_KEY));
  }

  public void setClientSecurityType(ClientSecurityType type) {
    properties.setProperty(CLIENT_SECURITY_KEY, type.toString());
  }

  public void setLdap(String host, String userClass, String userNameAttr, String groupClass, String groupName, String groupMember,
      String baseDN, boolean anon, String managerDN, String managerPass) {
    properties.setProperty(LDAP_PRIMARY_URL_KEY, host);
    properties.setProperty(LDAP_USER_OBJECT_CLASS_KEY, userClass);
    properties.setProperty(LDAP_USERNAME_ATTRIBUTE_KEY, userNameAttr);
    properties.setProperty(LDAP_GROUP_OBJECT_CLASS_KEY, groupClass);
    properties.setProperty(LDAP_GROUP_NAMING_ATTR_KEY, groupName);
    properties.setProperty(LDAP_GROUP_MEMEBERSHIP_ATTR_KEY, groupMember);
    properties.setProperty(LDAP_BASE_DN_KEY, baseDN);
    properties.setProperty(LDAP_BIND_ANONYMOUSLY_KEY, String.valueOf(anon));
    properties.setProperty(LDAP_MANAGER_DN_KEY, managerDN);
    properties.setProperty(LDAP_MANAGER_PASSWORD_KEY, managerPass);
  }

  public String getWebAppDir() {
    LOG.info("Web App DIR test " + properties.getProperty(WEBAPP_DIR));
    return properties.getProperty(WEBAPP_DIR, "web");
  }

  /**
   * Get the file that will be used for host mapping.
   * @return null if such a file is not present, value if present.
   */
  public String getHostsMapFile() {
    LOG.info("Hosts Mapping File " + properties.getProperty(SRVR_HOSTS_MAPPING));
    return properties.getProperty(SRVR_HOSTS_MAPPING);
  }

  /**
   * Gets ambari stack-path
   * @return String
   */
  public String getMetadataPath() {
    return properties.getProperty(METADETA_DIR_PATH);
  }

  /**
   * Gets ambari common services path
   * @return String
   */
  public String getCommonServicesPath() {
    return properties.getProperty(COMMON_SERVICES_DIR_PATH);
  }

  public String getServerVersionFilePath() {
    return properties.getProperty(SERVER_VERSION_FILE);
  }

  /**
   * Check to see if the API should be authenticated or not
   * @return false if not, true if the authentication is enabled.
   */
  public boolean getApiAuthentication() {
    return ("true".equals(properties.getProperty(API_AUTHENTICATE, "false")));
  }

  /**
   * Gets ssl api port
   * @return int
   */
  public int getClientSSLApiPort() {
    return Integer.parseInt(properties.getProperty(CLIENT_API_SSL_PORT_KEY, String.valueOf(CLIENT_API_SSL_PORT_DEFAULT)));
  }

  /**
   * Check to see if the API should be authenticated via ssl or not
   * @return false if not, true if ssl needs to be used.
   */
  public boolean getApiSSLAuthentication() {
    return ("true".equals(properties.getProperty(API_USE_SSL, "false")));
  }

  /**
   * Check to see if two-way SSL auth should be used between server and agents
   * or not
   *
   * @return true two-way SSL authentication is enabled
   */
  public boolean getTwoWaySsl() {
    return ("true".equals(properties.getProperty(SRVR_TWO_WAY_SSL_KEY,
      SRVR_TWO_WAY_SSL_DEFAULT)));
  }

  /**
   * Check persistence type Ambari Server should use. Possible values:
   * in-memory - use in-memory Derby database to store data
   * local - use local Postgres instance
   * remote - use provided jdbc driver name and url to connect to database
   */
  public PersistenceType getPersistenceType() {
    String value = properties.getProperty(SERVER_PERSISTENCE_TYPE_KEY, SERVER_PERSISTENCE_TYPE_DEFAULT);
    return PersistenceType.fromString(value);
  }

  public String getDatabaseDriver() {
    if (getPersistenceType() != PersistenceType.IN_MEMORY) {
      return properties.getProperty(SERVER_JDBC_DRIVER_KEY, JDBC_LOCAL_DRIVER);
    } else {
      return JDBC_IN_MEMROY_DRIVER;
    }
  }

  public String getDatabaseUrl() {
    if (getPersistenceType() != PersistenceType.IN_MEMORY) {
      String URI = properties.getProperty(SERVER_JDBC_URL_KEY);
      if (URI != null) {
        return URI;
      } else {
        return getLocalDatabaseUrl();
      }
    } else {
      return JDBC_IN_MEMORY_URL;
    }
  }

  public String getLocalDatabaseUrl() {
    String dbName = properties.getProperty(SERVER_DB_NAME_KEY);
    if(dbName == null || dbName.isEmpty()) {
      throw new RuntimeException("Server DB Name is not configured!");
    }

    return JDBC_LOCAL_URL + dbName;
  }

  public String getDatabaseUser() {
    return properties.getProperty(SERVER_JDBC_USER_NAME_KEY, SERVER_JDBC_USER_NAME_DEFAULT);
  }

  public String getDatabasePassword() {
    String passwdProp = properties.getProperty(SERVER_JDBC_USER_PASSWD_KEY);
    String dbpasswd = null;
    if (CredentialProvider.isAliasString(passwdProp)) {
      dbpasswd = readPasswordFromStore(passwdProp);
    }

    if (dbpasswd != null) {
      return dbpasswd;
    } else {
      return readPasswordFromFile(passwdProp, SERVER_JDBC_USER_PASSWD_DEFAULT);
    }
  }

  public String getRcaDatabaseDriver() {
    return properties.getProperty(SERVER_JDBC_RCA_DRIVER_KEY, JDBC_RCA_LOCAL_DRIVER);
  }

  public String getRcaDatabaseUrl() {
    return properties.getProperty(SERVER_JDBC_RCA_URL_KEY, JDBC_RCA_LOCAL_URL);
  }

  public String getRcaDatabaseUser() {
    return properties.getProperty(SERVER_JDBC_RCA_USER_NAME_KEY, SERVER_JDBC_RCA_USER_NAME_DEFAULT);
  }

  public String getRcaDatabasePassword() {
    String passwdProp = properties.getProperty(SERVER_JDBC_RCA_USER_PASSWD_KEY);
    if (passwdProp != null) {
      String dbpasswd = readPasswordFromStore(passwdProp);
      if (dbpasswd != null) {
        return dbpasswd;
      }
    }
    return readPasswordFromFile(passwdProp, SERVER_JDBC_RCA_USER_PASSWD_DEFAULT);
  }

  private String readPasswordFromFile(String filePath, String defaultPassword) {
    if (filePath == null) {
      LOG.debug("DB password file not specified - using default");
      return defaultPassword;
    } else {
      LOG.debug("Reading password from file {}", filePath);
      String password;
      try {
        password = FileUtils.readFileToString(new File(filePath));
        password = StringUtils.chomp(password);
      } catch (IOException e) {
        throw new RuntimeException("Unable to read database password", e);
      }
      return password;
    }
  }

  String readPasswordFromStore(String aliasStr) {
    String password = null;
    loadCredentialProvider();
    if (credentialProvider != null) {
      char[] result = null;
      try {
        result = credentialProvider.getPasswordForAlias(aliasStr);
      } catch (AmbariException e) {
        LOG.error("Error reading from credential store.");
        e.printStackTrace();
      }
      if (result != null) {
        password = new String(result);
      } else {
        LOG.error("Cannot read password for alias = " + aliasStr);
      }
    }
    return password;
  }

  /**
   * Gets parameters of LDAP server to connect to
   * @return LdapServerProperties object representing connection parameters
   */
  public LdapServerProperties getLdapServerProperties() {
    LdapServerProperties ldapServerProperties = new LdapServerProperties();

    ldapServerProperties.setPrimaryUrl(properties.getProperty(
        LDAP_PRIMARY_URL_KEY, LDAP_PRIMARY_URL_DEFAULT));
    ldapServerProperties.setSecondaryUrl(properties.getProperty(
        LDAP_SECONDARY_URL_KEY));
    ldapServerProperties.setUseSsl("true".equalsIgnoreCase(properties.
        getProperty(LDAP_USE_SSL_KEY)));
    ldapServerProperties.setAnonymousBind("true".
        equalsIgnoreCase(properties.getProperty(LDAP_BIND_ANONYMOUSLY_KEY,
            LDAP_BIND_ANONYMOUSLY_DEFAULT)));
    ldapServerProperties.setManagerDn(properties.getProperty(
        LDAP_MANAGER_DN_KEY));
    String ldapPasswordProperty = properties.getProperty(LDAP_MANAGER_PASSWORD_KEY);
    String ldapPassword = null;
    if (CredentialProvider.isAliasString(ldapPasswordProperty)) {
      ldapPassword = readPasswordFromStore(ldapPasswordProperty);
    }
    if (ldapPassword != null) {
      ldapServerProperties.setManagerPassword(ldapPassword);
    } else {
      if (ldapPasswordProperty != null && new File(ldapPasswordProperty).exists()) {
        ldapServerProperties.setManagerPassword(readPasswordFromFile(ldapPasswordProperty, ""));
      }
    }
    ldapServerProperties.setBaseDN(properties.getProperty
        (LDAP_BASE_DN_KEY, LDAP_BASE_DN_DEFAULT));
    ldapServerProperties.setUsernameAttribute(properties.
        getProperty(LDAP_USERNAME_ATTRIBUTE_KEY, LDAP_USERNAME_ATTRIBUTE_DEFAULT));

    ldapServerProperties.setUserBase(properties.getProperty(LDAP_USER_BASE_KEY, LDAP_USER_BASE_DEFAULT));
    ldapServerProperties.setUserObjectClass(properties.getProperty(LDAP_USER_OBJECT_CLASS_KEY, LDAP_USER_OBJECT_CLASS_DEFAULT));
    ldapServerProperties.setDnAttribute(properties.getProperty(LDAP_DN_ATTRIBUTE_KEY, LDAP_DN_ATTRIBUTE_DEFAULT));

    ldapServerProperties.setGroupBase(properties.
        getProperty(LDAP_GROUP_BASE_KEY, LDAP_GROUP_BASE_DEFAULT));
    ldapServerProperties.setGroupObjectClass(properties.
        getProperty(LDAP_GROUP_OBJECT_CLASS_KEY, LDAP_GROUP_OBJECT_CLASS_DEFAULT));
    ldapServerProperties.setGroupMembershipAttr(properties.getProperty(
        LDAP_GROUP_MEMEBERSHIP_ATTR_KEY, LDAP_GROUP_MEMBERSHIP_ATTR_DEFAULT));
    ldapServerProperties.setGroupNamingAttr(properties.
        getProperty(LDAP_GROUP_NAMING_ATTR_KEY, LDAP_GROUP_NAMING_ATTR_DEFAULT));
    ldapServerProperties.setAdminGroupMappingRules(properties.getProperty(
        LDAP_ADMIN_GROUP_MAPPING_RULES_KEY, LDAP_ADMIN_GROUP_MAPPING_RULES_DEFAULT));
    ldapServerProperties.setGroupSearchFilter(properties.getProperty(
        LDAP_GROUP_SEARCH_FILTER_KEY, LDAP_GROUP_SEARCH_FILTER_DEFAULT));
    ldapServerProperties.setReferralMethod(properties.getProperty(LDAP_REFERRAL_KEY, LDAP_REFERRAL_DEFAULT));

    if (properties.containsKey(LDAP_GROUP_BASE_KEY) ||
        properties.containsKey(LDAP_GROUP_OBJECT_CLASS_KEY) ||
        properties.containsKey(LDAP_GROUP_MEMEBERSHIP_ATTR_KEY) ||
        properties.containsKey(LDAP_GROUP_NAMING_ATTR_KEY) ||
        properties.containsKey(LDAP_ADMIN_GROUP_MAPPING_RULES_KEY) ||
        properties.containsKey(LDAP_GROUP_SEARCH_FILTER_KEY)) {
      ldapServerProperties.setGroupMappingEnabled(true);
    }

    return ldapServerProperties;
  }

  public boolean isLdapConfigured() {
    return Boolean.parseBoolean(properties.getProperty(IS_LDAP_CONFIGURED, IS_LDAP_CONFIGURED_DEFAULT));
  }

  public String getServerOsType() {
    return properties.getProperty(OS_VERSION_KEY, "");
  }

  public String getServerOsFamily() {
    return properties.getProperty(OS_FAMILY_KEY, "");
  }

  public String getMasterHostname(String defaultValue) {
    return properties.getProperty(BOOTSTRAP_MASTER_HOSTNAME, defaultValue);
  }

  public int getClientApiPort() {
    return Integer.parseInt(properties.getProperty(CLIENT_API_PORT_KEY, String.valueOf(CLIENT_API_PORT_DEFAULT)));
  }

  public String getOjdbcJarName() {
	return properties.getProperty(OJDBC_JAR_NAME_KEY, OJDBC_JAR_NAME_DEFAULT);
  }

  public String getJavaHome() {
    return properties.getProperty(JAVA_HOME_KEY);
  }

  public String getJDKName() {
    return properties.getProperty(JDK_NAME_KEY);
  }

  public String getJCEName() {
    return properties.getProperty(JCE_NAME_KEY);
  }

  public String getServerDBName() {
	return properties.getProperty(SERVER_DB_NAME_KEY, SERVER_DB_NAME_DEFAULT);
  }

  public String getMySQLJarName() {
	return properties.getProperty(MYSQL_JAR_NAME_KEY, MYSQL_JAR_NAME_DEFAULT);
  }

  public JPATableGenerationStrategy getJPATableGenerationStrategy() {
    return JPATableGenerationStrategy.fromString(System.getProperty(SERVER_JDBC_GENERATE_TABLES_KEY));
  }

  public int getConnectionMaxIdleTime() {
    return Integer.parseInt(properties.getProperty
            (SERVER_CONNECTION_MAX_IDLE_TIME, String.valueOf("900000")));
  }

  /**
   * @return the name to be used for audit information if there is no
   * logged-in user.  Default is '_anonymous'.
   */
  public String getAnonymousAuditName() {
    return properties.getProperty(ANONYMOUS_AUDIT_NAME_KEY, "_anonymous");
  }

  public boolean isMasterKeyPersisted() {
    String masterKeyLocation = getMasterKeyLocation();
    File f = new File(masterKeyLocation);
    return f.exists();
  }

  public String getMasterKeyLocation() {
    String defaultDir = properties.getProperty(MASTER_KEY_LOCATION,
      properties.getProperty(SRVR_KSTR_DIR_KEY, SRVR_KSTR_DIR_DEFAULT));
    return defaultDir + File.separator + MASTER_KEY_FILENAME_DEFAULT;
  }

  public String getSrvrDisabledCiphers() {
    String disabledCiphers = properties.getProperty(SRVR_DISABLED_CIPHERS,
            properties.getProperty(SRVR_DISABLED_CIPHERS, SRVR_DISABLED_CIPHERS_DEFAULT));
    return disabledCiphers.trim();
  }

  public String getSrvrDisabledProtocols() {
    String disabledProtocols = properties.getProperty(SRVR_DISABLED_PROTOCOLS,
            properties.getProperty(SRVR_DISABLED_PROTOCOLS, SRVR_DISABLED_PROTOCOLS_DEFAULT));
    return disabledProtocols.trim();
  }

  public int getOneWayAuthPort() {
    return Integer.parseInt(properties.getProperty(SRVR_ONE_WAY_SSL_PORT_KEY, String.valueOf(SRVR_ONE_WAY_SSL_PORT_DEFAULT)));
  }

  public int getTwoWayAuthPort() {
    return Integer.parseInt(properties.getProperty(SRVR_TWO_WAY_SSL_PORT_KEY, String.valueOf(SRVR_TWO_WAY_SSL_PORT_DEFAULT)));
  }

  /**
   * @return custom properties for database connections
   */
  public Map<String,String> getDatabaseCustomProperties() {
    if (null != customDbProperties) {
      return customDbProperties;
    }

    customDbProperties = new HashMap<String, String>();

    for (Entry<Object, Object> entry : properties.entrySet()) {
      String key = entry.getKey().toString();
      String val = entry.getValue().toString();
      if (key.startsWith(SERVER_JDBC_PROPERTIES_PREFIX)) {
        customDbProperties.put(key.substring(SERVER_JDBC_PROPERTIES_PREFIX.length()), val);
      }
    }

    return customDbProperties;
  }

  public Map<String, String> getAmbariProperties() {

    Properties properties = readConfigFile();
    Map<String, String> ambariPropertiesMap = new HashMap<String, String>();

    for(String key : properties.stringPropertyNames()) {
      ambariPropertiesMap.put(key, properties.getProperty(key));
    }
    return ambariPropertiesMap;
  }

  public long getExecutionCommandsCacheSize() {
    String stringValue = properties.getProperty(SERVER_EC_CACHE_SIZE);
    long value = SERVER_EC_CACHE_SIZE_DEFAULT;
    if (stringValue != null) {
      try {
        value = Long.valueOf(stringValue);
      } catch (NumberFormatException ignored) {
      }

    }

    return value;
  }

  /**
   * @return whether staleConfig's flag is cached.
   */
  public boolean isStaleConfigCacheEnabled() {
    String stringValue =
      properties.getProperty(SERVER_STALE_CONFIG_CACHE_ENABLED_KEY,
        SERVER_STALE_CONFIG_CACHE_ENABLED_DEFAULT);
    return "true".equalsIgnoreCase(stringValue);
  }

  /**
   * @return a string array of suffixes used to validate repo URLs.
   */
  public String[] getRepoValidationSuffixes(String osFamily) {
    String repoSuffixes;

    if(osFamily.equals(UBUNTU_OS)) {
      repoSuffixes = properties.getProperty(REPO_SUFFIX_KEY_UBUNTU,
          REPO_SUFFIX_UBUNTU);
    } else {
      repoSuffixes = properties.getProperty(REPO_SUFFIX_KEY_DEFAULT,
          REPO_SUFFIX_DEFAULT);
    }

    return repoSuffixes.split(",");
  }

  public String isExecutionSchedulerClusterd() {
    return properties.getProperty(EXECUTION_SCHEDULER_CLUSTERED, "false");
  }

  public String getExecutionSchedulerThreads() {
    return properties.getProperty(EXECUTION_SCHEDULER_THREADS,
        DEFAULT_SCHEDULER_THREAD_COUNT);
  }

  public Integer getRequestReadTimeout() {
    return Integer.parseInt(properties.getProperty(REQUEST_READ_TIMEOUT,
        REQUEST_READ_TIMEOUT_DEFAULT));
  }

  public Integer getRequestConnectTimeout() {
    return Integer.parseInt(properties.getProperty(REQUEST_CONNECT_TIMEOUT,
        REQUEST_CONNECT_TIMEOUT_DEFAULT));
  }

  public String getExecutionSchedulerConnections() {
    return properties.getProperty(EXECUTION_SCHEDULER_CONNECTIONS,
        DEFAULT_SCHEDULER_MAX_CONNECTIONS);
  }

  public Long getExecutionSchedulerMisfireToleration() {
    String limit = properties.getProperty
      (EXECUTION_SCHEDULER_MISFIRE_TOLERATION,
        DEFAULT_EXECUTION_SCHEDULER_MISFIRE_TOLERATION);
    return Long.parseLong(limit);
  }

  public Integer getExecutionSchedulerStartDelay() {
    String delay = properties.getProperty(EXECUTION_SCHEDULER_START_DELAY,
        DEFAULT_SCHEDULER_START_DELAY_SECONDS);
    return Integer.parseInt(delay);
  }

  public Integer getExternalScriptTimeout() {
    return Integer.parseInt(properties.getProperty(EXTERNAL_SCRIPT_TIMEOUT_KEY, EXTERNAL_SCRIPT_TIMEOUT_DEFAULT));
  }

  public boolean getParallelStageExecution() {
    return "true".equalsIgnoreCase(configsMap.get(PARALLEL_STAGE_EXECUTION_KEY));
  }

  public String getCustomActionDefinitionPath() {
    return properties.getProperty(CUSTOM_ACTION_DEFINITION_KEY,
        CUSTOM_ACTION_DEFINITION_DEF_VALUE);
  }

  /**
   * @param isPackageInstallationTask true, if task is for installing packages
   * @return default task timeout in seconds (string representation). This value
   *         is used at python (agent) code.
   */
  public String getDefaultAgentTaskTimeout(boolean isPackageInstallationTask) {
    String key = isPackageInstallationTask ? AGENT_PACKAGE_INSTALL_TASK_TIMEOUT_KEY : AGENT_TASK_TIMEOUT_KEY;
    String defaultValue = isPackageInstallationTask ? AGENT_PACKAGE_INSTALL_TASK_TIMEOUT_DEFAULT : AGENT_TASK_TIMEOUT_DEFAULT;
    String value = properties.getProperty(key, defaultValue);
    if (StringUtils.isNumeric(value)) {
      return value;
    } else {
      LOG.warn(String.format("Value of %s (%s) should be a number, " +
          "falling back to default value (%s)",
          key, value, defaultValue));
      return defaultValue;
    }
  }

  public String getResourceDirPath() {
    return properties.getProperty(RESOURCES_DIR_KEY, RESOURCES_DIR_DEFAULT);
  }

  public String getSharedResourcesDirPath(){
      return properties.getProperty(SHARED_RESOURCES_DIR_KEY, SHARED_RESOURCES_DIR_DEFAULT);
  }

  public String getServerJDBCPostgresSchemaName() {
    return properties.getProperty(SERVER_JDBC_POSTGRES_SCHEMA_NAME, "");
  }

  /**
   * @return max thread pool size for clients, default 25
   */
  public int getClientThreadPoolSize() {
    return Integer.parseInt(properties.getProperty(
        CLIENT_THREADPOOL_SIZE_KEY, String.valueOf(CLIENT_THREADPOOL_SIZE_DEFAULT)));
  }

  /**
   * @return max thread pool size for agents, default 25
   */
  public int getAgentThreadPoolSize() {
    return Integer.parseInt(properties.getProperty(
        AGENT_THREADPOOL_SIZE_KEY, String.valueOf(AGENT_THREADPOOL_SIZE_DEFAULT)));
  }

  /**
   * Get the view extraction thread pool max size.
   *
   * @return the view extraction thread pool max size
   */
  public int getViewExtractionThreadPoolMaxSize() {
    return Integer.parseInt(properties.getProperty(
        VIEW_EXTRACTION_THREADPOOL_MAX_SIZE_KEY, String.valueOf(VIEW_EXTRACTION_THREADPOOL_MAX_SIZE_DEFAULT)));
  }

  /**
   * Get the view extraction thread pool core size.
   *
   * @return the view extraction thread pool core size
   */
  public int getViewExtractionThreadPoolCoreSize() {
    return Integer.parseInt(properties.getProperty(
        VIEW_EXTRACTION_THREADPOOL_CORE_SIZE_KEY, String.valueOf(VIEW_EXTRACTION_THREADPOOL_CORE_SIZE_DEFAULT)));
  }

  /**
   * Get the view extraction thread pool timeout.
   *
   * @return the view extraction thread pool timeout
   */
  public long getViewExtractionThreadPoolTimeout() {
    return Long.parseLong(properties.getProperty(
        VIEW_EXTRACTION_THREADPOOL_TIMEOUT_KEY, String.valueOf(VIEW_EXTRACTION_THREADPOOL_TIMEOUT_DEFAULT)));
  }

  /**
   * Gets the inactivity timeout value, in seconds, for sessions created in
   * Jetty by Spring Security. Without this timeout value, each request to the
   * REST APIs will create new sessions that are never reaped since their
   * default time is -1.
   *
   * @return the time value or {@code 1800} seconds for default.
   */
  public int getHttpSessionInactiveTimeout() {
    return Integer.parseInt(properties.getProperty(
        SERVER_HTTP_SESSION_INACTIVE_TIMEOUT,
        "1800"));
  }

  /**
   * Gets the location of the XML alert template file which contains the
   * velocity templates for outbound notifications.
   *
   * @return the location of the template file, or {@code null} if not defined.
   */
  public String getAlertTemplateFile() {
    return properties.getProperty(ALERT_TEMPLATE_FILE);
  }

  /**
   * Gets the default KDC port to use when no port is specified in KDC hostname
   *
   * @return the default KDC port to use.
   */
  public String getDefaultKdcPort() {
    return properties.getProperty(KDC_PORT_KEY, KDC_PORT_KEY_DEFAULT);
  }

  /**
   * Gets the inactivity timeout value, in milliseconds, for socket connection
   * made to KDC Server for its reachability verification.
   *
   * @return the timeout value as configured in {@code tbds.properties}
   * 				 or {@code 10000 ms} for default.
   */
  public int getKdcConnectionCheckTimeout() {
    return Integer.parseInt(properties.getProperty(
        KDC_CONNECTION_CHECK_TIMEOUT_KEY, KDC_CONNECTION_CHECK_TIMEOUT_DEFAULT));
  }

  /**
   * Gets the directory where Ambari is to store cached keytab files.
   *
   * @return a File containing the path to the directory to use to store cached keytab files
   */
  public File getKerberosKeytabCacheDir() {
    String fileName = properties.getProperty(KERBEROS_KEYTAB_CACHE_DIR_KEY, KERBEROS_KEYTAB_CACHE_DIR_DEFAULT);
    return new File(fileName);
  }

  /**
   * Gets the type of database by examining the {@link #getDatabaseUrl()} JDBC
   * URL.
   *
   * @return the database type (never {@code null}).
   * @throws RuntimeException
   *           if there no known database type.
   */
  public DatabaseType getDatabaseType() {
    String dbUrl = getDatabaseUrl();
    DatabaseType databaseType;

    if (dbUrl.contains(DatabaseType.POSTGRES.getName())) {
      databaseType = DatabaseType.POSTGRES;
    } else if (dbUrl.contains(DatabaseType.ORACLE.getName())) {
      databaseType = DatabaseType.ORACLE;
    } else if (dbUrl.contains(DatabaseType.MYSQL.getName())) {
      databaseType = DatabaseType.MYSQL;
    } else if (dbUrl.contains(DatabaseType.DERBY.getName())) {
      databaseType = DatabaseType.DERBY;
    } else {
      throw new RuntimeException(
          "The database type could be not determined from the JDBC URL "
              + dbUrl);
    }

    return databaseType;
  }

  /**
   * Gets the type of connection pool that EclipseLink should use.
   *
   * @return default of {@link ConnectionPoolType#INTERNAL}.
   */
  public ConnectionPoolType getConnectionPoolType(){
    String connectionPoolType = properties.getProperty(
        SERVER_JDBC_CONNECTION_POOL, ConnectionPoolType.INTERNAL.getName());

    if (connectionPoolType.equals(ConnectionPoolType.C3P0.getName())) {
      return ConnectionPoolType.C3P0;
    }

    return ConnectionPoolType.INTERNAL;
  }

  /**
   * Gets the minimum number of connections that should always exist in the
   * connection pool.
   *
   * @return default of {@value #DEFAULT_JDBC_POOL_MIN_CONNECTIONS}
   */
  public int getConnectionPoolMinimumSize() {
    return Integer.parseInt(properties.getProperty(
        SERVER_JDBC_CONNECTION_POOL_MIN_SIZE, DEFAULT_JDBC_POOL_MIN_CONNECTIONS));
  }

  /**
   * Gets the maximum number of connections that should even exist in the
   * connection pool.
   *
   * @return default of {@value #DEFAULT_JDBC_POOL_MAX_CONNECTIONS}
   */
  public int getConnectionPoolMaximumSize() {
    return Integer.parseInt(properties.getProperty(
        SERVER_JDBC_CONNECTION_POOL_MAX_SIZE, DEFAULT_JDBC_POOL_MAX_CONNECTIONS));
  }

  /**
   * Gets the maximum amount of time in seconds any connection, whether its been
   * idle or active, should even be in the pool. This will terminate the
   * connection after the expiration age and force new connections to be opened.
   *
   * @return default of {@value #DEFAULT_JDBC_POOL_MAX_AGE_SECONDS}
   */
  public int getConnectionPoolMaximumAge() {
    return Integer.parseInt(properties.getProperty(
        SERVER_JDBC_CONNECTION_POOL_MAX_AGE, DEFAULT_JDBC_POOL_MAX_AGE_SECONDS));
  }

  /**
   * Gets the maximum amount of time in seconds that an idle connection can
   * remain in the pool. This should always be greater than the value returned
   * from {@link #getConnectionPoolMaximumExcessIdle()}
   *
   * @return default of {@value #DEFAULT_JDBC_POOL_MAX_IDLE_TIME_SECONDS}
   */
  public int getConnectionPoolMaximumIdle() {
    return Integer.parseInt(properties.getProperty(
        SERVER_JDBC_CONNECTION_POOL_MAX_IDLE_TIME,
        DEFAULT_JDBC_POOL_MAX_IDLE_TIME_SECONDS));
  }

  /**
   * Gets the maximum amount of time in seconds that connections beyond the
   * minimum pool size should remain in the pool. This should always be less
   * than than the value returned from {@link #getConnectionPoolMaximumIdle()}
   *
   * @return default of {@value #DEFAULT_JDBC_POOL_EXCESS_MAX_IDLE_TIME_SECONDS}
   */
  public int getConnectionPoolMaximumExcessIdle() {
    return Integer.parseInt(properties.getProperty(
        SERVER_JDBC_CONNECTION_POOL_MAX_IDLE_TIME_EXCESS,
        DEFAULT_JDBC_POOL_EXCESS_MAX_IDLE_TIME_SECONDS));
  }

  /**
   * Gets the number of connections that should be retrieved when the pool size
   * must increase. It's wise to set this higher than 1 since the assumption is
   * that a pool that needs to grow should probably grow by more than 1.
   *
   * @return default of {@value #DEFAULT_JDBC_POOL_ACQUISITION_SIZE}
   */
  public int getConnectionPoolAcquisitionSize() {
    return Integer.parseInt(properties.getProperty(
        SERVER_JDBC_CONNECTION_POOL_AQUISITION_SIZE,
        DEFAULT_JDBC_POOL_ACQUISITION_SIZE));
  }

  /**
   * Gets the number of seconds in between testing each idle connection in the
   * connection pool for validity.
   *
   * @return default of {@value #DEFAULT_JDBC_POOL_IDLE_TEST_INTERVAL}
   */
  public int getConnectionPoolIdleTestInternval() {
    return Integer.parseInt(properties.getProperty(
        SERVER_JDBC_CONNECTION_POOL_IDLE_TEST_INTERVAL,
        DEFAULT_JDBC_POOL_IDLE_TEST_INTERVAL));
  }

}
