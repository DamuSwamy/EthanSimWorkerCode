import os
import requests
from st2common.runners.base_action import Action
from st2client.client import Client
from st2client.models import LiveAction

class MavenlinkIntegrationAction(Action):
    def chunk_list(self, lst, chunk_size):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), chunk_size):
            yield lst[i:i + chunk_size]

    def flatten_json(self, json_obj, parent_key='', separator='_'):
        flattened = {}
        for key, value in json_obj.items():
            new_key = f"{parent_key}{separator}{key}" if parent_key else key
            if isinstance(value, dict):
                flattened.update(self.flatten_json(value, new_key, separator))
            else:
                flattened[new_key] = value
        return flattened

    def run(self):
        # APIS
        support_detail_api_url = "https://api.mavenlink.com/api/v1/workspaces?include=custom_field_values&by_custom_choice_value=691435:3305075&per_page=100"
        wsp_id = 0
        time_entries_api_url = f"https://api.mavenlink.com/api/v1/time_entries?include=role,user,workspace,story&workspace_id={wsp_id}&per_page=100"
        
        # Authorization Header
        headers = {'Authorization': 'Bearer 3bd2ef96c036e39236ba5ba1c97e20c7ae3d527a9142559e0e9d3729fd7662bb'}

        # ML_Support_Detail needed Keys
        ML_Support_Detail_Columns = ['title', 'workspaceid', 'status', 'total_expenses_in_cents', 'price_in_cents', 'price', 'percent_budget_used', 'budget_used', 'budget_used_in_cents', 'budget_remaining', 'group', 'client_role_name']

        # Table Names
        SupportDetailsTable = 'ML_Support_Detail'
        TimeEntriesTable = 'ML_Time_Entries'

        # ML_Support_Detail Insert Preparation
        support_details_resp = requests.get(support_detail_api_url, headers=headers)
        support_details_dict = support_details_resp.json()

        workspaces = support_details_dict['workspaces']

        support_detail_insert_statements = []
        workspace_ids = []
        support_details_json_data = []

        for wsp in workspaces:
            workspace_ids.append(wsp)
            flattened_dict = self.flatten_json(workspaces[wsp])
            title = str(flattened_dict['title']).replace("'", "''")
            client_role_name = str(flattened_dict['client_role_name']).replace("'", "''")
            values = {
                "title": title,
                "workspaceid": wsp,
                "status": flattened_dict.get('status', ''),
                "total_expenses_in_cents": flattened_dict.get('total_expenses_in_cents', ''),
                "price_in_cents": flattened_dict.get('price_in_cents', ''),
                "price": flattened_dict.get('price', ''),
                "percent_budget_used": flattened_dict.get('percent_budget_used', ''),
                "budget_used": flattened_dict.get('budget_used', ''),
                "budget_used_in_cents": flattened_dict.get('budget_used_in_cents', ''),
                "budget_remaining": flattened_dict.get('budget_remaining', ''),
                "group": flattened_dict.get('group', ''),
                "client_role_name": client_role_name
            }
            support_details_json_data.append(values)

        self.logger.info(f"Workspace IDs: {len(workspace_ids)}")

        time_entries_insert_statements = []
        time_entries_ids = []
        time_entries_json_data = []

        for wsp in workspace_ids:
            time_entries_resp = requests.get(f"https://api.mavenlink.com/api/v1/time_entries?include=role,user,workspace,story&workspace_id={wsp}&per_page=100", headers=headers)
            time_entries_dict = time_entries_resp.json()

            workspaces = time_entries_dict['workspaces']
            time_entries = time_entries_dict['time_entries']
            stories = time_entries_dict['stories']
            roles = time_entries_dict['roles']
            users = time_entries_dict['users']

            for entry in time_entries:
                time_entries_ids.append(entry)
                time_entries_object = time_entries[entry]
                date = time_entries_object['date_performed']
                person = users[time_entries_object['user_id']]['full_name']
                project = workspaces[time_entries_object['workspace_id']]['title'].replace("'", "''")
                task = stories[time_entries_object['story_id']]['title'].replace("'", "''") if time_entries_object['story_id'] is not None else 'NULL'
                time_in_hrs = time_entries_object['time_in_minutes'] / 60
                role = roles[time_entries_object['role_id']]['name']
                rate = time_entries_object['rate_in_cents'] / 100
                subtotal = rate * time_in_hrs
                workspace = 'NULL'

                if task != 'NULL':
                    task = f"'{task}'"

                # DB Insert Values
                values = {
                    "Date": date,
                    "Person": person,
                    "Project": project,
                    "Task": task,
                    "Time_in_hrs": time_in_hrs,
                    "Role": role,
                    "Rate": rate,
                    "Subtotal": subtotal,
                    "Workspace": workspace
                }
                time_entries_json_data.append(values)
                self.logger.info(values)

        # Initialize ActionManager
        am = ActionManager()

        am.execute(
            "127.0.0.1",
            "sql.insert_bulk",
            {"connection": "productionCloudExtension", "data": support_details_json_data, "table": "[dbo].[Bkp_ML_Support_Detail]"}
        )
        self.logger.info(f"Total Time Entries: {len(time_entries_json_data)}")

        # Chunk size for batch processing
        chunk_size = 500

        # Split the time_entries_json_data into chunks of 500
        time_entries_chunks = list(self.chunk_list(time_entries_json_data, chunk_size))

        
        return {
            'result': 'success',
            'message': 'Mavenlink integration completed successfully.'
        }

class ActionManager(object):
    def execute(self, server, action, params):
        client = Client(base_url="https://{}/".format(server))
        client.liveactions.create(LiveAction(action=action, parameters=params))

# Instantiate and run the MavenlinkIntegrationAction
action = MavenlinkIntegrationAction()
action.run()

