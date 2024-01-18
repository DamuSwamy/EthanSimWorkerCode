import json
import requests
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from st2common.runners.base_action import Action

class UpdateUserExtensionsAction(Action):
    def run(self, object_id, ext15, ext16, sponsor, ticket, creation_date, notes):
        # Microsoft Graph API endpoint for updating user extensions
        graph_api_endpoint = "https://graph.microsoft.com/v1.0/users/{user_id}/extensions/{extension_name}"

        # Convert creation_date to datetime object
        creation_date = datetime.strptime(creation_date, '%Y-%m-%dT%H:%M:%S')

        # Calculate End date (6 months later)
        end_date = creation_date + relativedelta(months=6)
        end = end_date.strftime('%Y%m%d')

        # Cloud Extension Attributes
        ext_properties_15 = {
            "Sponsor": sponsor,
            "Ticket": ticket,
            "Start": creation_date.strftime('%Y-%m-%dT%H:%M:%S'),
            "End": end
        }

        ext_properties_16 = {
            "Notes": notes
        }

        # Convert dictionaries to JSON
        ext_properties_15_json = json.dumps(ext_properties_15, separators=(',', ':'))
        ext_properties_16_json = json.dumps(ext_properties_16, separators=(',', ':'))

        # Trim string if needed
        if len(ext_properties_16_json) > 250:
            ext_properties_16_json = ext_properties_16_json[:250]

        # Microsoft Graph API credentials
        client_id = self.config.get('client_id')
        tenant_id = self.config.get('tenant_id')
        client_secret = self.config.get('client_secret')

        # Get access token using client credentials grant flow
        token_endpoint = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
        token_data = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
            'scope': 'https://graph.microsoft.com/.default'
        }

        token_response = requests.post(token_endpoint, data=token_data)
        token_json = token_response.json()
        access_token = token_json['access_token']

        # Update extension attributes using Microsoft Graph API
        headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json'
        }

        # Update extension attribute 15
        url_15 = graph_api_endpoint.format(user_id=object_id, extension_name=ext15)
        response_15 = requests.patch(url_15, headers=headers, data=ext_properties_15_json)

        # Update extension attribute 16
        url_16 = graph_api_endpoint.format(user_id=object_id, extension_name=ext16)
        response_16 = requests.patch(url_16, headers=headers, data=ext_properties_16_json)

        # Check the responses
        result = {
            "response_15": {"status_code": response_15.status_code, "text": response_15.text},
            "response_16": {"status_code": response_16.status_code, "text": response_16.text}
        }

        return result

