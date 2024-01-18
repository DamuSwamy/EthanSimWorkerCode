from st2common.runners.base_action import Action
import requests

class InviteExternalUser(Action):
    def run(self, external_email, sponsor_email):
        # Hardcoded values
        client_id = '0ce270d2-c253-454e-bc7f-a95877f54c9f'
        tenant_id = 'b02e50ac-20e5-4c60-bcd4-8454b3201fd1'
        client_secret = 'bku8Q~Xaqm_47Gf1tBBOrBzW1VlQliLZc_hMnalM'
        expiration_period_months = 6 
        invite_redirect_url = 'https://portal.office.com'  

        try:
            # Obtain the access token using client credentials flow
            token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
            token_data = {
                'grant_type': 'client_credentials',
                'client_id': client_id,
                'client_secret': client_secret,
                'scope': 'https://graph.microsoft.com/.default',
            }

            token_response = requests.post(token_url, data=token_data)
            access_token = token_response.json().get('access_token')
        except Exception as e:
            print(f"Failed to obtain access token: {e}")
	       

        # Set the invitation message body
        customized_message_body = f"""
        Welcome to Ethan External Access

            - Your sponsor contact is {sponsor_email}
            - Account expires in {expiration_period_months} months
            - If you have any issues, please review the guide at https://www.ethan.com.au/GuestAzureADuser/Welcome.html
            - For further assistance, please contact your sponsor, and they will create a help desk request on your behalf.

        Thanks

        Ethan IT Team
        """

        # Set the Graph API endpoint
        graph_api_endpoint = "https://graph.microsoft.com/v1.0/invitations"

       
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }

        # Set the Graph API request payload
        graph_api_payload = {
            'invitedUserEmailAddress': external_email,
            'inviteRedirectUrl': invite_redirect_url,
            'sendInvitationMessage': True,
            'invitedUserMessageInfo': {
                'customizedMessageBody': customized_message_body
            },
            'invitedUserType': 'Guest',
        }

        try:
            # Make the Graph API request
            graph_api_response = requests.post(graph_api_endpoint, headers=headers, json=graph_api_payload)
        except Exception as e:
            # Handle the exception, log it, or raise it depending on your needs
            print(f"Failed to make Graph API request: {e}")
            raise

        # Output the Graph API response
        return graph_api_response.json()

                                                                                                       
