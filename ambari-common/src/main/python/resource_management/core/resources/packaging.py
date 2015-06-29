#!/usr/bin/env python
"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Ambari Agent

"""

__all__ = ["Package"]

from resource_management.core.base import Resource, ForcedListArgument, ResourceArgument


class Package(Resource):
  action = ForcedListArgument(default="install")
  package_name = ResourceArgument(default=lambda obj: obj.name)
  location = ResourceArgument(default=lambda obj: obj.package_name)

  # Allow using only specific list of repositories when performing action
  use_repos = ResourceArgument(default=[])
  """
  True           -  log it in INFO mode
  False          -  never log it
  None (default) -  log it in DEBUG mode
  """
  logoutput = ResourceArgument(default=None)

  version = ResourceArgument()
  actions = ["install", "upgrade", "remove"]
  build_vars = ForcedListArgument(default=[])