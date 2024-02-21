from st2common.runners.base_action import Action
import json
from datetime import datetime
import math
import pytz
import requests

class FSaas(Action):
    def __init__(self, config=None, action_service=None):
        super(FSaas, self).__init__(config, action_service)

    def run(self, fileName):

        url = 'https://10.120.97.200:8080/platform/3/cluster/config'
        username = 'vb4-isi1-api-RO'
        password = 'tuner-ZbFC2iweiz6Qe!hAkdjL'
        headers = {
        'Accept': 'application/json'
        }

        response = requests.get(url, auth=(username, password), headers=headers, verify = False)
        print(response)
        if response.status_code == 200:
            print(response.json()) 
            return {
                'data':response.json()
            }

        else:
            return {
                'msg':'Request failed'
            }
        




        
    



