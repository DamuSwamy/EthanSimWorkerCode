import json
from lib.actions import BaseAction
from lib import braas_api

class GetGroupMembersAction(BaseAction):
    def run(self, braas, group_id, access_token=None):
        ret = False
        args = {}
        backup_server = self.config['braas'].get(braas)['host']
        if access_token is None:
            access_token = self.establish_connection(braas)

        args['access_token'] = access_token
        
        args['url'] = "https://{}/api/v1/groups/{}/members?recursive=true&paged=false&size=10000".format(backup_server, group_id)
        args['method'] = "get"

        req_data = braas_api.addArgs(**args)
        resp = braas_api.makeRequest(**req_data)

        myresp = {}
        myresp['status_code'] = resp.status_code
        try:
            myresp['data'] = json.loads(resp.content.rstrip())
        except ValueError:
            myresp['data'] = resp.content

        if myresp['status_code'] >= 200 and myresp['status_code'] <= 299:
            ret = True

        return (ret, myresp)
