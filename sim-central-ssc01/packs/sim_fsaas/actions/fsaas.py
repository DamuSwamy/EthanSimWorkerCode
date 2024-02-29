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

        url = 'https://vb4-isi1-mgmt.fs.ethoria.services:8080/platform/3/cluster/config'
        #url = "https://vb4-isi1-mgmt.fs.ethoria.services:8080/platform/15/quota/quotas"
        username = 'vb4-isi1-api-RO'
        password = 'tuner-ZbFC2iweiz6Qe!hAkdjL'
        headers = {
        'Accept': 'application/json',
        'Authorization': 'Basic dmI0LWlzaTEtYXBpLVJPOnR1bmVyLVpiRkMyaXdlaXo2UWUhaEFrZGpM'
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
        




        
    



