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
        
                bearer_token = bearer_token.replace('\n', '').replace('\r', '') 
                headers = {
                'Authorization': f'Bearer {bearer_token}'
                }
                k=[] 
                with open("opt/stackstorm/packs/sim_multi_cloud/actions/subscription_details", 'r') as file:
                # Load the JSON data
                    json_data = json.load(file)

                # Iterate through each object in the array
                for obj in json_data.get('value', []):
                # Check if the current object has the target ID

                    if 'subscriptionId' in obj:
                        k.append(obj.get('subscriptionId'))

                # If the target ID is not found
                print("List of subscription id \n")
                print(k)
                
                # to empty the file
                with open("/opt/stackstorm/packs/sim_multi_cloud/actions/azure.json", 'wb') as filee:
                    pass
                
                with open("/opt/stackstorm/packs/sim_multi_cloud/actions/azure.json", 'wb') as filee:
            # Add an opening square bracket to start the JSON array
                     filee.write(b'[')



                for i,subscription_id in enumerate(k):
                    url=f'https://management.azure.com/subscriptions/{subscription_id}/providers/Microsoft.Compute/virtualMachines?api-version=2021-03-01'
                    all_vm=requests.get(url,headers=headers,verify=False)
                    with  open("/opt/stackstorm/packs/sim_multi_cloud/actions/azure.json", "ab") as filee:
                # Write the response content to the file
                        if i>0: 
                            filee.write(b',')
                        filee.write(all_vm.content)

                with open("/opt/stackstorm/packs/sim_multi_cloud/actions/azure.json", 'ab') as filee:
                    filee.write(b']')
                #print(all_vm)
                print("\nVM details are added in azure.json file")

