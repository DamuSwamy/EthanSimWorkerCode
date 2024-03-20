import requests
import json
from st2common.runners.base_action import Action

class SelfDestructMessageAction(Action):
    def run(self, api_url, api_key, to_email, message, expires_at, passphrase, no_views):
        from_user_id = "svc-ss-listcreation"
        from_first_name = "sim"
        from_surname = "Automation"
        from_email_address = "passwordstate@ethan.com.au"

        headers = {
            "Content-Type": "application/json",
            "APIKey": api_key
        }

        data = {
            "ToEmailAddress": to_email,
            "Passphrase": passphrase,
            "Message": message,
            "ExpiresAt": expires_at,
            "FromUserID": from_user_id,
            "FromFirstName": from_first_name,
            "FromSurname": from_surname,
            "FromEmailAddress": from_email_address,
            "NoViews": no_views
        }

        response = requests.post(api_url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            return {"message": "Message sent successfully!"}
        else:
            return {"error": "Failed to send message. Status code: {}".format(response.status_code)}

