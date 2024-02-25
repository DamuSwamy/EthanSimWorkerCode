import requests
from st2common.runners.base_action import Action

class AddUserToGroupAction(Action):
    def run(self, user_upn, group_display_name, client_id, tenant_id, client_secret):
        # Get access token
        token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
        token_data = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
            'scope': 'https://graph.microsoft.com/.default'
        }
        token_response = requests.post(token_url, data=token_data)
        access_token = token_response.json()['access_token']

        # Get user's object ID
        get_user_url = f'https://graph.microsoft.com/v1.0/users/{user_upn}'
        headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json'
        }
        response = requests.get(get_user_url, headers=headers)

        if response.status_code == 200:
            user_id = response.json()['id']
            
            # Get group ID based on display name
            get_groups_url = 'https://graph.microsoft.com/v1.0/groups'
            response = requests.get(get_groups_url, headers=headers)

            if response.status_code == 200:
                groups = response.json()['value']
                for group in groups:
                    if group['displayName'] == group_display_name:
                        group_id = group['id']

                        # Add user to group
                        add_user_to_group_url = f'https://graph.microsoft.com/v1.0/groups/{group_id}/members/$ref'
                        data = {
                            '@odata.id': f'https://graph.microsoft.com/v1.0/directoryObjects/{user_id}'
                        }
                        response = requests.post(add_user_to_group_url, headers=headers, json=data)

                        if response.status_code == 204:
                            return {"result": "User added to the group successfully."}
                        else:
                            return {"error": "Failed to add user to the group.", "status_code": response.status_code, "message": response.text}
                else:
                    return {"error": "Group not found."}
            else:
                return {"error": "Failed to retrieve groups.", "status_code": response.status_code, "message": response.text}
        else:
            return {"error": "Failed to retrieve user details.", "status_code": response.status_code, "message": response.text}

