import json
from lib.actions import BaseAction
from lib import braas_api

class GetGroupMembersAction(BaseAction):
    def run(self, braas, group_ids, access_token=None):
        self.backup_server = self.config['braas'].get(braas)['host']
        if access_token is None:
            access_token = self.establish_connection(braas)
        self.access_token = access_token
        self.result = []
        for gid in group_ids:
            self.result = self.result + self.get_members(gid, braas)
        return self.result

    def get_members(self, gid, braas):
        result = []
        args = {}
        args['access_token'] = self.access_token
        
        args['url'] = "https://{}/api/v1/groups/{}/members?recursive=true&paged=false&size=10000".format(self.backup_server, gid)
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
            for group in myresp['data']['content']:
                group_mem = {}
                group_mem['backupServer'] = braas
                group_mem['cid'] = group['cid']
                group_mem['gid'] = group['gid']
                group_mem['domain'] = group['domain']
                group_mem['name'] = group['name']
                group_mem['memberType'] = group['memberType']
                result.append(group_mem)
        return result
