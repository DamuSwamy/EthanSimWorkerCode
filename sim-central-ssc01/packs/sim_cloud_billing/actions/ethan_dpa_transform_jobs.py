from st2common.runners.base_action import Action
from datetime import datetime, date, timedelta
from operator import itemgetter

class TransformJobsAction(Action):
    def run(self, backup_clients_data, ccb_usage_data, billing_period=None):
        dpaclient_list = []
        unmatched_list = []
        if billing_period is None:
            today = date.today()
            first = today.replace(day=1)
            last_month = first - timedelta(days=1)
            billing_period = last_month.strftime("%Y%m")
        print(billing_period)
        for backup in sorted(backup_clients_data, key=itemgetter('Client'), reverse=True):
            if backup['Org'] is None or (backup['Org'].islower() and len(backup['Org']) != 4):
                try:
                    backup['Org'] = backup['group'].split('-')[0]
                except Exception as e:
                    if backup['domainName'] is None:
                        if '-' in backup['Client']:
                            domain = backup['Client'].split('-')[0]
                            if len(domain) <= 4:
                                backup['Org'] = domain.upper()
                    else:
                        backup['Org'] = backup['domainName'].rsplit('/', 1)[-1]
            elif backup['Org'] == "Mixed":
                backup['Org'] = backup['domainName'].rsplit('/', 1)[-1]
            if backup['Org'] is not None and len(backup['Org']) > 4 and backup['domainName'] is not None:
                backup['Org'] = backup['domainName'].rsplit('/', 1)[-1]
            backup_array = [dict(backup, Org=sub['Org'], FEA=sub['FEA'], billingPeriod=billing_period) for sub in sorted(ccb_usage_data, key=itemgetter('Client'), reverse=True) if backup['Client'] == sub['Client']]
            if not backup_array:
                backup['FEA'] = 0
                backup['billingPeriod'] = billing_period
                if backup['Org'] is None:
                    backup['Org'] = 'NONE'
                unmatched_list.append(backup)
            dpaclient_list = dpaclient_list + backup_array
        return dpaclient_list + unmatched_list
