from st2common.runners.base_action import Action
from operator import itemgetter
from itertools import groupby
from datetime import datetime, timedelta
from dateutil import tz
import pytz

class TransformBackupDataAction(Action):
    def run(self, backup_array, ignore_list, ignore_list_from_validation=[]):
        backup_failure_array = backup_array['debug_failures']
        backup_success_array = backup_array['debug_success']
        failures = sorted(backup_failure_array,
                          key = itemgetter('backupServer'))
        successes = sorted(backup_success_array,
                          key = itemgetter('backupServer'))

        # Display data grouped by backupserver
        ignore = []
        result = {}
        success_result = {}
        remediation = {}
        ticket_remediation_list = []
        ignore_list_no_activity = []
        #required = ['clientName', 'pluginName', 'backupGroup', 'schedule', 'custid']
        for key, value in groupby(failures,
                                  key = itemgetter('backupServer')):
            groupby_list = []
            for k in value:
               groupby_list.append(k)
            result[key] = groupby_list

        for key, value in groupby(successes,
                                  key = itemgetter('backupServer')):
            success_groupby_list = []
            for k in value:
                success_groupby_list.append(k)
            success_result[key] = success_groupby_list


        for server in ignore_list_from_validation:
            if server in success_result.keys():
                ignore_list_from_validation.remove(server)
                continue
            elif server in result.keys():
                ignore_list_from_validation.remove(server)
                continue
            ignore_list_no_activity.append(server)

        # Segregate the data for ignore and action list
        for failure in result.keys():
            if not failure in ignore_list and len(result[failure]) >= 10:
                count = 0
                for failed in result[failure]:
                    startTime_str = failed['startTime']
                    startTime = datetime.strptime(startTime_str, '%Y-%m-%d %H:%M:%S')
                    startTime = startTime.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Australia/Sydney')).replace(second=0, microsecond=0).replace(tzinfo=None)
                    endTime = datetime.now(tz.tzlocal()).replace(second=0, microsecond=0).replace(tzinfo=None)
                    time_diff_x = int((endTime - startTime).total_seconds())
                    if time_diff_x < 1860:
                        count = count + 1
                    if count >= 10:
                        ignore.append(failure)
                        break
            #remediation[failure] = [{key : val for key, val in sub.items() if key in required} for sub in result[failure]]
            #remediation[failure] = result[failure]

        ignore_list += ignore

        if len(backup_failure_array) <= 0 and len(backup_success_array) <= 0:
            ignore_list_no_activity = ignore_list_from_validation

        ignore = [*set(ignore)]
        ignore_list_no_activity = [*set(ignore_list_no_activity)]
        ignore_list = [*set(ignore_list)]

        #remediation = [sub for sub in backup_failure_array if not sub['backupServer'] in ignore_list and sub['status'] == 'failed' and 'VMware Image' in sub['pluginName']]

        return { "bulk_failures": ignore, "no_activity": ignore_list_no_activity, "final_ignore_list": ignore_list }
