from st2common.runners.base_action import Action
from operator import itemgetter

class InsertAndUpdateListGeneratorV2Action(Action):
    def run(self, action, data, events, create_events):
        vm_list = []
        vm_disk_list = []
        if action == 'insert':
            for sub in sorted(data['VirtualMachines'], key=itemgetter('VmID'), reverse=True):
                insert = [sub for sub in event_list if int(event['VmId']) == int(sub['VmId']) and event['Event_Type'] in create_events for event in events]
                if len(insert) > 1:
                    insert = [insert[0]]
                vm_list += insert
            for sub in sorted(data['VmDisks'], key=itemgetter('EthVmId'), reverse=True):
                insert = [dict(sub, DiskInitial=sub['DiskSize'], CreatedDate=event['Event_Date']) for event in events if int(event['EthVmId']) == int(sub['EthVmId']) and event['DeviceKey'] == sub['DeviceKey']]
                if len(insert) > 1:
                    insert = [insert[0]]
                vm_disk_list += insert

        if action == 'remove':
            vm_obj = {}
            vm_disk_obj = {}
            for event in events:
                if 'EthVmId' in event.keys() and event['Event_Type'] in ['VmRemovedEvent', 'VmDecommisionedEvent']:
                    EthVmId = event['EthVmId']
                    if EthVmId:
                        vm_obj[EthVmId] = {"_EthVmId": EthVmId,
                                           "_VmId": event['VmId'],
                                           "VmActive": False,
                                           "DecommDate": event['Event_Date'],
                                           "DecommBy": event['Event_User']}
                        vm_disk_obj[EthVmId+"_disk"] = {"_EthVmId": EthVmId,
                                                        "RemoveDate": event['Event_Date']}

            vm_disk_list = list(vm_disk_obj.values())
            vm_list = list(vm_obj.values())
 
        return {"vm": vm_list,"vmdisk": vm_disk_list}
