import json
import csv
import requests
import base64
from st2common.runners.base_action import Action
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the InsecureRequestWarning, leave other warnings unaffected
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class get_D42_devices(Action):
    def run(self,bearer_token):
                url="https://cmdb.ecorp.systems/services/data/v1.0/query/"
                sql_query = """
SELECT resource_pk,resource_name,identifier,vendor_resource_type FROM view_resource_v2
WHERE vendor_resource_type IN ('SQL Database', 'SQL Server', 'Azure Function App', 'Log Analytics Workspace', 'Blob Storage Account', 'Server Farm', 'Frontdoor')
"""
                payload = {
                'query': sql_query
                }
                #bearer_token=bearer_token.decode('utf-8') 
                bearer_token = bearer_token.replace('\n', '').replace('\r', '')
                #bearer_token = base64.b64decode(bearer_token.encode()).decode()[:-len("mis@123")]
                #token=bearer_token
                headers = {
                'Authorization': f'Bearer {bearer_token}',
                'Accept': 'application/json'  # Adjust content type based on your API requirements
                }
                data = requests.post(url, headers=headers, data=payload, verify=False)
                with open("/opt/stackstorm/packs/sim_multi_cloud/actions/dev42_resources","wb") as filee:
                    filee.write(data.content)
                #print(data)
                csv_file_path = '/opt/stackstorm/packs/sim_multi_cloud/actions/dev42_resources'

                # Open the CSV file
                with open(csv_file_path, 'r') as file:
                # Create a CSV reader
                    csv_reader = csv.reader(file)
                    total_rows = 0
                    # Iterate through each row in the CSV file
                    access_denied = True
                    for row in csv_reader:
                        # Check if the row has at least two fields
                        
                        if "You don't have permission" in row[0]:
                            access_denied = False
                            print("You do not have access or unable to fetch the data using api")
                            break
                        total_rows += 1

                        if len(row) >= 2:
                            # Print the first and second fields
                            print("resource_pk - ", row[0])
                            print("resource_name - ", row[1])
                            print("\n")
                        else:
                            print("Row does not have enough fields.")
                    if access_denied:
                        print("Total number of resources added - ", total_rows) 
                        print("Details of resources are successfully stored in dev42_resources file\n")

                #file_path = "/opt/stackstorm/packs/sn_integration/actions/dev42"  # Replace with the actual path to your file




