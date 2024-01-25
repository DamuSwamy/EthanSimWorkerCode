import json
import csv
import requests
import base64
from st2common.runners.base_action import Action
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the InsecureRequestWarning, leave other warnings unaffected
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class get_vm_details_azure(Action):
    def run(self,username,password):
        
                #bearer_token = bearer_token.replace('\n', '').replace('\r', '') 
                #bearer_token = base64.b64decode(bearer_token.encode()).decode()[:-len("mis@123")]
                username=username
                password=password
                headers = {
                'Content-type': 'application/json'
                }
                url="https://ethandev.service-now.com/api/now/table/cmdb_ci?sysparm_query=categoryINSQL Database, SQL Server, Azure Function App,Log Analytics Workspace,Blob Storage Account,Server Farm, Frontdoor"
                all_vm=requests.get(url,headers=headers,auth=(username,password),verify=False)
                content_str = all_vm.content.decode('utf-8')
                all_vm_data = json.loads(content_str)
                with  open("/opt/stackstorm/packs/sim_multi_cloud/actions/service.json", "wb") as filee:
                     filee.write(all_vm.content)

                print("\nDetails are added in service.json file\n")


