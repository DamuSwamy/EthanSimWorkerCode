import json
import csv
import requests
from st2common.runners.base_action import Action
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the InsecureRequestWarning, leave other warnings unaffected
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class adds_unique_id_to_devices(Action):
    def run(self,dev_42_file,vm_data_file,token):
        d1=[]
        flag=True 
        with open(dev_42_file, 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            # Assuming the second field is the identifier  
            #header = next(csv_reader)
            identifier_index = 1  # Index of the second field
            third_field_index = 2
            d1 = {row[identifier_index]: [row[0], row[third_field_index] if len(row) > third_field_index else None] for row in csv_reader if row[identifier_index]}

        data1=d1
        #print(data1)
        print('\n')
        
        token = token.replace('\n', '').replace('\r', '')
       

        with open(vm_data_file, 'r') as file:
            file_contents = json.load(file)


# Split the file contents into individual JSON objects
        #json_objects = file_contents.strip().split('\n')

        #print(json_objects)
        for json_str in file_contents:
    # Parse JSON string into a Python dictionary
          #  print(json_str)
           # print("-----------------------------------------------")        
            data2=json_str.get("value",[])

    # Access and process the values under the "value" key
            for obj2 in data2:

            # Assume the objects have a unique identifier (e.g., 'name' field)
                identifier2 = obj2.get('properties', {}).get('vmId')
                result={}
                    # Check if the identifier is in the CSV data
                if identifier2.upper() in data1:
                # Process or print the matching fields
                #print(f"Match found for identifier '{identifier2}':")
                #print("Name:", obj2.get('name'))
                    idd=obj2.get('id')
                #print("id:", obj2.get('id'))
                #print("vmId:",identifier2)
                
                    identi=data1[identifier2.upper()][1]
                    #print(identi)
                    if identi!=idd:
                        flag=False
                        result = {
                        "device_id": data1[identifier2.upper()][0],
                        "key": "identifier",
                        "type": "json",
                        "value": idd
                         }
                        result_json_string=json.dumps(result)
                   #print(result_json_string)
                        headers = {
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {token}',
                        'Cookie': 'd42sessnid_csrftoken=WvcEEPtIjtMtH0ADoBSUPGVfMjwWAg82KYiwbyNe5kfipAKQalHjvqfqDYBNDDCZ'
                        }
                        api_endpoint='https://cmdb.ecorp.systems/api/1.0/custom_fields/device/'
                        print("api call")
                        response = requests.put(api_endpoint, headers=headers, data=result_json_string,verify=False)#, headers=headers,verify=False)
                        print(response.text)
                        print("\n")
        if (flag):
            print("Everything is already updated")
