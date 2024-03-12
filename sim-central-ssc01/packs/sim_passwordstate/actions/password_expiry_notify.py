import time
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

        # Function to send email using sim_central
        def send_email(to, subject, body):
            url = "https://sim-central.sim.esecure.systems/api/v1/executions"
            headers = {
                "st2-api-key": "MTc3MjBjODg1YjUwZDM2NzM2OGFkNjBkMjE0NWIxOWVkYTBmMThlZWY0ODUwMTcwYzQzNzJlZDcwYTIzYzAwYQ",
                "Content-Type": "application/json"
            }
            payload = {
                "action": "core.sendmail",
                "parameters": {
                    "from": "SiM.Automation@ethan.com.au",
                    "to": to_email,
                    "subject": subject,
                    "body": body,
                }
            }
            response = requests.post(url, headers=headers, json=payload)
            return response.json()

        # Function to get users with last password change timestamp
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

        html_body_template = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Password Expiry Notification</title>
        </head>
        <body>
            <div>
                Dear {user_name},<br><br>
                Your <strong>ethan.com.au</strong> password is set to expire in the next {days_to_expiry} days and we highly recommend you change it ASAP to save yourself a whole lotta admin hassle. The security of your account is a top priority to us and helps to keep the company and all your peers safe.<br><br>
                <strong>Password Expiry Details:</strong><br>
                <ul>
                    <li>Current Password Expiry Date: {expiry_date}</li>
                </ul>
                <p><strong>Can’t I Just Do It Later?</strong></p>
                <p>To put it bluntly…we’d really prefer you didn’t. Changing your password proactively ensures that your account remains secure and accessible, while waiting until the last minute can result in unnecessary account lockouts, disruptions to your work, and lots of painful back and forth.</p>
                <p><strong>How to Update Your Password:</strong></p>
                <ol>
                    <li>Log in to your company account using your current credentials.</li>
                    <li>Navigate to the "Account Settings" or "Profile" section.</li>
                    <li>Look for the "Change Password" option.</li>
                    <li>Follow the on-screen instructions to create a new, strong password.</li>
                </ol>
                <p><strong>Password Guidelines:</strong></p>
                <ul>
                    <li>Passwords must</li>
                    <li>Be at least 10 characters long.</li>
                    <li>Include a combination of uppercase and lowercase letters, numbers, and special characters.</li>
                    <li>Not contain easily guessable information like birthdays or names.</li>
                </ul>
                <p>As a reminder, you should not share your password with anyone, including IT support or colleagues.</p>
                <p><strong>Need Assistance?</strong></p>
                <p>If you encounter any difficulties while updating your password or have questions about password security, please don't hesitate to reach out to our IT support team at [IT Support Email or Phone Number]. They are here to assist you (and will look upon you very kindly for making the effort to change your password before it expires).</p>
                <p>We appreciate your cooperation in maintaining the security of our systems and data, and hope you have a great day.</p>
                <p><strong>Click below button to change the password</strong></p>
                <!-- Hyperlink for Redirect -->
                <a href="https://account.activedirectory.windowsazure.com/ChangePassword.aspx" style="display: inline-block; background-color: black; color: white; padding: 10px; text-decoration: none; cursor: pointer;" target="_blank">
                    Change Password Now
                </a>
                <br><br>
                Best regards,<br>
                Sim Automation,<br>
                Ethan
            </div>
        </body>
        </html>
        """


#iteration for every user
        for user in users:
            user["days_to_expiry"] = (datetime.strptime(user["expiry_date"], "%Y-%m-%d") - datetime.now()).days
            to_email = "Sai.Yagneswarreddy@Ethan.com.au"
            subject = "Password Expiry Notification - Your Password Will Expire Soon"

            # Update the HTML body template with individual user details
            html_body = html_body_template.format(
                user_name=user["name"],
                days_to_expiry=user["days_to_expiry"],
                expiry_date=user["expiry_date"]
            )
            time.sleep(200)
            # Send email
            response = send_email("to_email", subject, html_body)
            if "success" in response and response["success"]:
                print(f"Email sent successfully to {to_email}")
            else:
                print(f"Failed to send email to {to_email}. Response: {response}")

        return users
