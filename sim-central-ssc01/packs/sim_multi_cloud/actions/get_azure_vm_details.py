import json
import csv
import requests
import base64
from st2common.runners.base_action import Action
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the InsecureRequestWarning, leave other warnings unaffected
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class get_vm_details_azure(Action):
    def run(self,bearer_token):
                url="https://management.azure.com/subscriptions/d3579ae4-1dca-4e24-afe7-6863931f0b3e/providers/Microsoft.Compute/virtualMachines?api-version=2021-03-01"
                bearer_token = bearer_token.replace('\n', '').replace('\r', '') 
                headers = {
                'Authorization': f'Bearer {bearer_token}'
                }
                all_vm=requests.get(url,headers=headers,verify=False)
                with  open("/opt/stackstorm/packs/device42/actions/azure.json", "wb") as filee:
        # Write the response content to the file
                    filee.write(all_vm.content)

                print(all_vm)
