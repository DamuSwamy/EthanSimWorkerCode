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
from vmwarelib.actions import BaseAction
from pyVmomi import vim  # pylint: disable-msg=E0611
import json


class GetFolder(BaseAction):
    def run(self, get_all_folders, vsphere=None):
        """
        Retrieve details of folders from vCenter

        Args:
        - vsphere: Pre-configured vsphere connection details (config.yaml)

        Returns:
        - dict: Resource group details. 
        """

        # check a means of finding the VM has been provided
        self.establish_connection(vsphere)


        if not get_all_folders:
            raise ValueError("Please tick the checkbox given.")

        self.establish_connection(vsphere)
        results = self.get_all_folders()

        return results

    def get_all_folders(self):
        results_arr = []
        container = inventory.get_managed_entities(self.si_content, vim.Folder)
        for folder in container.view:
            results = {}
            #results[resource_pool.name] = json.loads(json.dumps(resource_pool.summary,
            #                                           cls=ResourcePoolGetJSONEncoder))
            results['folderName']   = folder.name
            results['folderID']     = folder._GetMoId()
            results['folderParent'] = folder.parent._GetMoId()
            results_arr.append(results)
        return results_arr
