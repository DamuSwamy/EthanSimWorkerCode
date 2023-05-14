import json
from lib.actions import BaseAction
from lib import braas_api

class GetActivitiesAction(BaseAction):
    def run(self, braas, size=20, access_token=None):
        ret = False
        args = {}
        activity_array = []
        backup_server = self.config['braas'].get(braas)['host']
        if access_token is None:
            access_token = self.establish_connection(braas)

        args['access_token'] = access_token

        args['url'] = "https://{}/api/v1/activities?domain=%2F&duration=0&recursive=true&size={}".format(backup_server, size)
        args['method'] = "get"

        print(backup_server)
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
            for activity in myresp['data']['content']:
                stats = activity.pop("stats")
                if len(activity['queuedDate']) == 0:
                    activity['queuedDate'] = '9999-01-01T00:00:00Z'
                if len(activity['scheduledDate']) == 0:
                    activity['scheduledDate'] = '9999-01-01T00:00:00Z'
                if len(activity['activatedDate']) == 0:
                    activity['activatedDate'] = '9999-01-01T00:00:00Z'
                if len(activity['completedDate']) == 0:
                    activity['completedDate'] = '9999-01-01T00:00:00Z'
                if stats is not None:
                    for key, value in stats.items():
                        keyarray       = [*key]
                        keyFirstLetter = keyarray[0].upper()
                        keyarray.pop(0)
                        keyarrayStr    = "".join(keyarray)
                        activity['stats'+keyFirstLetter+keyarrayStr] = value
                activity_array.append(activity)
        return (ret, activity_array)
