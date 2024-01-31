import json
import csv
import requests
import base64
from st2common.runners.base_action import Action
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the InsecureRequestWarning, leave other warnings unaffected
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class adds_unique_id_to_devices(Action):
    def run(self,username,password,servicenow_hostname):#,dev_42_file,vm_data_file,token):
        idd=[]
        l=[]
        c=0
        csv_file_path="/opt/stackstorm/packs/sim_multi_cloud/actions/dev42_resources"
        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # Skip the header row if it exists

            for row in csv_reader:
        # Assuming the third field is at index 2 (0-indexed)
                identi = row[2]
                idd.append(identi)
        with open("/opt/stackstorm/packs/sim_multi_cloud/actions/service.json", 'r') as file:
            file_contents = json.load(file)
        #print(file_contents)
        Username=username
        Password=password
        headers = {
                "Content-Type": "application/json",
                }
        payload = {
         "operational_status": "6"
        }
        #json_payload=json.dumps(payload)
        for obj in file_contents["result"]:
            short_description = obj.get("short_description")
            company=obj.get("company")
            sys_id=obj.get("sys_id")
            status=obj.get("operational_status")
            name=obj.get("name")
            #print(status)
            if short_description not in idd and company!="" and status!="6":
                url = f"https://{servicenow_hostname}/api/now/table/cmdb_ci/{sys_id}"
                response = requests.patch(url, json=payload, headers=headers, auth=(Username, Password),verify=False)
                if response.status_code == 200:
                    l.append((name,sys_id))
                    c=c+1
                else:
                    print(f"Error: {response.status_code} - {response.text}") 
        if(c):
            print(f"Number of resources updated: {c}")
            print(f"\nList of name, sys_id whose operational_status is updated:\n")
            for i,j in l:
                print(i,j)
        else:
            print("No record updated")





