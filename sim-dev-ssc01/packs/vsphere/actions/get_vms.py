# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pyVmomi import vim  # pylint: disable-msg=E0611

from vmwarelib import inventory
from vmwarelib.actions import BaseAction
from vmwarelib.serialize import TemplateGetJSONEncoder
import json
from datetime import datetime
import re

class GetVMs(BaseAction):

    def run(self, ids=None, names=None, uuids=None, datastores=None,
            datastore_clusters=None, resource_pools=None,
            vapps=None, hosts=None, folders=None, clusters=None,
            datacenters=None, virtual_switches=None,
            no_recursion=False, get_all_vms=False, vsphere=None, vcenter_id=""):
        # TODO: food for thought. PowerCli contains additional
        # parameters that are not present here for the folliwing reason:
        # <server> - we may need to bring it in if we decide to have
        #            connections to more than 1 VC.
        # <tag>    - Tags in VC are not the same as tags you see in Web
        #            Client for the reason, that those tags are stored
        #            in Inventory Service only. PowerCli somehow can access
        #            it, from vSphere SDK there is no way.

        self.establish_connection(vsphere)

        props = ['config.guestFullName', 'name', 'runtime.powerState']
        moid_to_vm = {}

        if get_all_vms:
            empty   = ""
            all_vms = []
            '''
            results = {}
            container = inventory.get_virtualmachines(self.si_content)
            for vm in container.view:
                results[vm.name] = json.loads(json.dumps(vm.summary,
                                                           cls=TemplateGetJSONEncoder))
            return results
            '''
            container = inventory.get_virtualmachines(self.si_content)
            for vm in container.view:
                result = {}
                for customDef in vm.availableField:
                    if customDef.name == 'APPLICATION':
                        application_id            = customDef.key
                    elif customDef.name == 'ENVIRONMENT':
                        environment_id            = customDef.key
                    elif customDef.name == 'STIER':
                        storage_tier_id           = customDef.key
                    elif customDef.name == 'CUSTID':
                        customer_id               = customDef.key
                result['custidx']                 = empty.join([x.value for x in vm.customValue if x.key == customer_id])
                result['ethvmid']                 = str(vcenter_id) + vm.config.instanceUuid
                result['invVCServerID']           = vcenter_id
                result['vmID']                    = vm._GetMoId().replace('vm-', '')
                result['vmPersistentID']          = vm.config.instanceUuid
                result['vmUuid']                  = vm.config.uuid
                result['vmName']                  = vm.summary.config.name
                result['vmHostName']              = vm.guest.hostName
                result['vmIPAddress']             = vm.guest.ipAddress
                result['vmCPU']                   = vm.summary.config.numCpu
                result['vmRAM']                   = round(vm.summary.config.memorySizeMB/1024)
                result['vmStorageUsed']           = round(vm.summary.storage.committed/1073741824)
                result['vmStorageTotal']          = round((vm.summary.storage.committed/1073741824) + (vm.summary.storage.uncommitted/1073741824))
                if vm.runtime.powerState == 'poweredOff':
                    result['vmPowerState']        = 0
                elif vm.runtime.powerState == 'poweredOn':
                    result['vmPowerState']        = 1
                elif vm.runtime.powerState == 'Suspended':
                    result['vmPowerState']        = 2
                else:
                    result['vmPowerState']        = vm.runtime.powerState
                result['vmHost']                  = vm.runtime.host._moId
                result['vmConfiguredOS']          = vm.summary.config.guestFullName
                result['vmVersion']               = "v" + vm.config.version.split("-",1)[1]
                result['vmBootTime']              = vm.runtime.bootTime.strftime("%d-%m-%y %H:%M:%S.%f") if vm.runtime.bootTime is not None else None
                result['vmGuestToolsStatus']      = vm.guest.toolsStatus
                result['vmGuestToolsVersionStatus'] = vm.guest.toolsVersionStatus2
                result['vmGuestToolsRunningStatus'] = vm.guest.toolsRunningStatus
                result['vmGuestToolsVersion']     = vm.guest.toolsVersion
                result['vmGuestOSName']           = vm.summary.config.guestFullName
                result['vmGuestState']            = vm.guest.guestState
                result['vmResourcePool']          = vm.resourcePool.name
                result['vmConfigFile']            = vm.summary.config.vmPathName
                result['vmApplication']           = empty.join([x.value for x in vm.customValue if x.key == application_id])
                result['vmEnvironment']           = empty.join([x.value for x in vm.customValue if x.key == environment_id])
                result['vmCostCode']              = ""
                result['vmStorageTier']           = empty.join([x.value for x in vm.customValue if x.key == storage_tier_id])
                result['vmCIACName']              = ""
                result['vmCreatedBy']             = ""
                result['vmCreatedDate']           = ""
                result['vmCreatedSource']         = ""
                result['vmRemovedBy']             = ""
                result['vmRemovedDate']           = ""
                result['vmActive']                = True
                result['lastUpdated']             = datetime.now().strftime("%y-%m-%d %H:%M:%S")
                result['vmCPUReservation']        = vm.resourceConfig.cpuAllocation.reservation
                result['vmCPULimit']              = vm.resourceConfig.cpuAllocation.limit
                result['vmRAMReservation']        = vm.resourceConfig.memoryAllocation.reservation
                result['vmRAMLimit']              = vm.resourceConfig.memoryAllocation.limit
                disks                             = vm.config.hardware.device
                disk_array = []
                for disk in disks:
                    device_type                   = type(disk).__name__
                    if disk.backing is None and device_type != 'vim.vm.device.VirtualDisk':
                        continue
                    disk_obj = {}
                    if hasattr(disk.backing, 'fileName'):
                        datastore = disk.backing.datastore
                        if datastore:
                            disk_obj['vmDatastoreID']     = disk.backing.datastore._GetMoId()
                            disk_obj['vmDiskName']        = disk.deviceInfo.label
                            if hasattr(disk, 'capacityInKB'):
                                disk_obj['vmDiskSize']    = round(disk.capacityInKB/1048576)
                            else:
                                disk_obj['vmDiskSize']    = 0
                            disk_obj['vmDiskDatastore']   = re.match("\[(.*?)\]",disk.backing.fileName).group(1)
                            disk_obj['vmDiskFileName']    = disk.backing.fileName
                            disk_obj['vmDiskUnit']        = disk.unitNumber
                            disk_obj['deviceKey']         = disk.key
                            disk_obj['vmDiskFormat']      = ""
                            disk_array.append(disk_obj)
                result['vmDisks']                 = disk_array                
                networks                          = vm.guest.net
                network_array = []
                for network in networks:
                    if network.deviceConfigId > 0:
                        network_obj = {}
                        network_obj['network']    = network.network
                        network_obj['macAddress'] = network.macAddress
                        network_obj['connected']  = network.connected
                        network_obj['deviceKey']  = network.deviceConfigId
                        if hasattr(network.ipConfig, 'ipAddress'):
                            network_obj['ipAddress']  = empty.join([ip.ipAddress for ip in network.ipConfig.ipAddress if ip.state == 'preferred'])
                        else:
                            network_obj['ipAddress']  = ""
                        network_array.append(network_obj)
                result['vmNetworks']              = network_array      
                all_vms.append(result)
            return all_vms

        # getting vms by their moids
        vms_from_moids = []
        if ids:
            container = self.si_content.viewManager.CreateContainerView(
                self.si_content.rootFolder, [vim.VirtualMachine], True)
            for vm in container.view:
                moid = str(vm).split(':')[1].replace('\'', '')
                if moid in ids:
                    vms_from_moids.append(vm)
            GetVMs.__add_vm_properties_to_map_from_vm_array(moid_to_vm,
                                                            vms_from_moids)

        # getting vms by their names
        vms_from_names = []
        if names:
            container = self.si_content.viewManager.CreateContainerView(
                self.si_content.rootFolder, [vim.VirtualMachine], True)
            for vm in container.view:
                if vm.name in names:
                    vms_from_names.append(vm)
            GetVMs.__add_vm_properties_to_map_from_vm_array(
                moid_to_vm, vms_from_names)

        # getting vms by their uuids
        vms_from_uuids = []
        if uuids:
            container = self.si_content.viewManager.CreateContainerView(
                self.si_content.rootFolder, [vim.VirtualMachine], True)
            for vm in container.view:
                if vm.config.uuid in uuids:
                    vms_from_uuids.append(vm)
            GetVMs.__add_vm_properties_to_map_from_vm_array(moid_to_vm,
                                                            vms_from_uuids)

        # getting vms from datastore objects
        vms_from_datastores = []
        if datastores:
            vim_datastores = [vim.Datastore(moid, stub=self.si._stub)
                              for moid in datastores]
            for ds in vim_datastores:
                vms_from_datastores.extend(ds.vm)
            GetVMs.__add_vm_properties_to_map_from_vm_array(
                moid_to_vm, vms_from_datastores)

        # getting vms from datastore cluster objects
        vms_from_datastore_clusters = []
        if datastore_clusters:
            vim_datastore_clusters = [
                vim.StoragePod(moid, stub=self.si._stub)
                for moid in datastore_clusters
            ]
            for ds_cl in vim_datastore_clusters:
                for ds in ds_cl.childEntity:
                    vms_from_datastore_clusters.extend(ds.vm)
            GetVMs.__add_vm_properties_to_map_from_vm_array(
                moid_to_vm, vms_from_datastore_clusters)

        # getting vms from virtual switch objects
        vms_from_virtual_switches = []
        if virtual_switches:
            vim_virtual_switches = [
                vim.DistributedVirtualSwitch(moid, stub=self.si._stub)
                for moid in virtual_switches
            ]
            for vswitch in vim_virtual_switches:
                for pg in vswitch.portgroup:
                    vms_from_virtual_switches.extend(pg.vm)
            GetVMs.__add_vm_properties_to_map_from_vm_array(
                moid_to_vm, vms_from_virtual_switches)

        # getting vms from containers (location param)
        vms_from_containers = []
        containers = []

        if resource_pools:
            containers += [vim.ResourcePool(moid, stub=self.si._stub)
                           for moid in resource_pools]

        if vapps:
            containers += [vim.VirtualApp(moid, stub=self.si._stub)
                           for moid in vapps]

        if hosts:
            containers += [vim.HostSystem(moid, stub=self.si._stub)
                           for moid in hosts]

        if folders:
            containers += [vim.Folder(moid, stub=self.si._stub)
                           for moid in folders]

        if clusters:
            containers += [vim.ComputeResource(moid, stub=self.si._stub)
                           for moid in clusters]

        if datacenters:
            containers += [vim.Datacenter(moid, stub=self.si._stub)
                           for moid in datacenters]

        for cont in containers:
            objView = self.si_content.viewManager.CreateContainerView(
                cont, [vim.VirtualMachine], not no_recursion)
            tSpec = vim.PropertyCollector.TraversalSpec(
                name='tSpecName', path='view', skip=False,
                type=vim.view.ContainerView)
            pSpec = vim.PropertyCollector.PropertySpec(
                all=False, pathSet=props, type=vim.VirtualMachine)
            oSpec = vim.PropertyCollector.ObjectSpec(
                obj=objView, selectSet=[tSpec], skip=False)
            pfSpec = vim.PropertyCollector.FilterSpec(
                objectSet=[oSpec], propSet=[pSpec],
                reportMissingObjectsInResults=False)
            retOptions = vim.PropertyCollector.RetrieveOptions()
            retProps = self.si_content.propertyCollector.RetrievePropertiesEx(
                specSet=[pfSpec], options=retOptions)
            vms_from_containers += retProps.objects
            while retProps.token:
                retProps = self.si_content.propertyCollector.\
                    ContinueRetrievePropertiesEx(
                        token=retProps.token)
                vms_from_containers += retProps.objects
            objView.Destroy()

        for vm in vms_from_containers:
            if vm.obj._GetMoId() not in moid_to_vm:
                moid_to_vm[vm.obj._GetMoId()] = {
                    "moid": vm.obj._GetMoId(),
                    "name": vm.propSet[1].val,
                    "os": vm.propSet[0].val,
                    "runtime.powerState": vm.propSet[2].val
                }
        return list(moid_to_vm.values())

    @staticmethod
    def __add_vm_properties_to_map_from_vm_array(vm_map, vm_array):
        for vm in vm_array:
            if vm._GetMoId() not in vm_map:
                vm_map[vm._GetMoId()] = {
                    "moid": vm._GetMoId(),
                    "name": vm.name,
                    "os": vm.config.guestFullName,
                    "runtime.powerState": vm.runtime.powerState,
                    "hostName": vm.guest.hostName,
                    "ipAddress": vm.guest.ipAddress,
                    "vmPersistentID": vm.config.instanceUuid,
                    "vmUuid": vm.config.uuid
                }
