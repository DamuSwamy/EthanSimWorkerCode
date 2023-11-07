import requests
from st2common.runners.base_action import Action

class PostMessageToWebexRoom(Action):
    def run(self, bearer_token, room_id, text):
    
        api_url = "https://webexapis.com/v1/messages"

     
        headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json"
        }


        body = {
            "roomId": room_id,
            "markdown": text
        }

        response = requests.post(api_url, json=body, headers=headers)

      
        if response.status_code == 200:
            return {"status": "Message posted successfully"}
        else:
            return {
                "status": "Failed to post message",
                "status_code": response.status_code,
                "error": response.text
            }
