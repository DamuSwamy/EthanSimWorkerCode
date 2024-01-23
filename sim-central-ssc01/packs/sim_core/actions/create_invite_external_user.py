from st2common.runners.base_action import Action
import requests

class InviteExternalUser(Action):
    def run(self, external_user_email, sponsor_email, access_token, given_name, surname, company):
        # Hardcoded values
        expiration_period_months = 6  # replace with actual value
        invite_redirect_url = 'https://portal.office.com'  # Hardcoded value

        # Construct InvitedUserDisplayName
        display_name = f"{given_name} {surname} ({company})"

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

        # Set the Graph API request headers
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }

        # Set the Graph API request payload
        graph_api_payload = {
            'invitedUserDisplayName': display_name,
            'invitedUserEmailAddress': external_user_email,
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

