/*
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
package org.apache.ambari.server.api.rest;

import static org.easymock.EasyMock.createStrictMock;
import static org.easymock.EasyMock.expect;
import static org.easymock.EasyMock.replay;
import static org.easymock.EasyMock.verify;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.SocketException;
import java.util.Properties;

import org.apache.ambari.server.KdcServerConnectionVerification;
import org.apache.ambari.server.configuration.Configuration;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.apache.directory.kerberos.client.KdcConfig;
import org.apache.directory.kerberos.client.KdcConnection;
import org.apache.directory.kerberos.client.TgTicket;
import org.apache.directory.shared.kerberos.exceptions.ErrorType;
import org.apache.directory.shared.kerberos.exceptions.KerberosException;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import org.springframework.test.annotation.ExpectedException;


/**
 * Test for {@link KdcServerConnectionVerification}
 */
public class KdcServerConnectionVerificationTest  {

  private static Log LOG = LogFactory.getLog(KdcServerConnectionVerificationTest.class);

  private KdcServerConnectionVerification kdcConnectionVerifier;
  private Properties configProps;
  private Configuration configuration;

  private static ServerSocket serverSocket = null;
  private static boolean serverStop = false;

  private static final int KDC_TEST_PORT = 8090;
  // Some dummy port to test a non-listening KDC server
  private static final int DUMMY_KDC_PORT = 11234;

  @BeforeClass
  public static void beforeClass() throws Exception {
    createSocketServer(KDC_TEST_PORT);
  }

  @AfterClass
  public static void afterClass() throws Exception {
    closeServerSocket();
  }
  
  @Before
  public void before() throws Exception {
    configProps = new Properties();
    configProps.setProperty(Configuration.KDC_PORT_KEY, Integer.toString(KDC_TEST_PORT));
    configuration = new Configuration(configProps);
    kdcConnectionVerifier = new KdcServerConnectionVerification(configuration);     
  }

  @Test
  public void testWithPortSuccess() throws Exception {
    assertTrue(kdcConnectionVerifier.isKdcReachable(String.format("localhost:%d", KDC_TEST_PORT)));
  }

  @Test
  public void testWithoutPortSuccess() throws Exception {
    assertTrue(kdcConnectionVerifier.isKdcReachable("localhost"));
  }

  @Test
  public void testWithoutPortFailure() throws Exception {
    // Assumption: test machine has no KDC so nothing listening on port DUMMY_KDC_PORT
    configProps.setProperty(Configuration.KDC_PORT_KEY, Integer.toString(DUMMY_KDC_PORT));
    assertFalse(kdcConnectionVerifier.isKdcReachable("localhost"));
  }

  @Test
  public void testWithPortFailure() throws Exception {
    assertFalse(kdcConnectionVerifier.isKdcReachable("localhost:8091"));
  }


  @Test
  @ExpectedException(NumberFormatException.class)
  public void testPortParsingFailure() throws Exception {
    assertFalse(kdcConnectionVerifier.isKdcReachable("localhost:abc"));
  }

  @Test
  public void testValidateUDP__Successful() throws Exception {
    KdcConnection connection = createStrictMock(KdcConnection.class);

    expect(connection.getTgt("noUser@noRealm", "noPassword")).andReturn(null).once();
    replay(connection);

    TestKdcServerConnectionVerification kdcConnVerifier =
        new TestKdcServerConnectionVerification(configuration, connection);

    boolean result = kdcConnVerifier.isKdcReachableViaUDP("test-host", 11111);
    assertTrue(result);

    KdcConfig kdcConfig = kdcConnVerifier.getConfigUsedInConnectionCreation();
    assertTrue(kdcConfig.isUseUdp());
    assertEquals("test-host", kdcConfig.getHostName());
    assertEquals(11111, kdcConfig.getKdcPort());
    assertEquals(10 * 1000, kdcConfig.getTimeout());

    verify(connection);
  }

  @Test
  public void testValidateUDP__Successful2() throws Exception {
    KdcConnection connection = createStrictMock(KdcConnection.class);

    expect(connection.getTgt("noUser@noRealm", "noPassword")).andThrow(
        new KerberosException(ErrorType.KDC_ERR_C_PRINCIPAL_UNKNOWN));
    replay(connection);

    TestKdcServerConnectionVerification kdcConnVerifier =
        new TestKdcServerConnectionVerification(configuration, connection);

    boolean result = kdcConnVerifier.isKdcReachableViaUDP("test-host", 11111);
    assertTrue(result);

    KdcConfig kdcConfig = kdcConnVerifier.getConfigUsedInConnectionCreation();
    assertTrue(kdcConfig.isUseUdp());
    assertEquals("test-host", kdcConfig.getHostName());
    assertEquals(11111, kdcConfig.getKdcPort());
    assertEquals(10 * 1000, kdcConfig.getTimeout());

    verify(connection);
  }

  @Test
  public void testValidateUDP__Fail_UnknownException() throws Exception {
    KdcConnection connection = createStrictMock(KdcConnection.class);

    expect(connection.getTgt("noUser@noRealm", "noPassword")).andThrow(
        new RuntimeException("This is a really bad exception"));
    replay(connection);

    TestKdcServerConnectionVerification kdcConnVerifier =
        new TestKdcServerConnectionVerification(configuration, connection);

    boolean result = kdcConnVerifier.isKdcReachableViaUDP("test-host", 11111);
    assertFalse(result);

    KdcConfig kdcConfig = kdcConnVerifier.getConfigUsedInConnectionCreation();
    assertTrue(kdcConfig.isUseUdp());
    assertEquals("test-host", kdcConfig.getHostName());
    assertEquals(11111, kdcConfig.getKdcPort());
    assertEquals(10 * 1000, kdcConfig.getTimeout());

    verify(connection);
  }

