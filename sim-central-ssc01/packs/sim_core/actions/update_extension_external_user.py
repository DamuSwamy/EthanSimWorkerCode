import json
import requests
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from st2common.runners.base_action import Action

class UpdateUserExtensionsAction(Action):
    def run(self, object_id, ext15, ext16, sponsor, ticket, notes, client_id, client_secret, tenant_id):
        # Python equivalent of PowerShell's Get-Date
        creation_date = datetime.now().strftime('%Y%m%d')

        # Python equivalent of PowerShell's $ExpirationDate
        expiration_date = datetime.now() + relativedelta(months=6)

        # Python equivalent of PowerShell's $End
        end_date = expiration_date.strftime('%Y%m%d')

        # Cloud Extension Attributes
        ext_properties_15 = {
            "Sponsor": sponsor,
            "Ticket": ticket,
            "Start": creation_date,
            "End": end_date
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
        url_15 = f"https://graph.microsoft.com/v1.0/users/{object_id}/extensions/{ext15}"
        response_15 = requests.patch(url_15, headers=headers, data=ext_properties_15_json)

        # Update extension attribute 16
        url_16 = f"https://graph.microsoft.com/v1.0/users/{object_id}/extensions/{ext16}"
        response_16 = requests.patch(url_16, headers=headers, data=ext_properties_16_json)

        # Check the responses
        result = {
            "response_15": {"status_code": response_15.status_code, "text": response_15.text},
            "response_16": {"status_code": response_16.status_code, "text": response_16.text},
            "end_date": end_date
        }

        return result

