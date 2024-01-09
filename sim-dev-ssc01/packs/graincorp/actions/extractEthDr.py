from st2common.runners.base_action import Action
import json

class ExtractEthDr(Action):
    def __init__(self, config=None, action_service=None):
        super(ExtractEthDr, self).__init__(config, action_service)

    def run(self):
        
        txt_file_path = '/opt/stackstorm/packs/graincorp/joinccbtociacoutput.txt'
        with open(txt_file_path, 'r') as txt_file:
          json_data = json.load(txt_file)

        join_ccb_to_ciac_output=json_data

        extractethDRObject={
            "VMs":{
                "vm":[

                ]
            }
        }

        arr=[]
        for obj in join_ccb_to_ciac_output:
            if obj["ethDR"]>0:
                temp_obj={}
                temp_obj["Name"]=obj["Name"]
                temp_obj["ethDR"]=obj["ethDR"]
                arr.append(temp_obj)

        extractethDRObject["VMs"]["vm"] = list(arr)


        txt_file_output = "/opt/stackstorm/packs/graincorp/extractEthDRoutput.txt"
        with open(txt_file_output, 'w') as txt_file:
          json.dump(list(arr), txt_file)

        return {
            'data': extractethDRObject
        }