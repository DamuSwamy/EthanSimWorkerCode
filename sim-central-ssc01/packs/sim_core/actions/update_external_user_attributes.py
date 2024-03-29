import requests
from st2common.runners.base_action import Action

class UpdateUserProperties(Action):
    def run(self, user_object_id, company, given_name, surname, sponsor, ticket, access_token):

        graph_url = 'https://graph.microsoft.com/v1.0'

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

