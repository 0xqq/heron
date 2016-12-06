# Copyright 2016 Twitter. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
'''response.py'''
import abc
from collections import namedtuple

from heron.common.src.python.utils.log import Log

class Status:
  Ok, NonUserError, UserError = range(3)

class Response(object):
  def __init__(self, status, succ_msg=None, err_msg=None, debug_msg=None):
    self.status = self.status_type(status)
    self.succ_msg = succ_msg
    self.err_msg = err_msg
    self.debug_msg = debug_msg

  @staticmethod
  def status_type(status_code):
    if status_code == 0:
      return Status.Ok
    elif status_code < 100:
      return Status.NonUserError
    else:
      return Status.UserError

  @abc.abstractmethod
  def render(self):
    pass

class TopologyDefLoadResponse(Response):
  def __init__(self, status=1, defn_file=None, succ_msg=None, err_msg=None, debug_msg=None):
    super(TopologyDefCreationResponse, self).__init__(status, succ_msg, err_msg, debug_msg)
    self.defn_file = defn_file

  def render(self):
    if self.status != Status.Ok:
      if self.err_msg:
        Log.error(self.err_msg)
      else:
        Log.error("Unable to load topology definition file: %s", self.defn_file)
      if self.debug_msg: Log.debug(self.debug_msg)

class InvocationResponse(Response):
  def __init__(self, main_class, topo_type, status, succ_msg, err_msg, debug_msg):
    super(InvocationResponse, self).__init__(status, succ_msg, err_msg, debug_msg)
    self.main_class = main_class
    self.topo_type = topo_type

class TopologyDefCreationResponse(InvocationResponse):
  def __init__(self, topology_file, main_class, topo_type, status, succ_msg, err_msg, debug_msg):
    super(TopologyDefCreationResponse, self).__init__(
      main_class, topo_type, status, succ_msg, err_msg, debug_msg)
    self.topology_file = topology_file

  def render(self):
    if self.status != Status.Ok:
      Log.error("Unable to create %s topology definition file '%s' by invoking'%s'",
        self.topo_type, self.topology_file, self.main_class)
      Log.error(self.debug_msg)

class TopologyLaunchResponse(InvocationResponse):
  def __init__(self, main_class, topo_type, topo_name, status, succ_msg, err_msg, debug_msg):
    super(TopologyLaunchResponse, self).__init__(
      main_class, topo_type, status, succ_msg, err_msg, debug_msg)
    self.topo_name = topo_name

  def render(self):
    if self.status == Status.Ok:
      Log.info("Successfully launched topology '%s'", self.topo_name)
    else:
      Log.error("Failed to launch %s topology '%s'", self.topo_type, self.topo_name)
      if self.status == Status.NonUserError:
        Log.error(self.debug_msg)
      else:
        Log.error(self.err_msg)
        Log.debug(self.debug_msg)

def render(resp):
  if isinstance(resp, list):
    for r in resp:
      r.render()
  elif isinstance(resp, Response):
    resp.render()
  else:
    raise RuntimeError("Unknown response type")

