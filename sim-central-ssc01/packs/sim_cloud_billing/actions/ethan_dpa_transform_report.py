from st2common.runners.base_action import Action
from operator import itemgetter
from datetime import datetime, date, timedelta
from st2client.client import Client
from st2client.models import LiveAction

class ActionManager(object):
    def execute(self, server, action, params):
        client = Client(base_url="https://{}/".format(server))
        client.liveactions.create(LiveAction(action=action, parameters=params))

class TransformDpaDataAction(Action):
    def run(self, sql_vm_data, dpa_data, db_connection):
        self.dpaclient_list = []
        self.unmatched_list = []
        self.connection = db_connection
        self.count = 0
        today = date.today()
        first = today.replace(day=1)
        last_month = first - timedelta(days=1)
        bp_last_month = last_month.strftime("%Y-%m")
        bp_current_month = datetime.now().strftime("%Y-%m")
        billingPeriod = None
        i = 1
        for dpa in sorted(dpa_data, key=itemgetter('Client'), reverse=True):
            if i == 1:
                billingPeriod = dpa['billingPeriod']
                print("Cleaning up billing period {}".format(billingPeriod))
                self.cleanup(billingPeriod, 'brasDPA')
                i = i + 1
            dpa_array = [dict(dpa, vmName=sub['vmName'].lower(), FEP=sub['vmStorageTotal'] - sub['vmRAM']) for sub in sorted(sql_vm_data, key=itemgetter('vmName'), reverse=True) if dpa['Client'].lower() == sub['vmName'].lower() and dpa['Org'] == sub['Org'] and sub['vmActive']]
            if not dpa_array:
                dpa_array = [dict(dpa, vmName=sub['vmName'], FEP=sub['vmStorageTotal'] - sub['vmRAM']) for sub in sorted(sql_vm_data, key=itemgetter('vmName'), reverse=True) if '(' in sub['vmName'] and dpa['Client'].lower() == sub['vmName'].split(' (')[0].lower() and dpa['Org'] == sub['Org'] and sub['vmActive']]
                if not dpa_array:
                    dpa_array = [dict(dpa, vmName=sub['vmName'], FEP=sub['vmStorageTotal'] - sub['vmRAM']) for sub in sorted(sql_vm_data, key=itemgetter('vmName'), reverse=True) if sub['vmHostName'] is not None and dpa['Client'].lower() == sub['vmHostName'].lower() and dpa['Org'] == sub['Org'] and sub['vmActive']]
                    if not dpa_array:
                        dpa_array = [dict(dpa, vmName=sub['vmName'], FEP=sub['vmStorageTotal'] - sub['vmRAM']) for sub in sorted(sql_vm_data, key=itemgetter('vmName'), reverse=True) if dpa['Client'].lower() == sub['vmName'].lower() and dpa['Org'] == sub['Org'] and not sub['vmActive'] and (bp_last_month in sub['lastUpdated'] or bp_current_month in sub['lastUpdated'])]
                        if len(dpa_array) > 1:
                            dpa_array = [dpa_array[0]]
                        if not dpa_array:
                            dpa_array = [dict(dpa, vmName=sub['vmName'], FEP=sub['vmStorageTotal'] - sub['vmRAM']) for sub in sorted(sql_vm_data, key=itemgetter('lastUpdated'), reverse=True) if sub['vmHostName'] is not None and dpa['Client'].lower() == sub['vmHostName'].lower() and dpa['Org'] == sub['Org'] and not sub['vmActive'] and (bp_last_month in sub['lastUpdated'] or bp_current_month in sub['lastUpdated'])]
                            if len(dpa_array) > 1:
                                dpa_array = [dpa_array[0]]
                            if not dpa_array:
                                dpa_array = [dict(dpa, vmName=sub['vmName'], FEP=sub['vmStorageTotal'] - sub['vmRAM']) for sub in sorted(sql_vm_data, key=itemgetter('lastUpdated'), reverse=True) if sub['vmHostName'] is not None and dpa['Client'].lower() == sub['vmHostName'].lower() and dpa['Org'] == sub['Org'] and not sub['vmActive']]
                                if len(dpa_array) > 1:
                                    dpa_array = [dpa_array[0]]
            if not dpa_array:
                if dpa['Org'] == 'Mixed':
                    print("Excluding {}".format(dpa['Client']))
                    continue
                dpa['FEP'] = 0
                self.unmatched_list.append(dpa)
            self.dpaclient_list = self.dpaclient_list + dpa_array 
            if len(self.dpaclient_list) >= 500:
                print("Inserting DPAclient: {}".format(str(len(self.dpaclient_list))))
                self.insert_data(self.dpaclient_list, 'brasDPA')
        if len(self.dpaclient_list) < 500:
            print("Inserting DPAclient: {}".format(str(len(self.dpaclient_list))))
            self.insert_data(self.dpaclient_list, 'brasDPA')
        self.insert_data(self.unmatched_list, 'brasDPA')
        print("Inserting DPAclient Unmatched: {}".format(str(len(self.unmatched_list))))
        return {"dpaclients": self.count, "billingPeriod": billingPeriod }

    def insert_data(self, data, table_name):
        if len(data) > 0:
            am = ActionManager()
            am.execute("127.0.0.1",
                       "sql.insert_bulk",
                       {"connection": self.connection, "data": data, "table": table_name})
            self.count = self.count + len(data)
            self.dpaclient_list = []

    def cleanup(self, billing_period, table_name):
        am = ActionManager()
        am.execute("127.0.0.1",
                   "sql.query",
                   {"connection": self.connection, "query": "DELETE FROM {} WHERE billingPeriod='{}'".format(table_name, billing_period)})
