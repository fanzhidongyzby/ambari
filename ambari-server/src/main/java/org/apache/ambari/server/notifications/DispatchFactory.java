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
package org.apache.ambari.server.notifications;

import java.util.HashMap;
import java.util.Map;

import org.apache.ambari.server.notifications.dispatchers.EmailDispatcher;

import com.google.inject.Inject;
import com.google.inject.Injector;
import com.google.inject.Singleton;
import org.apache.ambari.server.notifications.dispatchers.SNMPDispatcher;

/**
 * The {@link DispatchFactory} is used to provide singleton instances of
 * {@link NotificationDispatcher} based on a supplied type.
 */
@Singleton
public class DispatchFactory {

  /**
   * Mapping of dispatch type to dispatcher singleton.
   */
  private final Map<String, NotificationDispatcher> m_dispatchers = new HashMap<String, NotificationDispatcher>();

  /**
   * Constructor.
   *
   */
  @Inject
  public DispatchFactory(Injector injector) {
    EmailDispatcher emailDispatcher = injector.getInstance(EmailDispatcher.class);
    SNMPDispatcher snmpDispatcher = injector.getInstance(SNMPDispatcher.class);
    m_dispatchers.put(emailDispatcher.getType(), emailDispatcher);
    m_dispatchers.put(snmpDispatcher.getType(), snmpDispatcher);
  }

  /**
   * Registers a dispatcher instance with a type.
   *
   * @param type
   *          the type
   * @param dispatcher
   *          the dispatcher to register with the type.
   */
  public void register(String type, NotificationDispatcher dispatcher) {
    if (null == dispatcher) {
      m_dispatchers.remove(type);
    } else {
      m_dispatchers.put(type, dispatcher);
    }
  }

  /**
   * Gets a dispatcher based on the type.
   *
   * @param type
   *          the type (not {@code null}).
   * @return a dispatcher instance, or {@code null} if none.
   */
  public NotificationDispatcher getDispatcher(String type) {
    return m_dispatchers.get(type);
  }
}
