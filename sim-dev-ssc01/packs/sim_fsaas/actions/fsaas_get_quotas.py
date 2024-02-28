from st2common.runners.base_action import Action
from lib import fsaas_api

class FSaas(Action):
    def run(self, cluster):
        
        args = {}
        port = self.config['fsaas'].get(cluster)['port']
        fsaas = self.config['fsaas'].get(cluster)['cluster']
        authorization = self.config['fsaas'].get(cluster).get('authorization')
        args['url'] = "https://{}:{}/platform/15/quota/quotas".format(fsaas, port)
        args['method'] = "get"
        args['authorization'] = authorization

        req_data = fsaas_api.addArgs(**args)

        try:
            resp = fsaas_api.makeRequest(**req_data)
            if resp.status_code >= 200 and resp.status_code <= 299:
                return {
                'data':resp.json()
            }
        except Exception as e:
            return {
             'msg':e
            }