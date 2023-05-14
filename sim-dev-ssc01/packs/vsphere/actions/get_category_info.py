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


class GetCategoryInfo(BaseAction):
    def run(self, category_name, category_id, vsphere):
        """
        Connect to the REST API and retrieve a list of objects with a given tag

        Args:
        - kwargs: inputs to the aciton
          - category_name: Name of the tag category
          - category_id: ID of the tag category in VMWare
          - vsphere: Pre-configured vsphere connection details (config.yaml)

        Returns:
        - list: List of objects that are tagged with a given value
        """
        """if not (category_name and category_id):
            raise ValueError("No Category IDs nor Names provided.")"""

        self.connect_rest(vsphere)

        # Get the category and tag
        if category_name:
            category = self.tagging.category_find_by_name(category_name)

        if category_id:
            category = self.tagging.category_get(category_id)

        return category
