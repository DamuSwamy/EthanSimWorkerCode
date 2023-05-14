import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def addArgs(**args):
    req = {}
    req['headers']     = args.get('headers', {})
    req['verify']      = args.get('verify', False) 
    req['url']         = args['url']
    req['method']      = args['method']
    req['params']      = args.get('params', {})
    req['data']        = args.get('data', {})

    if not 'access_token' in args:
        return (False, "Failed finding access token")
    req['headers'].update({"Content-type": "application/json"})
    req['headers'].update({"Authorization": "Bearer {}".format(args['access_token'])})
    return req

def makeRequest(**kwargs):
    method = kwargs.get('method', 'get')
    del kwargs['method']
    s = requests.Session()
    return getattr(s, method)(**kwargs)

