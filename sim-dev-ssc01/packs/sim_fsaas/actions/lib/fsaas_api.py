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

    req['headers'].update(
        {
         "Accept": "application/json",
         "Authorization": f"Basic {args.get('authorization')}"
        }
        )
    
    return req

def makeRequest(**kwargs):
    method = kwargs.get('method', 'get')
    del kwargs['method']
    s = requests.Session()
    response = getattr(s, method)(**kwargs)
    response.raise_for_status()
    return response
