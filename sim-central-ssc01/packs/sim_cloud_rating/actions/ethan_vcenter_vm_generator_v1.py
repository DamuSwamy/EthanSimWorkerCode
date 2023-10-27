from st2common.runners.base_action import Action
from operator import itemgetter
from datetime import datetime

class InsertAndUpdateListGeneratorAction(Action):
    def run(self, db_data, vc_data, data_type, events, create_events):
        update_list = []
        insert_list = []
        remove_list = []
        if data_type == 'vm':
            required = ['_EthVmId','_VmId', 'VmId','EthVmId','VmActive', 'VmName', 'VmHostName', 'VmIPAddress', 'VmCpu', 'VmRam', 'VmStorageUsed', 'VmStorageTotal', 'VmPowerState', 'VmVersion', 'LastScanTime']
            vm_data = [{key : val for key, val in sub.items() if key in required} for sub in vc_data]
            for y in sorted(db_data, key=itemgetter('EthVmId', 'VmId'), reverse=True):
                update = [sub for sub in vm_data if sub['EthVmId'] == y['EthVmId'] and int(sub['VmId']) == int(y['VmId'])]
 
                if len(update) <= 0:
                    scan_date = [ event['Event_Date'] for event in events if event['EthVmId'] == y['EthVmId'] ]
                    if scan_date:
                        last_scan = scan_date[0]
                    else:
                        last_scan = y['LastScanTime']
                    y['_EthVmId'] = y['EthVmId']
                    y['_VmId'] = y['VmId']
                    y['VmActive'] = False
                    y['DecommDate'] = last_scan
                    remove_list.append(y)
                else:
                    update_list = update_list + update
            for z in sorted(vc_data, key=itemgetter('EthVmId'), reverse=True):
                exist = [sub for sub in db_data if sub['EthVmId'] == z['EthVmId']]
                if len(exist) > 0:
                    continue
                insert_list.append(z)

        if data_type == 'vm_disk':
            required = ['_EthVmId','_DeviceKey','EthVmId','DeviceId','DeviceKey','DiskName','DiskTier','DiskSize','DiskUsed', 'DiskDatastore', 'DiskFileName','LastScanTime']
            disk_data = [{key : val for key, val in sub.items() if key in required} for sub in vc_data]
            for y in sorted(db_data, key=itemgetter('EthVmId', 'VmId', 'DeviceKey'), reverse=True):
                update = [sub for sub in disk_data if sub['EthVmId'] == y['EthVmId'] and int(sub['VmId']) == int(y['VmId']) and  int(sub['DeviceKey']) == int(y['DeviceKey'])]
                if len(update) <= 0:
                    scan_date = [event['Event_Date'] for event in events if event['EthVmId'] == y['EthVmId'] and event['DeviceKey'] == y['DeviceKey']]
                    if scan_date:
                        last_scan = scan_date[0]
                    else:
                        last_scan = y['LastScanTime']
                    y['_EthVmId']     = y['EthVmId']
                    y['_VmId']        = y['VmId']
                    y['_DeviceKey']   = y['DeviceKey']
                    y['RemoveDate']   = last_scan
                    y['LastScanTime'] = last_scan
                    remove_list.append(y)
                else:
                    update_list = update_list + update

            for z in sorted(vc_data, key=itemgetter('EthVmId', 'DeviceKey'), reverse=True):
                exist = [sub for sub in db_data if sub['EthVmId'] == z['EthVmId'] and int(sub['DeviceKey']) == int(z['DeviceKey'])]
                if len(exist) > 0:
                    continue
                z['DiskInitial'] = z['DiskSize']
                z['CreateDate']  = z['LastScanTime']
                insert_list.append(z)

        return {"insert": insert_list, "update": update_list, "remove": remove_list}
