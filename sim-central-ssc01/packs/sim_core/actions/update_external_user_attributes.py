import requests
from st2common.runners.base_action import Action

class UpdateUserProperties(Action):
    def run(self, user_object_id, company, given_name, surname, sponsor, ticket):
       
        tenant_id = 'b02e50ac-20e5-4c60-bcd4-8454b3201fd1'
        client_id = '0ce270d2-c253-454e-bc7f-a95877f54c9f'
        client_secret = 'bku8Q~Xaqm_47Gf1tBBOrBzW1VlQliLZc_hMnalM'
        graph_url = 'https://graph.microsoft.com/v1.0'

        # Get an access token
        token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
        token_data = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
            'scope': 'https://graph.microsoft.com/.default'
        }
        token_response = requests.post(token_url, data=token_data)
        access_token = token_response.json().get('access_token')

        # Set the new values for user properties
        update_data = {
            'companyName': company,
            'givenName': given_name,
            'surname': surname,
            'department': sponsor,
            'jobTitle': ticket
        }

        # Build the URL for updating user properties
        update_url = f'{graph_url}/users/{user_object_id}'

        #
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

      
        update_response = requests.patch(update_url, json=update_data, headers=headers)

        
        if update_response.status_code == 204:
            # Get updated user details
            user_details_url = f'{graph_url}/users/{user_object_id}?$select=id,companyName,givenName,surname,department,jobTitle'
            user_details_response = requests.get(user_details_url, headers=headers)
            user_details = user_details_response.json()

            return True, 'User properties updated successfully', user_details
        else:
            return False, f'Error updating user properties: {update_response.text}', None

	    

