import os
from st2common.runners.base_action import Action
import re

class GetVMDetails(Action):
    def run(self):
        return {
            "msg":"Getting VM Details"
        }

        