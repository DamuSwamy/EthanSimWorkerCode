import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from st2common.runners.base_action import Action
import ast

class HttpRequestAction(Action):
    def run(self, url, headers, method, body={}, input_data=None, action_name=None):
        if body:
            json_dat = json.dumps(body)
            body = json.loads(json_dat)
        elif input_data and action_name:
            input_data = json.dumps(input_data)
            body = {}
            body["action"] = action_name
            body["parameters"] = {}
            body["parameters"]["data"] = json.dumps(input_data).replace('"', "'").replace("\\", "")
            body["user"] = None

        args = {}
        args['url']     = url
        args['method']  = method
        args['headers'] = headers
        args['data']    = body
        print(body)

        req_data = self.addArgs(**args)
        resp = self.makeRequest(**req_data)

        myresp = {}
        myresp['status_code'] = resp.status_code
        try:
            myresp['body'] = json.loads(resp.content.rstrip())
        except ValueError:
            myresp['body'] = resp.content

        return myresp


    def addArgs(self, **args):
        req = {}
        req['headers']     = args.get('headers', {})
        req['verify']      = args.get('verify', False)
        req['url']         = args['url']
        req['method']      = args['method']
        req['params']      = args.get('params', {})
        req['data']        = args.get('data', {})
        return req

    def makeRequest(self, **kwargs):
        method = kwargs.get('method', 'get')
        del kwargs['method']
        s = requests.Session()
        response = getattr(s, method)(**kwargs)
        response.raise_for_status()
        return response
