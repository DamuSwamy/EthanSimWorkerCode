import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import datetime
from st2common.runners.base_action import Action

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class PythonActionProcessData(Action):
    def run(self, server_name, st2_api_key):
        # Use the provided server_name and st2_api_key
        url = f'https://{server_name}/api/v1/executions?status=succeeded'

        custom_headers = {
            "St2-Api-Key": st2_api_key
        }

        # Instead of reading from file, directly set the action name
        action_names_to_fetch = ["catch_all_automation_create_user","catch_all_automation_v2"]

        one_hour_ago = datetime.datetime.utcnow() - datetime.timedelta(hours=240)
        timestamp = one_hour_ago.strftime('%Y-%m-%dT%H:%M:%SZ')

        response = requests.get(url, headers=custom_headers, verify=False)
        data_list = []
        if response.status_code == 200:
            data_list = response.json()

        # Counter for DIAGNOSIS executions
        diagnosis_count = 0

        for entry in data_list:
            action = entry.get("action")
            if action and action.get("name") in action_names_to_fetch:
                execution_id = entry.get("id")
                execution_url = f'https://{server_name}/api/v1/executions/{execution_id}'

                execution_response = requests.get(execution_url, headers=custom_headers, verify=False)
                execution_data = execution_response.json()

                # Extract relevant information
                action_name = execution_data.get("action").get("name")
                status = execution_data.get("status")
                start_time = execution_data.get("start_timestamp")
                end_time = execution_data.get("end_timestamp")
                output = execution_data.get("result")

                # Additional code to extract and print the "state" value
                try:
                    state_value = output.get("output", {}).get("output", {}).get("info", {}).get("state", {})
                    ticket_number = output.get("output", {}).get("output", {}).get("info", {}).get("info", {}).get("ticket", {})

                    # Case-insensitive comparison for "DIAGNOSIS"
                    if state_value.lower() == "diagnosis":
                        # Increment the counter
                        diagnosis_count += 1

                        print("Action Name: {}".format(action_name))
                        print("Status: {}".format(status))
                        print("Start_time: {}".format(start_time))
                        print("End_time: {}".format(end_time))
                        print("State value:", state_value)
                        print("Ticket_Number: {}".format(ticket_number))
                        print("-----------------------------------------------------------------------------------------------------------------------------")

                except json.JSONDecodeError as e:
                    print("Error decoding JSON:", e)
                except KeyError as e:
                    print("KeyError:", e)
                except Exception as e:
                    print("An unexpected error occurred:", e)

        # Print "No diagnosis found" if diagnosis_count is 0
        print("Total DIAGNOSIS Status Executions:", diagnosis_count)
        if diagnosis_count == 0:
            print("No diagnosis found")
