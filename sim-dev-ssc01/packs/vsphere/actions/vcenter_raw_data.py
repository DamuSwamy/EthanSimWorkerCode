from vmwarelib import inventory
from vmwarelib.actions import BaseAction
from datetime import datetime
from pyVmomi import vim
import json
import re

class VcenterRawData(BaseAction):
    def run(self, vsphere, vcenter_id, get_vms=False, get_hosts=False, get_rps=False, get_folders=False, get_tags=False):
        self.establish_connection(vsphere)
        vms               = []
        hosts             = []
        resouce_pools     = []
        folders           = []
        tags              = {}
        if get_vms:
            vms           = self.get_all_vms()
        if get_hosts:
            hosts         = self.get_all_hosts()
        if get_rps:
            resouce_pools = self.get_all_resource_pools()
        if get_folders:
            folders       = self.get_all_folders()
        if get_tags:
            tags          = self.get_all_tags()


        return {"VirtualMachines": vms,
                "Hosts": hosts,
                "ResourcePools": resouce_pools,
                "Folders": folders,
                "Categories": tags}

    def get_all_vms(self):
        vm_list = []
        empty   = ""
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
            result['vmHost']                  = vm.runtime.host.name
            result['vmConfiguredOS']          = vm.summary.config.guestFullName
            result['vmVersion']               = "v" + vm.config.version.split("-",1)[1]
            result['vmBootTime']              = vm.runtime.bootTime.strftime("%d-%m-%y %H:%M:%S.%f") if vm.runtime.bootTime is not None else None
            result['vmGuestToolsStatus']      = vm.guest.toolsStatus
            result['vmGuestToolsVersionStatus'] = vm.guest.toolsVersionStatus2
            result['vmGuestToolsRunningStatus'] = vm.guest.toolsRunningStatus
            result['vmGuestToolsVersion']     = vm.guest.toolsVersion
            result['vmGuestOSName']           = vm.summary.config.guestFullName
            result['vmGuestState']            = vm.guest.guestState
            result['vmResourcePool']          = vm.resourcePool
            if vm.resourcePool is not None:
                result['vmResourcePool']      = vm.resourcePool.name
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
                    if datastore and disk.key < 3000:
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
            vm_list.append(result)
        return vm_list
    
    def get_all_hosts(self):
        results_arr = []
        container = inventory.get_managed_entities(self.si_content, vim.HostSystem)
        for host in container.view:
            results = {}
            results['hostName']   = host.name
            results['hostID']     = host._GetMoId()
            results_arr.append(results)
        return results_arr

    def get_all_resource_pools(self):
        results_arr = []
        container = inventory.get_managed_entities(self.si_content, vim.ResourcePool)
        for resource_pool in container.view:
            results = {}
            results['rpName']   = resource_pool.name
            results['rpID']     = resource_pool._GetMoId()
            results['rpParent'] =  resource_pool.parent._GetMoId()
            results_arr.append(results)
        return results_arr

    def get_all_folders(self):
        results_arr = []
        container = inventory.get_managed_entities(self.si_content, vim.Folder)
        for folder in container.view:
            results = {}
            results['folderName']   = folder.name
            results['folderID']     = folder._GetMoId()
            results['folderParent'] = folder.parent._GetMoId()
            results_arr.append(results)
        return results_arr

    def get_all_tags(self):
        category_list = self.tagging.category_list()
        category_obj_array = []
        result_obj = {}
        for category_id in category_list:
            category = self.tagging.category_get(category_id)
            category_obj = {}
            category_obj['id']          = category['id']
            category_obj['name']        = category['name']
            category_obj['description'] = category['description']
            category_obj['tags']        = {}
            category_obj['vCenterID']   = vcenter_id
            tag_list = self.tagging.tag_list(category_id)
            tag_obj_array = []
            for tag_id in tag_list:
                tag = self.tagging.tag_get(tag_id)
                tag_objects = self.tagging.tag_association_list_attached_objects(tag_id)
                tag_obj_array.append(self.transform(tag, tag_objects))
            category_obj['tags']['tag'] = tag_obj_array
            category_obj_array.append(category_obj)
        result_obj['category'] = category_obj_array
        return result_obj

    def transform(self, tag_info, tag_objects):
        tag = {}
        tag['tagID']              = tag_info['id']
        tag['tagName']            = tag_info['name']
        tag['tagDescription']     = tag_info['description']
        tag['categoryID']         = tag_info['category_id']
        tagDatastore              = []
        tagVM                     = []
        for obj in tag_objects:
            if obj['type'] == 'Datastore':
                tagDatastore.append(obj['id'])
            if obj['type'] == 'VirtualMachine':
                tagVM.append(obj['id'])
        if len(tagDatastore) > 0:
            tag['tagDatastores'] = {}
            tag['tagDatastores']['tagDatastore'] = tagDatastore

        if len(tagVM) > 0:
            tag['tagVMs']= {}
            tag['tagVMs']['tagVM'] = tagVM
        return tag
