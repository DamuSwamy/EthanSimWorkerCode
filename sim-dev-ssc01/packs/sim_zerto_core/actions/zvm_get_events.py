import json
from lib.actions import BaseAction
from lib import zerto_api
from datetime import datetime

class ZVMGetEventsAction(BaseAction):
    def run(self, zvm_host, port, access_token=None):
        ret = False
        args = {}
        if access_token is None:
            access_token = self.establish_connection(zvm_host, port)

        args['access_token'] = access_token
        
        args['url'] = "https://{}:{}/v1/events".format(zvm_host, port)
        args['method'] = "get"

        req_data = zerto_api.addArgs(**args)
        resp = zerto_api.makeRequest(**req_data)

        myresp = {}
        myresp['status_code'] = resp.status_code
        try:
            myresp['data'] = json.loads(resp.content.rstrip())
        except ValueError:
            myresp['data'] = resp.content

        result = []
        if myresp['status_code'] >= 200 and myresp['status_code'] <= 299:
            ret = True
            for event in myresp['data']:
                vpgIdentifier = [ vpg for vpg in  event['Vpgs'] if vpg['VpgIdentifier']]
                if vpgIdentifier:
                    event_obj = {"description": event['Description'],
                                 "occurredOn": event['OccurredOn'],
                                 "eventType": event['EventType'],
                                 "eventIdentifier": event['EventIdentifier'],
                                 "vpgIdentifier": vpgIdentifier[0]['VpgIdentifier']}
                    result.append(event_obj)

        return (ret, result)
