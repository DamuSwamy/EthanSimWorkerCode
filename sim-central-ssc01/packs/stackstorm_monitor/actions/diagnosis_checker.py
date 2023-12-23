import requests
import json
from datetime import datetime, timezone, timedelta
from st2common.runners.base_action import Action

class MyCustomStackStormAction(Action):
    def run(self):
        today_date = datetime.now()
        today_date_str = today_date.strftime("%Y-%m-%d")
        ist_offset = timedelta(hours=5, minutes=30)
        start_time = f"{today_date_str}T00:00:00"
        end_time = f"{today_date_str}T23:59:59"

        diagnosis_count = 0

        start_time_utc = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc) - ist_offset
        end_time_utc = datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc) - ist_offset

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
                        start_timestamp = datetime.strptime(start_timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
                        start_timestamp_ist = start_timestamp + ist_offset

                        if start_time_utc <= start_timestamp <= end_time_utc:
                            id = execution["id"]
                            status = execution.get("status")
                            start_time = execution.get("start_timestamp")
                            end_time = execution.get("end_timestamp")
                            state = execution.get("result", {}).get("output", {}).get("output", {}).get("info", {}).get("state", "N/A")
                            ticket_number = execution.get("result", {}).get("output", {}).get("output", {}).get("info", {}).get("info", {}).get("ticket", "N/A")
                            
                            if state.lower() == "diagnosis":
                                diagnosis_count += 1
                                print("Execution_id:", id)
                                print("Action Name:", action_name)
                                print("Execution start time(UTC):", start_time)
                                print("Execution End time(UTC):", end_time)
                                print("Ticket Number", ticket_number)
                else:
                    self.logger.error(f"Request for action {action_name} failed with status code {response.status_code}")
                    self.logger.error("Response content:", response.text)

                if diagnosis_count != 0:
                    self.logger.info("Diagnosis Count: %d", diagnosis_count)
                else:
                    self.logger.info(f"No diagnosis found for {today_date}")

        except Exception as e:
            self.logger.error(f"An error occurred: {e}")

if __name__ == '__main__':
    MyCustomStackStormAction().run()

