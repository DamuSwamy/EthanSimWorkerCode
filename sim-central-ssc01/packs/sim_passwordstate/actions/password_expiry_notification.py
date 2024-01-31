from st2common.runners.base_action import Action
import requests
from datetime import datetime, timedelta

class GetUserDetailsWithinExpiryRangeAction(Action):
    def run(self):
        # Azure AD details (hard-coded values)
        tenant_id = "455ac8b0-5713-4dd7-be28-3898e9505f7e"
        client_id = "20acf5a3-610b-42ae-a6c1-60e288948d76"
        client_secret = "Xvo8Q~xyxhtuDa_rcASU-E4tryPMriWC7EhNrbWV"
        resource = 'https://graph.microsoft.com'

        # Function to get an access token
        def get_access_token():
            token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/token'
            token_data = {
                'grant_type': 'client_credentials',
                'client_id': client_id,
                'client_secret': client_secret,
                'resource': resource
            }
            token_r = requests.post(token_url, data=token_data)
            return token_r.json().get("access_token")

        # Function to format datetime
        def format_datetime(datetime_str):
            if datetime_str:
                # Actual format: '2023-01-01T00:00:00Z'
                return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S")
            else:
                return ""

        # Function to calculate the date by adding 90 days to the timestamp
        def calculate_expiry_date(last_password_change):
            if last_password_change:
                last_password_change_datetime = datetime.strptime(last_password_change, "%Y-%m-%d %H:%M:%S")
                expiry_date = last_password_change_datetime + timedelta(days=90)
                return expiry_date.strftime("%Y-%m-%d")
            else:
                return ""

        # Function to get users with specific domains, last password change timestamp, and accountEnabled: true
        def get_all_users_enabled_within_expiry_range(token, domains, min_days, max_days):
            users = []
            graph_url = f'https://graph.microsoft.com/beta/users?$select=displayName,userPrincipalName,lastPasswordChangeDateTime,accountEnabled'
            headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}

            while True:
                user_r = requests.get(graph_url, headers=headers)
                user_data = user_r.json()

                for user in user_data.get('value', []):
                    email = user.get('userPrincipalName', '')
                    if any(domain in email for domain in domains) and user.get('accountEnabled', False):
                        last_password_change = format_datetime(user.get('lastPasswordChangeDateTime'))
                        expiry_date = calculate_expiry_date(last_password_change)
                        current_date = datetime.now()
                        expiry_date_datetime = datetime.strptime(expiry_date, "%Y-%m-%d")

                        days_to_expiry = (expiry_date_datetime - current_date).days

                        if min_days <= days_to_expiry <= max_days:
                            users.append({
                                'name': user.get('displayName'),
                                'email': email,
                                'last_password_change': last_password_change,
                                'expiry_date': expiry_date,
                                'days_to_expiry': days_to_expiry
                            })

                next_link = user_data.get('@odata.nextLink')
                if next_link:
                    graph_url = next_link
                else:
                    break

            return users

        # Main
        token = get_access_token()
        domains = ['Ethan.com.au', 'ethan.com.au']
        min_days = 15
        max_days = 30

        users = get_all_users_enabled_within_expiry_range(token, domains, min_days, max_days)

        return users

