import json
from lib.actions import BaseAction
from lib import zerto_api

class ZVMGetVersionAction(BaseAction):
    def run(self, zvm_host, port, access_token=None):
        ret = False
        args = {}
        if access_token is None:
            access_token = self.establish_connection(zvm_host, port)

        args['access_token'] = access_token
        
        args['url'] = "https://{}:{}/v1/localsite".format(zvm_host, port)
        args['method'] = "get"

        req_data = zerto_api.addArgs(**args)
        resp = zerto_api.makeRequest(**req_data)

        myresp = {}
        myresp['status_code'] = resp.status_code
        try:
            myresp['data'] = json.loads(resp.content.rstrip())
        except ValueError:
            myresp['data'] = resp.content

        if myresp['status_code'] >= 200 and myresp['status_code'] <= 299:
            ret = True

        return (ret, myresp)
