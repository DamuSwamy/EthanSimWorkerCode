import json
import csv
import requests
import base64
from st2common.runners.base_action import Action
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the InsecureRequestWarning, leave other warnings unaffected
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class GenerateAzureToken(Action):
    def run(self,clieent_id, clieent_secret):

        url="https://login.microsoftonline.com/d0aaafc0-4f56-478a-b986-fd9eb70046d6/oauth2/token"
        #credentials = base64.b64encode(f'{username}:{password}'.encode()).decode()
        #print(credentials)
        headers = {
        #'Authorization': f'Basic {credentials}',
        'Content-Type': 'application/x-www-form-urlencoded',  # Adjust content type based on your API requirements
        'Cookie': 'fpc=AlsdMDjJnHVIqHQE5gnRa_tkMWjLAQAAAFrSC90OAAAA; stsservicecookie=estsfd; x-ms-gateway-slice=estsfd'
        }
        data1={  
                "grant_type": "client_credentials",
                "client_id": f'{clieent_id}',
                "client_secret": f'{clieent_secret}',
                "resource": "https://management.azure.com/"
            }

        response=requests.get(url,headers=headers,data=data1,verify=False)
        response_json=json.loads(response.text)
        #print(response_json)
        access_token = response_json.get('access_token')
        #print("hello")
        access_token=access_token.rstrip()
        print(access_token)

