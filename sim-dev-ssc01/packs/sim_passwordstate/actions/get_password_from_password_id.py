import requests
from st2common.runners.base_action import Action

class GetPasswordAction(Action):
    def run(self, password_id, api_key):
        url = f"https://pwd.ecorp.systems/api/passwords/{password_id}"
        headers = {
            'APIKey': api_key
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            json_response = response.json()
            password_value = json_response[0]["Password"]
            return password_value  # Return only the password as a string
        else:
            return f"Error: {response.status_code}"
