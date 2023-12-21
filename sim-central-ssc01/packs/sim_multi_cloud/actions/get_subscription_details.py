import json
import csv
import requests
import base64
from st2common.runners.base_action import Action
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the InsecureRequestWarning, leave other warnings unaffected
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class get_subsciption_details_azure(Action):
    def run(self,bearer_token):
                url="https://management.azure.com/subscriptions?api-version=2023-07-01"
                bearer_token = bearer_token.replace('\n', '').replace('\r', '')
                headers = {
                'Authorization': f'Bearer {bearer_token}'
                }
                all_subscriptions = requests.get(url,headers=headers,verify=False)
                with open("/opt/stackstorm/packs/sim_multi_cloud/actions/subscription_details", "wb") as filee:
        # Write the response content to the file
                    filee.write(all_subscriptions.content)
                print("Subscription details")
                print(all_subscriptions.text)

