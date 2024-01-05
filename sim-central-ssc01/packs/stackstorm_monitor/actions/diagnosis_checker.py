import requests
import json
from datetime import datetime, timezone, timedelta
from st2common.runners.base_action import Action

class MyCustomStackStormAction(Action):
    def run(self):
        today_date = datetime.now(timezone.utc)
        today_date_ist = today_date + timedelta(hours=5, minutes=30)
        yesterday_9_30_am_ist = today_date_ist.replace(hour=9, minute=30, second=0, microsecond=0) - timedelta(days=1)
        today_9_30_am_ist = today_date_ist.replace(hour=9, minute=30, second=0, microsecond=0)

        diagnosis_count = 0

        action_names_to_fetch = ["sim_core.catch_all_automation_create_user", "sim_core.catch_all_automation_v2"]

        base_url = "https://sim-central.sim.esecure.systems/api/v1/executions?"

        headers = {
            "content_type": "application/json",
            "st2-api-key": "MTc3MjBjODg1YjUwZDM2NzM2OGFkNjBkMjE0NWIxOWVkYTBmMThlZWY0ODUwMTcwYzQzNzJlZDcwYTIzYzAwYQ",
        }

        try:
            for action_name in action_names_to_fetch:
                url = base_url + f"action={action_name}"

                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    data = json.loads(response.text)

                    for execution in data:
                        start_timestamp_str = execution.get("start_timestamp", "")
                        end_timestamp_str = execution.get("end_timestamp", "")

                        if start_timestamp_str and end_timestamp_str:
                            start_timestamp = datetime.strptime(start_timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
                            start_timestamp_ist = start_timestamp + timedelta(hours=5, minutes=30)

                            end_timestamp = datetime.strptime(end_timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
                            end_timestamp_ist = end_timestamp + timedelta(hours=5, minutes=30)

                            if yesterday_9_30_am_ist <= start_timestamp_ist <= today_9_30_am_ist:
                                id = execution["id"]
                                status = execution.get("status")
                                start_time = start_timestamp_ist.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                                end_time = end_timestamp_ist.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

                                state = execution.get("result", {}).get("output", {}).get("output", {}).get("info", {}).get("state", "N/A")
                                ticket_number = execution.get("result", {}).get("output", {}).get("output", {}).get("info", {}).get("info", {}).get("ticket", "N/A")

                                if state.lower() == "diagnosis":
                                    diagnosis_count += 1
                                    print("Execution_id:", id)
                                    print("Action Name:", action_name)
                                    print("Execution start time(IST):", start_time)
                                    print("Execution End time(IST):", end_time)
                                    print("Ticket Number", ticket_number)
                else:
                    print(f"Request for action {action_name} failed with status code {response.status_code}")
                    print("Response content:", response.text)

            if diagnosis_count != 0:
                print("Diagnosis Count:", diagnosis_count)
            else:
                print(f"No diagnosis found between {yesterday_9_30_am_ist} and {today_9_30_am_ist}")

        except Exception as e:
            print(f"An error occurred: {e}")

