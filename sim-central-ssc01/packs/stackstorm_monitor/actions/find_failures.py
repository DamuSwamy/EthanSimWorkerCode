import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import os
from st2common.runners.base_action import Action
import datetime
 
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
 
class PythonActionProcessData(Action):
    def run(self,List_of_actions_to_ignore,StackStorm_instance_detail):
 
        Stackstorm_server_names_and_Api_key = []
 
        for key, value in StackStorm_instance_detail.items():
            Stackstorm_server_names_and_Api_key.append([key,value])
 
        one_hour_ago = datetime.datetime.utcnow() - datetime.timedelta(hours=4, minutes=5)
        timestamp = one_hour_ago.strftime('%Y-%m-%dT%H:%M:%SZ')
 
        All_action_names = []
        All_errors = []
        All_starttime=[]
        All_executionurl=[]
 
        for Server_name in Stackstorm_server_names_and_Api_key:
            url=f'https://{Server_name[0]}:443/api/v1/executions?status=failed&timestamp_gt={timestamp}'
 
            custom_headers= {
            "St2-Api-Key": Server_name[1]
                }
 
 
            response = requests.get(url,headers=custom_headers, verify=False)
 
            data_list=[]
            if response.status_code == 200:
                data_list = response.json()
 
 
            action_names=[]
            starttime=[]
            errors=[]
            executionurl=[]
            for entry in data_list:
                action = entry.get("action")
 
            # Check if the action name is from the list or not
                if List_of_actions_to_ignore:
                   if action and action.get("name") not in List_of_actions_to_ignore:
                       if entry.get("parent"):
                           pass
                       else:
                           action_names.append(action.get("name"))
                           starttime.append(entry.get("start_timestamp"))
                           executionurl.append(entry.get("web_url"))
                           error = entry.get("result", {}).get("stderr")
                           if error and len(error)>100:
                              errors.append(error[:100])
                           else:
                              errors.append("Explore action to find error")
 
                else:
                    if entry.get("parent"):
                        pass
                    else:
                        action_names.append(action.get("name"))
                        starttime.append(entry.get("start_timestamp"))
                        executionurl.append(entry.get("web_url"))
                        error = entry.get("result", {}).get("stderr")
                        if error and len(error)>100:
                          errors.append(error[:100])
                        else:
                          errors.append("Explore action to find error")
 
            All_action_names.append(action_names)
            All_errors.append(errors)
            All_starttime.append(starttime)
            All_executionurl.append(executionurl)
            # Print the extracted information
        l=0
        for i in All_action_names:
            print("Stackstorm instance name: {}".format(Stackstorm_server_names_and_Api_key[l][0]))
            print("Number of failed task are {}".format(len(i)))
            print("\n")
            for j in range(len(i)):
                print("Action Name: {}".format(i[j]))
                print("Start_time: {}".format(All_starttime[l][j]))
                print("Execution_url: {}".format(All_executionurl[l][j]))
                print("Error: {}".format(All_errors[l][j]))
                print("-----------------------------------------------------------------------------------------------------------------------------\n")
            l=l+1