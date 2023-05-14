from st2common.runners.base_action import Action
from operator import itemgetter
from itertools import groupby

class TransformBackupDataAction(Action):
    def run(self, backup_failure_array):
        failures = sorted(backup_failure_array,
                          key = itemgetter('backupServer'))

        # Display data grouped by backupserver
        ignore_list = []
        result = {}
        remediation = {}
        #required = ['clientName', 'pluginName', 'backupGroup', 'schedule', 'custid']
        for key, value in groupby(failures,
                                  key = itemgetter('backupServer')):
            groupby_list = []
            for k in value:
               groupby_list.append(k)
            result[key] = groupby_list
        # Segregate the data for ignore and action list
        for failure in result.keys():
            if len(result[failure]) >= 10:
                ignore_list.append(failure)
                continue
            #remediation[failure] = [{key : val for key, val in sub.items() if key in required} for sub in result[failure]]
            remediation[failure] = result[failure]

        return { "ignore": ignore_list, "remediation": remediation }
