from st2common.runners.base_action import Action
import json

class Uniqueorgs(Action):
    def __init__(self, config=None, action_service=None):
        super(Uniqueorgs, self).__init__(config, action_service)

    def run(self):
        
        txt_file_path = "/opt/stackstorm/packs/sim_graincorp/inputs/joinccbtociacoutput.txt"
        
        try:
            with open(txt_file_path, 'r') as txt_file:
                joinccbtociacout = json.load(txt_file)
            join_ccb_to_ciac_output=joinccbtociacout
        
        except Exception as e:
            print(e)

        unique_orgs = set(item["Org"] for item in join_ccb_to_ciac_output)
        unique_org_array = list(unique_orgs)

        unique_org_object = {
            "Organisations": {
                "Row": [
                    {"Org": org} for org in unique_org_array
                ]
            }
        }
        
        txt_file_output = "/opt/stackstorm/packs/sim_graincorp/inputs/uniqueorgsoutput.txt"
        try:
            with open(txt_file_output, 'w') as txt_file:
                json.dump(unique_org_array, txt_file)
        except Exception as e:
            print(e)
        return {
            'data':unique_org_object
        }
