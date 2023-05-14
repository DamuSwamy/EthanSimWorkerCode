from vmwarelib import inventory
from vmwarelib.actions import BaseAction
from datetime import datetime, timedelta
from pyVmomi import vim, vmodl
import re
import pytz

#ref https://gist.github.com/prziborowski/65872c4c32e850495cdd16d366200830, https://github.com/vmware/pyvmomi/issues/743

class VcenterEvents(BaseAction):
    def run(self, vsphere, vcenter_id, event_period, event_type_filters, creation_events, update_events, exclude_user_events, vm_ignore_list):
        self.establish_connection(vsphere)
        self.vcenter_id = vcenter_id
        self.creation_events = creation_events
        self.update_events = update_events
        events_array    = []
        moid_to_event   = {}
        end_time        = datetime.now()
        #end_time        = datetime.strptime('2023-02-19 00:00:01', '%Y-%m-%d %H:%M:%S')
        end_time        = end_time.astimezone(pytz.timezone('Australia/Sydney'))
        start_time      = end_time - timedelta(hours=event_period)
        start_time      = start_time.astimezone(pytz.timezone('Australia/Sydney'))
        print(start_time)
        print(end_time)
        #event_type_filters = ['VmClonedEvent', 'VmCreatedEvent', 'VmDeployedEvent', 'VmRegisteredEvent', 'VmConnectedEvent', 'VmDiscoveredEvent']
        filter_time     = vim.event.EventFilterSpec.ByTime(beginTime=start_time, endTime=end_time)
        filter_spec     = vim.event.EventFilterSpec(eventTypeId=event_type_filters, time=filter_time)
        event_manager   = self.si_content.eventManager
        '''
        collector       = event_manager.QueryEvents(filter_spec)
        for e in collector:
            if any([x in e.vm.name for x in vm_ignore_list]) or any([x in e.userName for x in exclude_user_events]):
                continue
            events_array.append(e)'''
        event_collector       = event_manager.CreateCollectorForEvents(filter_spec)
        try:
            page_size = 1000 # The default and also the max event number per page till vSphere v6.5, you can change it to a smaller value by SetCollectorPageSize().
            events = []

            while True:
                events_in_page = event_collector.ReadNextEvents(page_size)
                num_event_in_page = len(events_in_page)
                if num_event_in_page == 0:
                    break
                events.extend(events_in_page) # or do other things on the collected events
        finally:
            event_collector.DestroyCollector()

        for e in events:
            if any([x in e.vm.name for x in vm_ignore_list]) or any([x in e.userName for x in exclude_user_events]):
                continue
            events_array.append(e)
        return self._add_event_properties_to_map_from_event_array(moid_to_event, events_array)

    def _add_event_properties_to_map_from_event_array(self, event_map, event_array):
        for e in event_array:
            event_type = type(e).__name__
            event_type = e.eventTypeId if hasattr(e, 'eventTypeId') else event_type
            event_type = event_type.replace("vim.event.", "").replace("com.vmware.vc.HA.", "")
            evtidx = "{}-{}".format(str(self.vcenter_id), str(e.key))
            created_time = e.createdTime.astimezone(pytz.timezone('Australia/Sydney'))
            event_map[e.key] = {"evtidx": evtidx,
                                "eventID": e.key,
                                "vmName": e.vm.name,
                                "vmID": int(str(e.vm.vm).split("vm-")[1].replace("'","")),
                                "eventDate": created_time.strftime("%Y-%m-%d %H:%M:%S"),
                                "eventUser": e.userName,
                                "eventType": event_type,
                                "deviceType": "virtualMachine",
                                "eventOperation": event_type,
                                "eventState": "Unknown",
                                "deviceID": None,
                                "deviceKey": None}
            if event_type in self.creation_events:
                if event_type == 'VmConnectedEvent':
                    if hasattr(e, 'chainId'):
                        if e.fullFormattedMessage == 'event.VmConnectedEvent.fullFormat' or 'connected' in e.fullFormattedMessage:
                            event_map[e.key]['eventState'] = 'ERROR_Connected'
                        elif e.fullFormattedMessage == 'com.vmware.vc.vm.DstVmMigratedEvent' or 'migrated' in e.fullFormattedMessage:
                            event_map[e.key]['eventState'] = 'Migrated'
                        else:
                            event_map[e.key]['eventState'] = 'Immaculate Conception'
                else:
                    if(e.fullFormattedMessage == 'event.VmDeployedEvent.fullFormat' or e.fullFormattedMessage == 'event.VmRegisteredEvent.fullFormat' or 'deployed' in e.fullFormattedMessage or 'Registered' in e.fullFormattedMessage):
                        event_map[e.key]['eventState'] = 'Template'
                    elif e.fullFormattedMessage == 'event.VmCreatedEvent.fullFormat' or 'Created' in e.fullFormattedMessage:
                        event_map[e.key]['eventState'] = 'Manually'
                    elif e.fullFormattedMessage == 'event.VmClonedEvent.fullFormat' or 'Clone' in e.fullFormattedMessage or 'was cloned from' in e.fullFormattedMessage:
                        event_map[e.key]['eventState'] = 'Cloned'
                    elif e.fullFormattedMessage == 'event.VmDiscoveredEvent.fullFormat' or 'Discovered' in e.fullFormattedMessage:
                        event_map[e.key]['eventState'] = 'Discovered'
                    elif e.fullFormattedMessage == 'event.VmConnectedEvent.fullFormat' or 'connected' in e.fullFormattedMessage:
                        event_map[e.key]['eventState'] = 'ERROR_Connected'  
                    elif e.fullFormattedMessage == 'event.VmRemovedEvent.fullFormat' or 'Removed' in e.fullFormattedMessage:
                        event_map[e.key]['eventState'] = 'Decommissioned'
                    else:
                        event_map[e.key]['eventState'] = 'Immaculate Conception'
            
                if e.fullFormattedMessage == 'com.vmware.vc.vm.DstVmMigratedEvent' or 'migrated' in e.fullFormattedMessage:
                    if hasattr(e, 'arguments'):
                        for arg in e.arguments:
                            if hasattr(arg, 'oldMoRef'):
                                event_map[e.key]['vmID']   = arg['oldMoRef'].split("vm-")[1]
                                break
                        event_map[e.key]['eventType']  = 'VmDecommisionedEvent'
                        event_map[e.key]['eventState'] = 'Decommissioned'
            if event_type in self.update_events:
                if event_type == 'VmPoweredOffEvent':
                    event_map[e.key]['eventState']     = 'powerOff'
                    event_map[e.key]['eventOperation'] = 'powerOff'
                if (event_type == 'VmPoweredOnEvent' and e.key == e.chainId) or event_type == 'VmStartingEvent':
                    event_map[e.key]['eventState']     = 'powerOn'
                    event_map[e.key]['eventOperation'] = 'powerOn'
                if event_type == 'VmUnprotectedEvent':
                    matched = False
                    event_map[e.key]['eventType']     = e.eventTypeId
                    for x in event_map.values():
                        if x['eventType'] == 'VmMigratedEvent' and x['chainId'] == e.chainId:
                            matched = True
                            event_map[e.key]['eventState']     = 'Unprotected'
                            event_map[e.key]['eventOperation'] = 'vmMigrated'
                            break
                    if not matched:
                        event_map[e.key]['eventState']     = 'powerOff'
                        event_map[e.key]['eventOperation'] = 'powerOff'
                if event_type == 'VmReconfiguredEvent':
                    if e.configSpec.numCPUs:
                        event_map[e.key]['deviceType']     = 'numCPUs'
                        event_map[e.key]['eventState']     = e.configSpec.numCPUs
                        event_map[e.key]['eventOperation'] = 'change'
                        event_map[str(e.key)+'_mem']       = event_map[e.key]
                    if e.configSpec.memoryMB:
                        event_map[e.key]['deviceType']     = 'memoryMB'
                        event_map[e.key]['eventState']     = e.configSpec.memoryMB/1024
                        event_map[e.key]['eventOperation'] = 'change'
                        event_map[str(e.key)+'_cpu']       = event_map[e.key]
                    if len(e.configSpec.deviceChange) > 0:
                        device_config = []
                        for d in e.configSpec.deviceChange:
                            device_type                        = type(d.device).__name__
                            device_type                        = device_type.replace('vim.vm.device.', '')
                            event_map[e.key]['deviceType']     = device_type
                            event_map[e.key]['eventOperation'] = d.operation
                            if device_type == 'VirtualDisk':
                                device  = d.device
                                event_map[e.key]['eventState'] = device.capacityInKB
                                if d.operation == 'add':
                                    if hasattr(device, 'key'):
                                        if isinstance(device.key, int) and device.key < 0 and device.diskObjectId :
                                            event_map[e.key]['deviceKey'] = int(device.diskObjectId.split("-")[1])
                                            event_map[e.key]['deviceID']  = device.backing.fileName.rsplit('/', 1)[-1]
                                        elif isinstance(device.key, int) and device.key < 0 and 'diskObjectId = ' in e.fullFormattedMessage:
                                            try:
                                                objectId = re.match("[\s\S]+diskObjectId = \\\"(.*?)\\\"",e.fullFormattedMessage).group(1)
                                                event_map[e.key]['deviceKey'] = int(objectId.split("-")[1])
                                            except Exception as e:
                                                event_map[e.key]['deviceKey'] = None
                                            try:
                                                deviceId = re.match("[\s\S]+backing = \(fileName = \\\"(.*?)\\\"", e.fullFormattedMessage).group(1)
                                                event_map[e.key]['deviceID']  = deviceId.rsplit('/', 1)[-1]
                                            except Exception as e:
                                                event_map[e.key]['deviceID'] = None
                                        elif isinstance(device.key, int) and device.key < 0:
                                            event_map[e.key]['deviceKey'] = device.key
                                            event_map[e.key]['deviceID']  = device.backing.fileName.rsplit('/', 1)[-1]
                                else:
                                    event_map[e.key]['deviceKey'] = device.key
                                    event_map[e.key]['deviceID']  = device.backing.fileName.rsplit('/', 1)[-1]

                            else:
                                event_map[e.key]['eventState'] = 'Unknown'
                    if not e.configSpec.numCPUs and not e.configSpec.memoryMB and not len(e.configSpec.deviceChange) > 0:
                        event_map[e.key]['eventState'] = 'Unknown'
                if event_type == 'VmRenamedEvent':
                    event_map[e.key]['deviceID']       = e.oldName
                    event_map[e.key]['eventState']     = 'vmRename'
                    event_map[e.key]['eventOperation'] = 'vmRename'                   
                if event_map[e.key]['eventState'] == 'Unknown':
                    del event_map[e.key]
        event_list = list(event_map.values())
        final_list = [i for n, i in enumerate(event_list) if i not in event_list[n + 1:]]
        return final_list
