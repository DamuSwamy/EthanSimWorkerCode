from st2common.runners.base_action import Action
from datetime import datetime, timedelta
import requests

class UpdateUserInformationAction(Action):
    def run(self, sponsor, ticket, notes, object_id, ext15, ext16, token):
        url = f"https://graph.microsoft.com/v1.0/users/{object_id}"

        current_date = datetime.now().strftime("%Y%m%d")
        end_date = (datetime.now() + timedelta(days=6 * 30)).strftime("%Y%m%d")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }

        payload = {
            ext15: f"{{\"Sponsor\":\"{sponsor}\",\"Ticket\":\"{ticket}\",\"Start\":\"{current_date}\",\"End\":\"{end_date}\"}}",
            ext16: f"{{\"Notes\":\"{notes}\"}}"
        }

        response = requests.patch(url, headers=headers, json=payload)

        if response.status_code == 204:
            result = {
                "status": "success",
                "message": "Extension updated successfully",
                "end_date": end_date
            }
        else:
            result = {
                "status": "failure",
                "message": f"Request failed with status code: {response.status_code}",
                "response": response.text,
                "end_date": end_date
            }

        
        return result

