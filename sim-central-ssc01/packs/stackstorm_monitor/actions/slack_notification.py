import requests
from st2common.runners.base_action import Action
from requests.packages.urllib3.exceptions import InsecureRequestWarning    
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
class SlackNotificationAction(Action):
    def run(self, message, webhook_url):
        # Define the payload for the Slack message
        payload = {
            "text": message
        }

        # Send the message to Slack
        response = requests.post(webhook_url, json=payload,verify=False)

        # Check the response for error handling, if needed
        if response.status_code != 200:
            return (False, f"Failed to send message to Slack. Status code: {response.status_code}")
        else:
            return (True, "Message sent to Slack successfully")
