from st2common.runners.base_action import Action
from operator import itemgetter
from datetime import datetime

class InsertAndUpdateListGeneratorAction(Action):
    def run(self, db_data, vc_data, data_type, events, create_events):
        update_list = []
        insert_list = []
        remove_list = []
        if data_type == 'vm':
            required = ['_ethvmid','_vmID', 'vmID','ethvmid','vmActive', 'vmName', 'vmHostName', 'vmIPAddress', 'vmCPU', 'vmRAM', 'vmStorageUsed', 'vmStorageTotal', 'vmPowerState', 'vmVersion', 'vmGuestToolsStatus', 'vmGuestToolsVersionStatus', 'vmGuestToolsRunningStatus', 'vmGuestState', 'lastUpdated']
            vm_data = [{key : val for key, val in sub.items() if key in required} for sub in vc_data]
            for y in sorted(db_data, key=itemgetter('ethvmid', 'vmID'), reverse=True):
                update = [sub for sub in vm_data if sub['ethvmid'] == y['ethvmid'] and int(sub['vmID']) == int(y['vmID'])]
 
                if len(update) <= 0:
                    y['_ethvmid'] = y['ethvmid']
                    y['_vmID'] = y['vmID']
                    y['vmActive'] = False
                    remove_list.append(y)
                else:
                    update_list = update_list + update
            for z in sorted(vc_data, key=itemgetter('ethvmid'), reverse=True):
                exist = [sub for sub in db_data if sub['ethvmid'] == z['ethvmid']]
                if len(exist) > 0:
                    continue
                for event in events:
                    if event['vmID'] == z['vmID'] and event['eventType'] in create_events:
                        z['vmCreatedBy'] = event['eventUser']
                        z['vmCreatedDate'] = event['eventDate']
                        z['vmCreatedSource'] = event['eventState']
                        break
                z['vmCPUInitialSize'] = z['vmCPU']
                z['vmRAMInitialSize'] = z['vmRAM']
                insert_list.append(z)

        if data_type == 'vm_disk':
            required = ['_ethvmid', '_vmID','_deviceKey','vmName','ethvmid','vmID','deviceKey','vmDiskSize', 'vmDiskTier', 'vmDiskDatastore', 'deviceID', 'lastUpdated', 'vmDiskFileName']
            disk_data = [{key : val for key, val in sub.items() if key in required} for sub in vc_data]
            for y in sorted(db_data, key=itemgetter('ethvmid', 'vmID', 'deviceKey'), reverse=True):
                update = [sub for sub in disk_data if sub['ethvmid'] == y['ethvmid'] and int(sub['vmID']) == int(y['vmID']) and  int(sub['deviceKey']) == int(y['deviceKey'])]
                if len(update) <= 0:
                    y['_ethvmid']    = y['ethvmid']
                    y['_vmID']       = y['vmID']
                    y['_deviceKey']  = y['deviceKey']
                    y['_inactiveDt'] = '9999-12-31 23:59:59' 
                    y['inactiveDt']  = y['lastUpdated']
                    y['lastUpdated'] = y['lastUpdated'] 
                    remove_list.append(y)
                else:
                    update_list = update_list + update

            for z in sorted(vc_data, key=itemgetter('ethvmid', 'deviceKey'), reverse=True):
                exist = [sub for sub in db_data if sub['ethvmid'] == z['ethvmid'] and int(sub['deviceKey']) == int(z['deviceKey'])]
                if len(exist) > 0:
                    continue
                z['inactiveDt'] = '9999-12-31 23:59:59'
                z['vmDiskInitialSize'] = z['vmDiskSize']
                insert_list.append(z)

        if data_type == 'vm_network':
            for z in sorted(vc_data, key=itemgetter('managedID', 'deviceKey'), reverse=True):
                exist = [sub for sub in db_data if sub['managedID'] == z['managedID'] and int(sub['deviceKey']) == int(z['deviceKey'])]
                if len(exist) > 0:
                    continue
                insert_list.append(z)

        return {"insert": insert_list, "update": update_list, "remove": remove_list}
