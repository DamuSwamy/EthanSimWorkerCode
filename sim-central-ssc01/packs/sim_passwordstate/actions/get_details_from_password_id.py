import requests
from st2common.runners.base_action import Action

class GetPasswordAction(Action):
    def run(self, password_id, api_key):
        url = f"https://pwd.ecorp.systems/api/passwords/{password_id}"
        headers = {
            'APIKey': api_key
        }

        response = requests.get(url, headers=headers)

        result = {
            'status_code': response.status_code,
        }

        if response.status_code == 200:
            json_response = response.json()
            result['json_response'] = json_response
        else:
            result['error_message'] = f"Error: {response.status_code}"

        return result

