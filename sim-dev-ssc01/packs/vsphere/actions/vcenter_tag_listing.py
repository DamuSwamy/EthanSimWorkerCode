# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from vmwarelib.actions import BaseAction


class vCenterTagListing(BaseAction):
    def run(self, vsphere, vcenter_id):
        """
        Connect to the REST API and retrieve a list of objects with a given tag category

        Args:
        - kwargs: inputs to the aciton
          - category_id: Name of the tag category
          - tag_list: Name of the tag in VMWare
          - vsphere: Pre-configured vsphere connection details (config.yaml)

        Returns:
        - list: List of objects that are tagged with a given value
        """
        self.connect_rest(vsphere)
        category_list = self.tagging.category_list()
        category_obj_array = []
        result_obj = {}
        for category_id in category_list:
            category = self.tagging.category_get(category_id)
            category_obj = {}
            category_obj['id']          = category['id']
            category_obj['name']        = category['name']
            category_obj['description'] = category['description']
            category_obj['tags']        = {}
            category_obj['vCenterID']   = vcenter_id
            tag_list = self.tagging.tag_list(category_id)
            tag_obj_array = []
            for tag_id in tag_list: 
                tag = self.tagging.tag_get(tag_id)
                tag_objects = self.tagging.tag_association_list_attached_objects(tag_id)
                tag_obj_array.append(self.transform(tag, tag_objects))
            category_obj['tags']['tag'] = tag_obj_array
            category_obj_array.append(category_obj)
        result_obj['category'] = category_obj_array
        return result_obj

    def transform(self, tag_info, tag_objects):
        tag = {}
        tag['tagID']              = tag_info['id']
        tag['tagName']            = tag_info['name']
        tag['tagDescription']     = tag_info['description']
        tag['categoryID']         = tag_info['category_id']
        tagDatastore              = []
        tagVM                     = []
        for obj in tag_objects:
            if obj['type'] == 'Datastore':
                tagDatastore.append(obj['id'])
            if obj['type'] == 'VirtualMachine':
                tagVM.append(obj['id'])
        if len(tagDatastore) > 0:
            tag['tagDatastores'] = {}
            tag['tagDatastores']['tagDatastore'] = tagDatastore 

        if len(tagVM) > 0:
            tag['tagVMs']= {}
            tag['tagVMs']['tagVM'] = tagVM
        return tag
