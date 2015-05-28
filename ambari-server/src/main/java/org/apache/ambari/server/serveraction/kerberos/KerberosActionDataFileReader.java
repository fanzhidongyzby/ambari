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

package org.apache.ambari.server.serveraction.kerberos;

import java.io.File;
import java.io.IOException;

/**
 * KerberosActionDataFileReader is an implementation of a KerberosActionDataFile that is used to
 * read existing KerberosActionDataFiles.
 * <p/>
 * This class encapsulates a {@link org.apache.commons.csv.CSVParser} to read a CSV-formatted file.
 */
public class KerberosActionDataFileReader extends AbstractKerberosDataFileReader {

  /**
   * Creates a new KerberosActionDataFileReader
   * <p/>
   * The file is opened upon creation, so there is no need to manually open it unless manually
   * closed before using.
   *
   * @param file a File declaring where to write the data
   * @throws IOException
   */
  public KerberosActionDataFileReader(File file) throws IOException {
    super(file);
  }
}
