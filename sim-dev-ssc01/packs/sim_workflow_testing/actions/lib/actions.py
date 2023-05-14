from st2common.runners.base_action import Action
import requests
import json

class BaseAction(Action):
    def __init__(self, config):
        super(BaseAction, self).__init__(config)

    def netdb_api(self, params, payload={}, **kwargs):
        auth_token = self.config['auth_token']
        if auth_token in kwargs and kwargs.get("auth_token"):
            auth_token = kwargs.get("auth_token")
        if 'method' in kwargs:
            method = kwargs['method']
        endpoint = "{}/{}".format(self.config['url'], params)
        payload  = payload
        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Token {}".format(auth_token)
        }
        response = requests.request(method, endpoint, headers=headers, data=payload)
        return response


    def read_config(self):
        return self.config['compliance']
