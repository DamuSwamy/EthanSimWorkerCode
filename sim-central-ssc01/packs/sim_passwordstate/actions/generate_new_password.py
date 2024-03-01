from st2common.runners.base_action import Action
import requests


class GeneratePasswordAction(Action):
    def run(self):
        url = "https://pwd.ecorp.systems/api/generatepassword/"
        headers = {
            "APIKey": "e75c3a324b869fd46d98ec23f75ba3c3"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an error for bad status codes
            
            # Parse the JSON response and extract the password field
            password = response.json()[0]["Password"]
            
            return password
        except requests.exceptions.RequestException as e:
            return (False, "Failed to generate password: {}".format(str(e)))

