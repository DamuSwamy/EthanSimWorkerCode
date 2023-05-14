# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from vmwarelib import inventory
from vmwarelib import checkinputs
from vmwarelib.actions import BaseAction
from vmwarelib.serialize import ResourcePoolGetJSONEncoder
from pyVmomi import vim  # pylint: disable-msg=E0611
import json


class GetResourcePool(BaseAction):
    def run(self, resource_pool_ids, resource_pool_names, get_all_resource_pool, vsphere=None):
        """
        Retrieve MOID of the virtual machine's containing resource pool

        Args:
        - resource_pool_ids: Moid of RP to retrieve
        - resource_pool_names: Name of RP to retrieve
        - vsphere: Pre-configured vsphere connection details (config.yaml)

        Returns:
        - dict: Resource group details. 
        """

        # check a means of finding the VM has been provided
        self.establish_connection(vsphere)


        if not get_all_resource_pool and not resource_pool_ids and not resource_pool_names:
            raise ValueError("No IDs nor Names provided.")

        self.establish_connection(vsphere)

        results = None
        if get_all_resource_pool:
            results = self.get_all_resource_pools()
        else:
            results = self.get_select_resource_pools(resource_pool_ids, resource_pool_names)

        return results

    def get_select_resource_pools(self, resource_pool_ids, resource_pool_names):
        results = {}
        if resource_pool_ids:
            for hid in resource_pool_ids:
                resource_pool = inventory.get_resource_pool(self.si_content, moid=hid)
                if resource_pool:
                    if host.name not in results:
                        results[host.name] = json.loads(json.dumps(host.summary,
                                                                   cls=HostGetJSONEncoder))
        if resource_pool_names:
            for host in resource_pool_names:
                host = inventory.get_hostsystem(self.si_content, name=host)
                if host:
                    if host.name not in results:
                        results[host.name] = json.loads(json.dumps(host.summary,
                                                                   cls=HostGetJSONEncoder))

        return results

    def get_all_resource_pools(self):
        results_arr = []
        container = inventory.get_managed_entities(self.si_content, vim.ResourcePool)
        for resource_pool in container.view:
            results = {}
            #results[resource_pool.name] = json.loads(json.dumps(resource_pool.summary,
            #                                           cls=ResourcePoolGetJSONEncoder))
            results['rpName']   = resource_pool.name
            results['rpID']     = resource_pool._GetMoId()
            results['rpParent'] =  resource_pool.parent._GetMoId()
            results_arr.append(results)
        return results_arr
