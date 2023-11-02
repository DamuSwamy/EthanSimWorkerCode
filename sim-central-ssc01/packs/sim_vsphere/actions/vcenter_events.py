from vmwarelib import inventory
from vmwarelib.actions import BaseAction
from datetime import datetime, timedelta
from pyVmomi import vim, vmodl
import re
import pytz

#ref https://gist.github.com/prziborowski/65872c4c32e850495cdd16d366200830, https://github.com/vmware/pyvmomi/issues/743

class VcenterEvents(BaseAction):
    def run(self, vsphere, vcenter_id, event_period, event_type_filters, creation_events, update_events, exclude_user_events, vm_ignore_list, filter_by_vm_ids=[]):
        self.establish_connection(vsphere)
        self.vcenter_id = vcenter_id
        self.creation_events = creation_events
        self.update_events = update_events
        events_array    = []
        moid_to_event   = {}
        end_time        = datetime.now()
        end_time        = end_time.astimezone(pytz.timezone('Australia/Sydney'))
        start_time      = end_time - timedelta(hours=event_period)
        start_time      = start_time.astimezone(pytz.timezone('Australia/Sydney'))
        test = False
        if test:
            #event_type_filters = ['VmReconfiguredEvent'] 
            start_time = '2023-10-15 05:00:00'
            end_time   = '2023-10-16 23:59:59'
            start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
            end_time   = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
            start_time = start_time.astimezone(pytz.timezone('Australia/Sydney'))
            end_time   = end_time.astimezone(pytz.timezone('Australia/Sydney'))
        events = []
        if filter_by_vm_ids:
            #event_type_filters = ['VmReconfiguredEvent']
            #start_time = '2023-05-01 03:30:00'
            #end_time   = '2023-05-31 03:45:59'
            #start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
            #end_time   = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')'''
            container = self.si_content.viewManager.CreateContainerView(
                            self.si_content.rootFolder, [vim.VirtualMachine], True)
            for vm in container.view:
                moid = int(vm._GetMoId().replace('vm-', ''))
                if moid in filter_by_vm_ids:
                    by_entity    = vim.event.EventFilterSpec.ByEntity(entity=vm, recursion="self")
                    filter_spec = vim.event.EventFilterSpec(entity=by_entity, eventTypeId=self.creation_events)
                    event = self.event_collector(filter_spec)
                    events = events + event
        else:
            print(start_time)
            print(end_time)
            filter_time = vim.event.EventFilterSpec.ByTime(beginTime=start_time, endTime=end_time)
            filter_spec = vim.event.EventFilterSpec(eventTypeId=event_type_filters, time=filter_time)
            events = self.event_collector(filter_spec)

        for e in events:
            if any([x in e.vm.name for x in vm_ignore_list]) or any([x in e.userName for x in exclude_user_events]):
                continue
            events_array.append(e)
        return self._add_event_properties_to_map_from_event_array(moid_to_event, events_array)

    def event_collector(self, filter_spec):
        '''
        collector       = event_manager.QueryEvents(filter_spec)
        for e in collector:
            if any([x in e.vm.name for x in vm_ignore_list]) or any([x in e.userName for x in exclude_user_events]):
                continue
            events_array.append(e)'''
        event_collector       = self.si_content.eventManager.CreateCollectorForEvents(filter_spec)
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
        return events


    def _add_event_properties_to_map_from_event_array(self, event_map, event_array):
        for e in event_array:
            event_type = type(e).__name__
            event_type = e.eventTypeId if hasattr(e, 'eventTypeId') else event_type
            event_type = event_type.replace("vim.event.", "").replace("com.vmware.vc.HA.", "")
            evtidx = "{}-{}".format(str(self.vcenter_id), str(e.key))
            created_time = e.createdTime.astimezone(pytz.timezone('Australia/Sydney'))
            vmId = int(str(e.vm.vm).split("vm-")[1].replace("'",""))
            ethvmId = None
            if hasattr(e, 'configSpec') and hasattr(e.configSpec, 'instanceUuid') and e.configSpec.instanceUuid is not None:
                 ethvmId = str(self.vcenter_id) + str(self.vcenter_id) + e.configSpec.instanceUuid

            event_map[e.key] = {"VCServer": int(self.vcenter_id),
                                "EventId": e.key,
                                "EthVmId": ethvmId,
                                "VmId": vmId,
                                "Event_Date": created_time.strftime("%Y-%m-%d %H:%M:%S"),
                                "Event_Type": event_type,
                                "Device_Type": "virtualMachine",
                                "Event_Operation": event_type,
                                "Event_State": "Unknown",
                                "Event_User": e.userName,
                                "DeviceId": None,
                                "DeviceKey": None,
                                "DiskName": None,
                                "DiskTier": None,
                                "DiskSize": None,
                                "DiskUsed": None}
            if event_type in self.creation_events:
                if event_type == 'VmConnectedEvent':
                    if hasattr(e, 'chainId'):
                        if e.fullFormattedMessage == 'event.VmConnectedEvent.fullFormat' or 'connected' in e.fullFormattedMessage:
                            event_map[e.key]['Event_State'] = 'Connected'
                        elif e.fullFormattedMessage == 'com.vmware.vc.vm.DstVmMigratedEvent' or 'migrated' in e.fullFormattedMessage:
                            event_map[e.key]['Event_State'] = 'Migrated'
                        else:
                            event_map[e.key]['Event_State'] = 'Immaculate Conception'
                elif event_type == 'DrsVmMigratedEvent' or event_type == 'vim.event.DrsVmMigratedEvent':
                    event_map[e.key]['Event_Type']  = 'VmHostMigratedEvent'
                    event_map[e.key]['Event_State'] = 'HOST_Migrated'
                else:
                    if(e.fullFormattedMessage == 'event.VmDeployedEvent.fullFormat' or e.fullFormattedMessage == 'event.VmRegisteredEvent.fullFormat' or 'deployed' in e.fullFormattedMessage or 'Registered' in e.fullFormattedMessage):
                        event_map[e.key]['Event_State'] = 'Template'
                    elif e.fullFormattedMessage == 'event.VmCreatedEvent.fullFormat' or 'Created' in e.fullFormattedMessage:
                        event_map[e.key]['Event_State'] = 'Manually'
                    elif e.fullFormattedMessage == 'event.VmClonedEvent.fullFormat' or 'Clone' in e.fullFormattedMessage or 'was cloned from' in e.fullFormattedMessage:
                        event_map[e.key]['Event_State'] = 'Cloned'
                    elif e.fullFormattedMessage == 'event.VmDiscoveredEvent.fullFormat' or 'Discovered' in e.fullFormattedMessage:
                        event_map[e.key]['Event_State'] = 'Discovered'
                    elif e.fullFormattedMessage == 'event.VmConnectedEvent.fullFormat' or 'connected' in e.fullFormattedMessage:
                        event_map[e.key]['Event_State'] = 'ERROR_Connected'  
                    elif e.fullFormattedMessage == 'event.VmRemovedEvent.fullFormat' or 'Removed' in e.fullFormattedMessage:
                        """validDecommEvent = False
                        for x in event_map.values():
                            if x['Event_Type'] == 'VmPoweredOffEvent' and int(x['vmID']) == int(str(e.vm.vm).split("vm-")[1].replace("'","")):
                                validDecommEvent = True
                                break
                        if not validDecommEvent:
                            event_map[e.key]['Event_State']     = 'Invalid Decommissioned'
                            event_map[e.key]['Event_Type']      = 'Invalid VmRemovedEvent'
                            event_map[e.key]['Device_Type']     = 'Invalid virtualMachine'
                            event_map[e.key]['Event_Operation'] = 'Invalid VmRemovedEvent'
                        else:"""
                        event_map[e.key]['Event_State']     = 'Decommissioned'

                    else:
                        event_map[e.key]['Event_State'] = 'Immaculate Conception'
            
                if e.fullFormattedMessage == 'com.vmware.vc.vm.DstVmMigratedEvent' or 'migrated' in e.fullFormattedMessage:
                    if hasattr(e, 'arguments'):
                        for arg in e.arguments:
                            if hasattr(arg, 'oldMoRef'):
                                event_map[e.key]['VmId']   = arg['oldMoRef'].split("vm-")[1]
                                break
                        event_map[e.key]['Event_Type']  = 'VmMigratedEvent'
                        event_map[e.key]['Event_State'] = 'Migrated'
                        if hasattr(e, 'chainId'):
                            event_map[e.key]['chainId']    = e.chainId
            if event_type in self.update_events:
                if event_type == 'VmPoweredOffEvent':
                    event_map[e.key]['Event_State']     = 'powerOff'
                    event_map[e.key]['Event_Operation'] = 'powerOff'
                if (event_type == 'VmPoweredOnEvent' and e.key == e.chainId) or event_type == 'VmStartingEvent':
                    event_map[e.key]['Event_State']     = 'powerOn'
                    event_map[e.key]['Event_Operation'] = 'powerOn'
                if event_type == 'VmUnprotectedEvent':
                    matched = False
                    event_map[e.key]['Event_Type']     = e.eventTypeId
                    for x in event_map.values():
                        if hasattr(e, 'chainId'):
                            if x['Event_Type'] == 'VmMigratedEvent' and 'chainId' in x and x['chainId'] == e.chainId:
                                matched = True
                                event_map[e.key]['Event_State']     = 'Unprotected'
                                event_map[e.key]['Event_Operation'] = 'vmMigrated'
                                break
                    if not matched:
                        event_map[e.key]['Event_State']     = 'powerOff'
                        event_map[e.key]['Event_Operation'] = 'powerOff'
                if event_type == 'VmReconfiguredEvent':
                    if e.configSpec.numCPUs:
                        event_map[e.key]['Device_Type']     = 'numCPUs'
                        event_map[e.key]['Event_State']     = e.configSpec.numCPUs
                        event_map[e.key]['Event_Operation'] = 'change'
                        event_map[str(e.key)+'_cpu']       = event_map[e.key]
                    if e.configSpec.memoryMB:
                        event_map[e.key]['Device_Type']     = 'memoryMB'
                        event_map[e.key]['Event_State']     = e.configSpec.memoryMB/1024
                        event_map[e.key]['Event_Operation'] = 'change'
                        event_map[str(e.key)+'_mem']       = event_map[e.key]
                    if len(e.configSpec.deviceChange) > 0:
                        device_config = []
                        for d in e.configSpec.deviceChange:
                            device_type                        = type(d.device).__name__
                            device_type                        = device_type.replace('vim.vm.device.', '')
                            event_map[e.key]['Device_Type']     = device_type
                            event_map[e.key]['Event_Operation'] = d.operation
                            if device_type == 'VirtualDisk':
                                device  = d.device
                                event_map[e.key]['Event_State'] = device.capacityInKB
                                event_map[e.key]['DiskName']    = device.deviceInfo.label if device.deviceInfo else ""
                                event_map[e.key]['DiskSize']    = device.capacityInKB

                                if device.backing:
                                    if device.backing.diskMode == 'independent_nonpersistent':
                                        event_map[e.key]['Event_State'] = 'Unknown'
                                else:
                                    continue
                                if d.operation == 'add':
                                    if hasattr(device, 'key'):
                                        if isinstance(device.key, int) and device.diskObjectId :
                                            event_map[e.key]['DeviceKey'] = int(device.diskObjectId.split("-")[1])
                                            event_map[e.key]['DeviceId']  = device.backing.fileName.rsplit('/', 1)[-1]
                                        elif isinstance(device.key, int) and 'diskObjectId = ' in e.fullFormattedMessage:
                                            try:
                                                objectId = re.match("[\s\S]+diskObjectId = \\\"(.*?)\\\"",e.fullFormattedMessage).group(1)
                                                event_map[e.key]['DeviceKey'] = int(objectId.split("-")[1])
                                            except Exception as e:
                                                event_map[e.key]['DeviceKey'] = 'Unknown'
                                            try:
                                                deviceId = re.match("[\s\S]+backing = \(fileName = \\\"(.*?)\\\"", e.fullFormattedMessage).group(1)
                                                event_map[e.key]['DeviceId']  = deviceId.rsplit('/', 1)[-1]
                                            except Exception as e:
                                                event_map[e.key]['DeviceId'] = 'Unknown'
                                        elif isinstance(device.key, int):
                                            event_map[e.key]['DeviceKey'] = device.key
                                            event_map[e.key]['DeviceId']  = device.backing.fileName.rsplit('/', 1)[-1]
                                        else:
                                            event_map[e.key]['DeviceKey'] = device.key
                                            event_map[e.key]['DeviceId']  = device.backing.fileName.rsplit('/', 1)[-1]
                                    if device.capacityInKB == 0:
                                        Event_State = re.match("[\s\S]+key = {0},.*summary.+\\\"(.*)KB\\\"\)".format(event_map[e.key]['DeviceKey']),e.fullFormattedMessage).group(1)
                                        event_map[e.key]['Event_State'] = int(Event_State.replace(",",""))
                                        event_map[e.key]['DiskSize']    = int(Event_State.replace(",",""))
                                else:
                                    event_map[e.key]['DeviceKey'] = device.key
                                    event_map[e.key]['DeviceId']  = device.backing.fileName.rsplit('/', 1)[-1]
                            else:
                                event_map[e.key]['Event_State'] = 'Unknown'
                    if not e.configSpec.numCPUs and not e.configSpec.memoryMB and not len(e.configSpec.deviceChange) > 0:
                        event_map[e.key]['Event_State'] = 'Unknown'
                if event_type == 'VmRenamedEvent':
                    event_map[e.key]['DeviceId']       = e.oldName
                    event_map[e.key]['Event_State']     = 'vmRename'
                    event_map[e.key]['Event_Operation'] = 'vmRename'                   
                if event_map[e.key]['Event_State'] == 'Unknown':
                    del event_map[e.key]
        event_list = list(event_map.values())
        final_list = [i for n, i in enumerate(event_list) if i not in event_list[n + 1:]]
        return final_list
