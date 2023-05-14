import json
from lib.actions import BaseAction
from lib import braas_api

class GetClientsAction(BaseAction):
    def run(self, braas, domain_name=None, access_token=None):
        ret = False
        result = []
        args = {}
        backup_server = self.config['braas'].get(braas)['host']
        if access_token is None:
            access_token = self.establish_connection(braas)

        args['access_token'] = access_token
        if domain_name is None:
            domain_name = "/"

        args['url'] = "https://{}/api/v1/clients?domain={}&recursive=true&size=10000".format(backup_server, domain_name)
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
            for client in myresp['data']['content']:
                if 'vcCids' in client:
                    vcCids = client.pop('vcCids')
                    client.pop('biosUuid')
                    client.pop('maxActiveJobs')
                    client.pop('autoDsMapping')
                    client.pop('vcs')
                    client.pop('vcenterHost')
                    if vcCids is not None:
                        client['vcCid'] = ",".join(vcCids)
                if not 'vcCid' in client:
                    client['vcCid'] = ''
                if not 'vmName' in client:
                    client['vmName'] = ''
                if not 'instanceUuid' in client:
                    client['instanceUuid'] = ''
                if not 'cbtEnabled' in client:
                    client['cbtEnabled'] = ''
                if not 'vmxPath' in client:
                    client['vmxPath'] = ''
                if not 'datacenter' in client:
                    client['datacenter'] = ''
                if not 'inventoryPath' in client:
                    client['inventoryPath'] = ''
                if not 'deleted' in client:
                    client['deleted'] = None
                else:
                    if client['deleted']:
                        client['deleted'] = 'true'
                    else:
                        client['deleted'] = 'false'
                if 'enabled' in client:
                    if client['enabled']:
                        client['enabled'] = 'true'
                    else:
                        client['enabled'] = 'false'
                if not 'template' in client:
                    client['template'] = ''
                client_id = client.pop('id')
                client.pop('contact')
                client.pop('clientInitBackup')
                client['cid'] = client_id
                paging = client.pop("paging")
                if paging is not None:
                    for key, value in paging.items():
                        keyarray       = [*key]
                        keyFirstLetter = keyarray[0].upper()
                        keyarray.pop(0)
                        keyarrayStr    = "".join(keyarray)
                        client['paging'+keyFirstLetter+keyarrayStr] = value
                result.append(client)

        return (ret, result)
