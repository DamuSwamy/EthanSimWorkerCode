from st2common.runners.base_action import Action
from operator import itemgetter

class InsertAndUpdateListGeneratorV2Action(Action):
    def run(self, action, data, events, create_events):
        vm_list = []
        vm_disk_list = []
        vm_network_list = []
        if action == 'insert':
            for sub in sorted(data['VirtualMachines'], key=itemgetter('vmID'), reverse=True):
                insert = [dict(sub, vmCPUInitialSize=sub['vmCPU'], vmRAMInitialSize=sub['vmRAM'], vmCreatedBy=event['eventUser'], vmCreatedDate=event['eventDate'], vmCreatedSource=event['eventState']) for event in events if int(event['vmID']) == int(sub['vmID']) and event['eventType'] in create_events]
                if len(insert) > 1:
                    insert = [insert[0]]
                vm_list = vm_list + insert
            #vm_list = [dict(sub, vmCPUInitialSize=sub['vmCPU'], vmRAMInitialSize=sub['vmRAM']) for sub in data['VirtualMachines']]
            vm_disk_list = [dict(sub, vmDiskInitialSize=sub['vmDiskSize'],inactiveDt='9999-12-31 23:59:59') for sub in data['VMDisks']]
            vm_network_list = data['VMNetworks']

        if action == 'remove':
            vm_obj = {}
            vm_disk_obj = {}
            for event in events:
                if 'ethvmid' in event.keys() and event['eventType'] in ['VmRemovedEvent', 'VmDecommisionedEvent']:
                    ethvmid = event['ethvmid']
                    vm_obj[ethvmid] = {"_ethvmid": ethvmid,
                                       "_vmID": event['vmID'],
                                       "vmActive": False,
                                       "vmRemovedBy": event['eventUser'],
                                       "vmRemovedDate": event['eventDate']}
                    vm_disk_obj[ethvmid+"_disk"] = {"_ethvmid": ethvmid,
                                                    "_vmID": event['vmID'],
                                                    "_inactiveDt": '9999-12-31 23:59:59',
                                                    "inactiveDt": event['eventDate'],
                                                    "lastUpdated": event['eventDate']}

            vm_disk_list = list(vm_disk_obj.values())
            vm_list = list(vm_obj.values())
 
        return {"vm": vm_list,"vmdisk": vm_disk_list, "vmnetwork": vm_network_list}
