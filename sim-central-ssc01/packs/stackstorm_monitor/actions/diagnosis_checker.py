import requests
import json
from datetime import datetime, timezone, timedelta
from st2common.runners.base_action import Action

class MyCustomStackStormAction(Action):
    def run(self):

        # Get yesterday's date
        yesterday_date = datetime.now() - timedelta(days=1)
        yesterday_date_str = yesterday_date.strftime("%Y-%m-%d")
        today_date = datetime.now()
        today_date_str = today_date.strftime("%Y-%m-%d")

        ist_offset = timedelta(hours=5, minutes=30)
        start_time = f"{yesterday_date_str}T09:30:00"
        end_time = f"{today_date_str}T09:29:59"

        diagnosis_count = 0

        # Convert local time to UTC
        start_time_utc = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc) - ist_offset
        end_time_utc = datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc) - ist_offset

        # Specify action names to fetch
        action_names_to_fetch = ["sim_core.catch_all_automation_create_user", "sim_core.catch_all_automation_v2"]

        base_url = "https://sim-central.sim.esecure.systems/api/v1/executions?"

        headers = {
            "content_type": "application/json",
            "st2-api-key": "MTc3MjBjODg1YjUwZDM2NzM2OGFkNjBkMjE0NWIxOWVkYTBmMThlZWY0ODUwMTcwYzQzNzJlZDcwYTIzYzAwYQ",
        }

        try:
            for action_name in action_names_to_fetch:
                # Construct the updated URL with the current action name and status parameter
                url = base_url + f"action={action_name}&status=succeeded"

                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    data = json.loads(response.text)

                    for execution in data:
                        start_timestamp_str = execution.get("start_timestamp")

                        # Check if start_timestamp_str is not None
                        if start_timestamp_str is not None:
                            # Convert timestamp string to datetime object
                            start_timestamp_utc = datetime.strptime(start_timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ").replace(
                                tzinfo=timezone.utc
                            )

                            # Adjust the start timestamp to IST
                            start_timestamp_ist = start_timestamp_utc + ist_offset

                            # Check if the execution time is within the desired range
                            if start_time_utc <= start_timestamp_ist <= end_time_utc:
                                id = execution["id"]
                                status = execution.get("status", "N/A")
                                end_timestamp_str = execution.get("end_timestamp", "N/A")
                                end_timestamp_utc = datetime.strptime(end_timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ").replace(
                                    tzinfo=timezone.utc
                                )
                                end_timestamp_ist = end_timestamp_utc + ist_offset
                                end_time = end_timestamp_ist.strftime("%Y-%m-%dT%H:%M:%S")

            
                                state = execution.get("result", {}).get("output", {}).get("output", {}).get("info", {}).get(
                                    "state", "N/A"
                                )
                                ticket_number = execution.get("result", {}).get("output", {}).get("output", {}).get("info", {}).get(
                                    "info", {}
                                ).get("ticket", "N/A")

                                if state.lower() == "diagnosis":
                                    diagnosis_count += 1
                                    print("Execution_id:", id)
                                    print("Action Name:", action_name)
                                    print("Execution start time(IST):", start_timestamp_ist.strftime("%Y-%m-%dT%H:%M:%S"))
                                    print("Execution End time(IST):", end_time)
                                    print("Ticket Number", ticket_number)
                                    print("-----------------------------------------")
                else:
                    print(f"Request for action {action_name} failed with status code {response.status_code}")
                    print("Response content:", response.text)

        except Exception as e:
            print(f"An error occurred: {e}")

        if diagnosis_count != 0:
            print("Diagnosis Count:", diagnosis_count)
        else:
            print(f"No diagnosis found from {start_time}")

