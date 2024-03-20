import requests
from st2common.runners.base_action import Action

class SendEmailConfirmation(Action):
    def run(self, to_email, user_name, user_email, requester_name):
        url = "https://sim-central.sim.esecure.systems/api/v1/executions"

        subject = f"User Account Creation Confirmation for {user_name}"
        
        body = f"""\
        <html>
          <body>
            <p>Dear {requester_name},</p>
            <p>We are writing to confirm the successful creation of the user account as per your request. Kindly find the user's login credentials provided through our secure Password State self-destruct message system.</p>
            <p>Please take note of the following details:</p>
            <ul>
              <li>Username: {user_name}</li>
              <li>User Email: {user_email}</li>
              <li>Email with Password has been sent separately via password state.</li>
              <li>Passphrase for URL Access: ethan2020</li>
            </ul>
            <p>For security purposes, we would like to highlight the following points:</p>
            <ul>
              <li>The password message will self-destruct in 3 days if unopened.</li>
              <li>You can access this message only twice.</li>
            </ul>
            <p>The user will be prompted to reset their password upon the first login.</p>
            <p>They should also link a mobile number to their account by logging into the following URL: <a href="https://warrigal.onelogin.com">https://warrigal.onelogin.com</a></p>
            <p>Profile &gt; Add 2-Factor Authentication Method (SMS).</p>
            <p>If they require any assistance with the above, please give service desk a call.</p>
            <p>Kind regards,</p>
            <p>SiM Automation<br>Ethan</p>
          </body>
        </html>
        """

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
                "body": body
            }
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 201:
            self.logger.info("Email sent successfully.")
        else:
            self.logger.error(f"Failed to send email. Status code: {response.status_code}, Response: {response.text}")
            return (False, f"Failed to send email. Status code: {response.status_code}")

        return (True, "Email sent successfully.")