  @Test
  public void testValidateUDP__Fail_Timeout() throws Exception {
    int timeout = 1;
    KdcConnection connection = new BlockingKdcConnection(null);

    TestKdcServerConnectionVerification kdcConnVerifier =
        new TestKdcServerConnectionVerification(configuration, connection);

    kdcConnVerifier.setUdpTimeout(timeout);

    boolean result = kdcConnVerifier.isKdcReachableViaUDP("test-host", 11111);
    assertFalse(result);

    KdcConfig kdcConfig = kdcConnVerifier.getConfigUsedInConnectionCreation();
    assertTrue(kdcConfig.isUseUdp());
    assertEquals("test-host", kdcConfig.getHostName());
    assertEquals(11111, kdcConfig.getKdcPort());
    assertEquals(timeout * 1000, kdcConfig.getTimeout());
  }

  @Test
  public void testValidateUDP__Fail_TimeoutErrorCode() throws Exception {
    KdcConnection connection = createStrictMock(KdcConnection.class);

    expect(connection.getTgt("noUser@noRealm", "noPassword")).andThrow(
        new KerberosException(ErrorType.KRB_ERR_GENERIC, "TimeOut occurred"));
    replay(connection);

    TestKdcServerConnectionVerification kdcConnVerifier =
        new TestKdcServerConnectionVerification(configuration, connection);

    boolean result = kdcConnVerifier.isKdcReachableViaUDP("test-host", 11111);
    assertFalse(result);

    KdcConfig kdcConfig = kdcConnVerifier.getConfigUsedInConnectionCreation();
    assertTrue(kdcConfig.isUseUdp());
    assertEquals("test-host", kdcConfig.getHostName());
    assertEquals(11111, kdcConfig.getKdcPort());
    assertEquals(10 * 1000, kdcConfig.getTimeout());

    verify(connection);
  }

  @Test
  public void testValidateUDP__Fail_GeneralErrorCode_NotTimeout() throws Exception {
    KdcConnection connection = createStrictMock(KdcConnection.class);

    expect(connection.getTgt("noUser@noRealm", "noPassword")).andThrow(
        new KerberosException(ErrorType.KRB_ERR_GENERIC, "foo"));
    replay(connection);

    TestKdcServerConnectionVerification kdcConnVerifier =
        new TestKdcServerConnectionVerification(configuration, connection);

    boolean result = kdcConnVerifier.isKdcReachableViaUDP("test-host", 11111);
    assertTrue(result);

    KdcConfig kdcConfig = kdcConnVerifier.getConfigUsedInConnectionCreation();
    assertTrue(kdcConfig.isUseUdp());
    assertEquals("test-host", kdcConfig.getHostName());
    assertEquals(11111, kdcConfig.getKdcPort());
    assertEquals(10 * 1000, kdcConfig.getTimeout());

    verify(connection);
  }


  /**
   * Socket server for test
   * We need a separate thread as accept() is a blocking call
   */
  private static class SocketThread extends Thread {
    public void run() {
      while (serverSocket != null && !serverStop) {
        try {
          serverSocket.accept();
        } catch (SocketException se) {
          LOG.debug("SocketException during tearDown. Can be safely ignored");
        } catch (IOException e) {
          LOG.error("Unexpected exception while accepting connection request");
        }
      }

    }
  }

  private static void createSocketServer(int port) throws Exception {
    serverSocket = new ServerSocket(port);
    new SocketThread().start();
  }

  private static void closeServerSocket() throws Exception {
    serverStop = true;
    try{
      serverSocket.close();
    } catch (IOException ioe) {
      LOG.debug("IOException during tearDown. Can be safely ignored");
    }
  }

  // Test implementation which allows a mock KDC connection to be used.
  private static class TestKdcServerConnectionVerification extends KdcServerConnectionVerification {
    private KdcConnection connection;
    private KdcConfig kdcConfig = null;

    public TestKdcServerConnectionVerification(Configuration config, KdcConnection connectionMock) {
      super(config);
      connection = connectionMock;
    }

    @Override
    protected KdcConnection getKdcUdpConnection(KdcConfig config) {
      kdcConfig = config;
      return connection;
    }

    public KdcConfig getConfigUsedInConnectionCreation() {
      return kdcConfig;
    }
  }

  /**
   * Test implementation which blocks on getTgt() for 60 seconds to facilitate timeout testing.
   */
  private static class BlockingKdcConnection extends KdcConnection {

    public BlockingKdcConnection(KdcConfig config) {
      super(config);
    }

    @Override
    public TgTicket getTgt(String principal, String password) throws Exception {
      // although it is generally a bad idea to use sleep in a unit test for a
      // timing mechanism, this is being used to simulate a timeout and should be
      // generally safe as we are not relying on this for timing other than expecting
      // that this will block longer than the timeout set on the connection validator
      // which should be set to 1 second when using this implementation.
      // We will only block the full 60 seconds in the case of a specific test failure
      // where the callable doesn't properly set the timeout on the get.
      Thread.sleep(60000);
      return null;
    }
  }
}
