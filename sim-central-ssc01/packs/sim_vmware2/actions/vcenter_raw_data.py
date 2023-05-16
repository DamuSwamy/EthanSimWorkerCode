from vmwarelib import inventory
from vmwarelib.actions import BaseAction
from datetime import datetime
from pyVmomi import vim
import json
import re
import pytz

class VcenterRawData(BaseAction):
    def run(self, vsphere, vcenter_id, proxy_vcenters, get_vms=False, ids=[], get_vm_disks=False, get_vm_networks=False, get_hosts=False, get_rps=False, get_folders=False, get_tags=False, datastores=[], custids=[], vm_required_field_array=[], vmdisk_required_field_array=[], tag_filter=[]):
        self.datastores = datastores
        self.vcenter_id = int(vcenter_id)
        self.cust_ids   = custids
        self.vsphere    = vsphere
        self.ids        = ids
        self.proxy_vcenters = proxy_vcenters
        vm_networks = vm_disks = vms = hosts = resouce_pools = folders = tags = []
        if get_vms or get_hosts or get_rps or get_folders:
            self.establish_connection(vsphere)
        if get_vms:
            vms           = self.get_all_vms()
            if get_vm_disks and get_vm_networks:
                for sub in vms:
                    d_found = n_found = False
                    for key, val in sub.items():
                        if key == 'vmDisks':
                            d_found = True
                            vm_disks = vm_disks + [disk for disk in val]
                        if key == 'vmNetworks':
                            n_found = True
                            vm_networks = vm_networks + [network for network in val]
                        if d_found and n_found:
                            break
                vms = [{key : val for key, val in sub.items() if key != 'vmDisks' and key != 'vmNetworks'} for sub in vms]
            if get_vm_disks and not get_vm_networks:
                for sub in vms:
                    for key, val in sub.items():
                        if key == 'vmDisks':
                            vm_disks = vm_disks + [disk for disk in val]
                            break
            if get_vm_networks and not get_vm_disks:
                for sub in vms:
                    for key, val in sub.items():
                        if key == 'vmNetworks':
                            vm_networks = vm_networks + [network for network in val]
                            break
            else:
                vms = [{key : val for key, val in sub.items() if key != 'vmDisks' and key != 'vmNetworks'} for sub in vms]

            if vm_required_field_array:
                vms = [{key : val for key, val in sub.items() if key in vm_required_field_array} for sub in vms]
            if vmdisk_required_field_array:
                vm_disks = [{key : val for key, val in sub.items() if key in vmdisk_required_field_array} for sub in vm_disks]

        if get_hosts:
            hosts         = self.get_all_hosts()
        if get_rps:
            resouce_pools = self.get_all_resource_pools()
        if get_folders:
            folders       = self.get_all_folders()
        if get_tags:
            tags          = self.get_all_tags(tag_filter)

        return  {"VirtualMachines": vms,
                 "VMDisks": vm_disks,
                 "VMNetworks": vm_networks,
                 "Hosts": hosts,
                 "ResourcePools": resouce_pools,
                 "Folders": folders,
                 "Categories": tags}

    def get_all_vms(self):
        moid_to_vm = {}
        vm_array = []
        container = self.si_content.viewManager.CreateContainerView(
            self.si_content.rootFolder, [vim.VirtualMachine], True)
        for vm in container.view:
            if self.ids:
                moid = int(vm._GetMoId().replace('vm-', ''))
                if moid in self.ids:
                    vm_array.append(vm)
            else:
                vm_array.append(vm)
        self._add_vm_properties_to_map_from_vm_array(
            moid_to_vm, vm_array)
        return list(moid_to_vm.values())

    def _add_vm_properties_to_map_from_vm_array(self, vm_map, vm_array):
        for vm in vm_array:
            application_set = env_set = stier_set = cust_set = False
            application_id = environment_id = storage_tier_id = customer_id = ""
            for customDef in vm.availableField:
                if customDef.name == 'APPLICATION':
                    application_set           = True
                    application_id            = customDef.key
                elif customDef.name == 'ENVIRONMENT':
                    env_set                   = True
                    environment_id            = customDef.key
                elif customDef.name == 'STIER':
                    stier_set                 = True
                    storage_tier_id           = customDef.key
                elif customDef.name == 'CUSTID':
                    cust_set                  = True
                    customer_id               = customDef.key
                if application_set and env_set and stier_set and customer_id:
                    break

            if vm.runtime.powerState == 'poweredOff':
                vmPowerState = 0
            elif vm.runtime.powerState == 'poweredOn':
                vmPowerState = 1
            elif vm.runtime.powerState == 'suspended':
                vmPowerState = 2
            else:
                vmPowerState = vm.runtime.powerState

            vmResourcePool = vm.resourcePool
            if vm.resourcePool is not None:
                vmResourcePool = vm.resourcePool.name

            ethvmid = str(self.vcenter_id) + vm.config.instanceUuid
            vm_id = int(vm._GetMoId().replace('vm-', ''))
            vm_name = vm.summary.config.name
            last_updated = datetime.now().astimezone(pytz.timezone('Australia/Sydney')).strftime("%Y-%m-%d %H:%M:%S")
            proxy = [vsphere for vsphere in self.proxy_vcenters if vsphere['name'] == self.vsphere]
            if proxy:
                custidx = proxy[0]['cust_id']
                custAnno = proxy[0]['cust_anno']
            else:
                custidx = self._get_vm_customer_id(vm.customValue, customer_id, ethvmid) if self.cust_ids else ''
                custAnno = ''.join([x.value for x in vm.customValue if x.key == customer_id])

            vm_map[vm._GetMoId()] = {
                "_ethvmid": ethvmid,
                "_vmID": vm_id,
                "_custAnno": custAnno,
                "custidx": custidx,
                "ethvmid": ethvmid,
                "invVCServerID": self.vcenter_id,
                "vmID": vm_id,
                "vmPersistentID": vm.config.instanceUuid,
                "vmUuid": vm.config.uuid,
                "vmName": vm_name,
                "vmHostName": vm.guest.hostName,
                "vmIPAddress": self._get_vm_ipaddress(vm.guest.net),
                "vmCPU": vm.summary.config.numCpu,
                "vmRAM": round(vm.summary.config.memorySizeMB/1024) if vm.summary.config.memorySizeMB is not None else None,
                "vmStorageUsed": round(vm.summary.storage.committed/1073741824),
                "vmStorageTotal": round((vm.summary.storage.committed/1073741824) + (vm.summary.storage.uncommitted/1073741824)),
                "vmPowerState": vmPowerState,
                "vmHost":vm.runtime.host.name,
                "vmConfiguredOS": vm.summary.config.guestFullName,
                "vmVersion": "v" + vm.config.version.split("-",1)[1],
                "vmBootTime": vm.runtime.bootTime.strftime("%Y-%m-%d %H:%M:%S") if vm.runtime.bootTime is not None else None,
                "vmGuestToolsStatus": vm.guest.toolsStatus,
                "vmGuestToolsVersionStatus": vm.guest.toolsVersionStatus2,
                "vmGuestToolsRunningStatus": vm.guest.toolsRunningStatus,
                "vmGuestToolsVersion": vm.guest.toolsVersion,
                "vmGuestOSName": vm.summary.config.guestFullName,
                "vmGuestState": vm.guest.guestState,
                "vmResourcePool": vmResourcePool,
                "vmConfigFile": vm.summary.config.vmPathName,
                "vmApplication": "".join([x.value for x in vm.customValue if x.key == application_id]),
                "vmEnvironment": "".join([x.value for x in vm.customValue if x.key == environment_id]),
                "vmStorageTier": "".join([x.value for x in vm.customValue if x.key == storage_tier_id]),
                "vmActive": True,
                "lastUpdated": last_updated,
                "vmCPUReservation": vm.resourceConfig.cpuAllocation.reservation,
                "vmCPULimit": vm.resourceConfig.cpuAllocation.limit,
                "vmRAMReservation": vm.resourceConfig.memoryAllocation.reservation,
                "vmRAMLimit": vm.resourceConfig.memoryAllocation.limit,
                "vmDisks": self._get_vm_disks(vm.config.hardware.device, vm_id, vm_name, ethvmid, last_updated),
                "vmNetworks": self._get_vm_networks(vm.guest.net, vm_id, vm_name, ethvmid, last_updated)
            }

    def _get_vm_ipaddress(self, vmGuestNet):
        ipAddress = ""
        for net in vmGuestNet:
            if hasattr(net.ipConfig, 'ipAddress'):
                found = False
                for ip in net.ipConfig.ipAddress:
                    ip_Address = ip.ipAddress
                    if not ':' in ip_Address and not '169.254' in ip_Address:
                        ipAddress = ip_Address
                        found = True
                        break
                if found:
                    break
        return ipAddress

    def _get_vm_customer_id(self, customValue, customer_id, ethvmid):
        cust_id = [cid['custidx'] for cid in self.cust_ids if cid['ethvmid'] == ethvmid]
        if not cust_id:
            cust_id = ""
            cust_id_str = [x.value for x in customValue if x.key == customer_id]
            if cust_id_str:
               cust_id_1 = [cid['custidx'] for cid in self.cust_ids if cid['vmCustAnno'] == cust_id_str[0] and cid['ethvmid'] == ethvmid]
               if cust_id_1:
                   cust_id = int(cust_id_1[0])
        else:
            cust_id = int(cust_id[0])
        return cust_id

    def _get_vm_networks(self, networks, vm_id, vm_name, ethvmid, last_updated):
        network_array = []
        for network in networks:
            if network.deviceConfigId > 0:
                network_obj = {}
                network_obj['managedID']     = ethvmid
                network_obj['invVCServer']   = self.vcenter_id
                network_obj['vmName']        = vm_name
                network_obj['vmID']          = vm_id
                network_obj['network']       = network.network
                network_obj['macAddress']    = network.macAddress
                network_obj['connected']     = network.connected
                network_obj['deviceKey']     = network.deviceConfigId
                if hasattr(network.ipConfig, 'ipAddress'):
                    ipAddress                = ','.join([ip.ipAddress for ip in network.ipConfig.ipAddress if ip.state == 'preferred'])
                    network_obj['ipAddress'] = ''.join([ipAddress[i] for i in range(len(ipAddress)) if i < 50])
                else:
                    network_obj['ipAddress'] = ''
                network_obj['lastUpdated']   = last_updated
                network_array.append(network_obj)
        return network_array

    def _get_vm_disks(self, disks, vm_id, vm_name, ethvmid, last_updated):
        disk_array = []
        for disk in disks:
            device_type = type(disk).__name__
            if (disk.backing is None and device_type != 'vim.vm.device.VirtualDisk'):
                continue
            disk_obj = {}
            if hasattr(disk.backing, 'fileName'):
                datastore = disk.backing.datastore
                if datastore and disk.key < 3000:
                    disk_obj['_ethvmid']          = ethvmid
                    disk_obj['_vmID']             = vm_id
                    disk_obj['_deviceKey']        = disk.key
                    disk_obj['ethvmid']           = ethvmid
                    disk_obj['invVCServerID']     = self.vcenter_id
                    try:
                        disk_obj['deviceID']      = disk.backing.fileName.split("/")[1]
                    except Exception as e:
                        disk_obj['deviceID']      = disk.backing.fileName
                    disk_obj['vmName']            = vm_name
                    disk_obj['vmID']              = vm_id
                    disk_obj['vmDatastoreID']     = disk.backing.datastore._GetMoId()
                    try:
                        disk_obj['vmDiskTier']    = "".join([d['storageTier'] for d in self.datastores if d['dsidx'] == str(self.vcenter_id) + "-" + disk.backing.datastore._GetMoId()])
                    except Exception as e:
                        disk_obj['vmDiskTier']    = ""
                    disk_obj['vmDiskName']        = disk.deviceInfo.label
                    if hasattr(disk, 'capacityInKB'):
                         disk_obj['vmDiskSize']   = round(disk.capacityInKB/1048576)
                    else:
                         disk_obj['vmDiskSize']   = 0
                    try:
                        disk_obj['vmDiskDatastore']   = re.match("\[(.*?)\]",disk.backing.fileName).group(1)
                    except Exception as e:
                        disk_obj['vmDiskDatastore']   = disk.backing.fileName
                    disk_obj['vmDiskFileName']    = disk.backing.fileName
                    disk_obj['vmDiskUnit']        = disk.unitNumber
                    disk_obj['deviceKey']         = disk.key
                    disk_obj['vmDiskFormat']      = ""
                    disk_obj['lastUpdated']       = last_updated
                    disk_array.append(disk_obj)
        return disk_array
    
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

    def get_all_tags(self, name_filter):
        self.connect_rest(self.vsphere)
        category_list = self.tagging.category_list()
        category_obj_array = []
        for category_id in category_list:
            category = self.tagging.category_get(category_id)
            if name_filter and not category['name'] in name_filter:
                continue
            category_obj = {}
            category_obj['id']          = category['id']
            category_obj['name']        = category['name']
            category_obj['description'] = category['description']
            category_obj['tags']        = {}
            category_obj['vCenterID']   = self.vcenter_id
            tag_list = self.tagging.tag_list(category_id)
            tag_obj_array = []
            for tag_id in tag_list:
                tag = self.tagging.tag_get(tag_id)
                tag_objects = self.tagging.tag_association_list_attached_objects(tag_id)
                tag_obj_array.append(VcenterRawData.__transform(tag, tag_objects))
            category_obj['tags']['tag'] = tag_obj_array
            category_obj_array.append(category_obj)
        return category_obj_array

    @staticmethod
    def __transform(tag_info, tag_objects):
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
