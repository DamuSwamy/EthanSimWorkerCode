import json
from lib.actions import BaseAction
from lib import braas_api

class GetGroupsAction(BaseAction):
    def run(self, braas, access_token=None):
        ret = False
        args = {}
        result = []
        backup_server = self.config['braas'].get(braas)['host']
        if access_token is None:
            access_token = self.establish_connection(braas)

        args['access_token'] = access_token
        
        args['url'] = "https://{}/api/v1/groups?domain=%2F&recursive=true&size=10000".format(backup_server)
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
            for group in myresp['data']['content']:
                group['backupServer'] = braas
                group_id = group.pop('id')
                group.pop('proxyIds')
                group['gid'] = group_id
                ruleidentifier = group.pop("ruleIdentifier")
                if ruleidentifier is not None:
                    for key, value in ruleidentifier.items():
                        keyarray       = [*key]
                        keyFirstLetter = keyarray[0].upper()
                        keyarray.pop(0)
                        keyarrayStr    = "".join(keyarray)
                        group['ruleIdentifier'+keyFirstLetter+keyarrayStr] = value
                result.append(group)

        return (ret, result)
