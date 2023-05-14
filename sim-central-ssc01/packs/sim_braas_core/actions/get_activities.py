import json
from lib.actions import BaseAction
from lib import braas_api
from datetime import datetime
import pytz
from dateutil import tz

class GetActivitiesAction(BaseAction):
    def run(self, braas, duration=24, size=20, braas_id=0, access_token=None):
        ret = False
        args = {}
        activity_array = []
        backup_server = self.config['braas'].get(braas)['host']
        if access_token is None:
            access_token = self.establish_connection(braas)

        args['access_token'] = access_token

        args['url'] = "https://{}/api/v1/activities?domain=%2F&duration={}&recursive=true&size={}".format(backup_server,duration,size)
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
                activity['id'] = '{}{}'.format(braas_id, activity['id'])
                groupId = activity.pop('groupId')
                scheduleDate = activity.pop('scheduledDate')
                if activity['children']:
                    activity['children'] = None
                if groupId is not None:
                    activity['gid'] = groupId
                else:
                    activity['gid'] = None
                stats = activity.pop("stats")
                if activity['allowOvertime']:
                    activity['allowOvertime'] = 'true'
                else:
                    activity['allowOvertime'] = 'false'
                if activity['canceling']:
                    activity['canceling'] = 'true'
                else:
                    activity['canceling'] = 'false'
                if activity['datasetOverride']:
                    activity['datasetOverride'] = 'true'
                else:
                    activity['datasetOverride'] = 'false'
                if activity['hardQuotaExceeded']:
                    activity['hardQuotaExceeded'] = 'true'
                else:
                    activity['hardQuotaExceeded'] = 'false'
                if activity['retentionPolicyOverride']:
                    activity['retentionPolicyOverride'] = 'true'
                else:
                    activity['retentionPolicyOverride'] = 'false'
                if activity['softQuotaExceeded']:
                    activity['softQuotaExceeded'] = 'true'
                else:
                    activity['softQuotaExceeded'] = 'false'
                if activity['queuedDate'] is not None:
                    if len(activity['queuedDate']) == 0:
                        activity['queuedDate'] = '9999-01-01T00:00:00Z'
                    else:
                        queuedDate = datetime.strptime(activity['queuedDate'], '%Y-%m-%dT%H:%M:%S.%fZ')
                        queuedDate = queuedDate.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Australia/Sydney'))
                        activity['queuedDate'] = queuedDate.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'Z'
                        #activity['queuedDate'] = activity['queuedDate']
                else:
                    activity['queuedDate'] = '9999-01-01T00:00:00Z'
                if scheduleDate is not None:
                    if len(scheduleDate) == 0:
                        activity['scheduleDate'] = '9999-01-01T00:00:00Z'
                    else:
                        scheduleDate = datetime.strptime(scheduleDate, '%Y-%m-%dT%H:%M:%S.%fZ')
                        scheduleDate = scheduleDate.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Australia/Sydney'))
                        activity['scheduleDate'] = scheduleDate.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'Z'
                else:
                    activity['scheduleDate'] = '9999-01-01T00:00:00Z'
                if activity['activatedDate'] is not None:
                    if len(activity['activatedDate']) == 0:
                        activity['activatedDate'] = '9999-01-01T00:00:00Z'
                    else:
                        activatedDate = datetime.strptime(activity['activatedDate'], '%Y-%m-%dT%H:%M:%S.%fZ')
                        activatedDate = activatedDate.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Australia/Sydney'))
                        activity['activatedDate'] = activatedDate.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'Z'
                else:
                    activity['activatedDate'] = '9999-01-01T00:00:00Z'
                if activity['completedDate'] is not None:
                    if len(activity['completedDate']) == 0:
                        activity['completedDate'] = '9999-01-01T00:00:00Z'
                    else:
                        completedDate = datetime.strptime(activity['completedDate'], '%Y-%m-%dT%H:%M:%S.%fZ')
                        completedDate = completedDate.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Australia/Sydney'))
                        activity['completedDate'] = completedDate.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'Z'
                else:
                    activity['completedDate'] = '9999-01-01T00:00:00Z'
                if 'estimatedBytes' in activity:
                    activity['estimatedBytes'] = round(int(activity['estimatedBytes'])/1024/1024)
                if stats is not None:
                    for key, value in stats.items():
                        keyarray       = [*key]
                        keyFirstLetter = keyarray[0].upper()
                        keyarray.pop(0)
                        keyarrayStr    = "".join(keyarray)
                        activity['stats'+keyFirstLetter+keyarrayStr] = value
                activity_array.append(activity)
        return (ret, activity_array)
