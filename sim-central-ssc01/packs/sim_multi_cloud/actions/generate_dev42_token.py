import json
import csv
import requests
import base64
from st2common.runners.base_action import Action
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the InsecureRequestWarning, leave other warnings unaffected
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class GenerateDev42Token(Action):
    def run(self,username, password):

        url="https://cmdb.ecorp.systems/tauth/1.0/token/"
        credentials = base64.b64encode(f'{username}:{password}'.encode()).decode()
        #credentials='OTc1NjUxNDI3NzEwNDJjY2IwYjkyOGFlM2U2NThlMjY6NDU5MWNmOTYxOTM4NGJiMWJhYjFkNWE0MGE0YjZhZWVfNGYyZjE3NGZlNWRiNDdiY2JlNGIwYTIxMzgwZmU0NTU='
        #print(credentials)
        headers = {
        'Authorization': f'Basic {credentials}',
        'Accept': 'application/json',  # Adjust content type based on your API requirements
        'Cookie': 'd42sessnid_csrftoken=WvcEEPtIjtMtH0ADoBSUPGVfMjwWAg82KYiwbyNe5kfipAKQalHjvqfqDYBNDDCZ'
        }

        response=requests.post(url,headers=headers,verify=False)
        response_json=json.loads(response.text)
        #print(response_json)
        access_token = response_json.get('token')
        #print(type(access_token))
        #print("hello")
        access_token=access_token.rstrip()
        #print(access_token)
        #print(base64.b64encode((access_token+"mis@123").encode()).decode())
        print("Token Generated")
        return access_token
