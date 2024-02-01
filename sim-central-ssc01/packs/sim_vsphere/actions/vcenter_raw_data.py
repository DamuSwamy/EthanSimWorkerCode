from vmwarelib import inventory
from vmwarelib.actions import BaseAction
from datetime import datetime
from pyVmomi import vim
import json
import re
import pytz

class VcenterRawData(BaseAction):
    def run(self, vsphere, vcenter_id, proxy_vcenters, get_vms=True, ids=[], get_vm_disks=False, get_vm_networks=False, get_hosts=False, get_rps=False, get_folders=False, get_tags=False, datastores=[], custids=[], vm_required_field_array=[], vmdisk_required_field_array=[], tag_filter=[]):
        self.datastores = datastores
        self.vcenter_id = int(vcenter_id)
        self.cust_ids   = custids
        self.vsphere    = vsphere
        self.ids        = ids
        self.proxy_vcenters = proxy_vcenters
        vm_networks = vm_disks = vms = hosts = resouce_pools = folders = tags = []
        if get_vms or get_vm_disks or get_hosts or get_rps or get_folders:
            self.establish_connection(vsphere)
        if get_vms:
            vms           = self.get_all_vms()
            if get_vm_disks and get_vm_networks:
                for sub in vms:
                    d_found = n_found = False
                    for key, val in sub.items():
                        if key == 'VmDisks':
                            d_found = True
                            vm_disks = vm_disks + [disk for disk in val]
                        if key == 'VmNetworks':
                            n_found = True
                            vm_networks = vm_networks + [network for network in val]
                        if d_found and n_found:
                            break
                vms = [{key : val for key, val in sub.items() if key != 'vmDisks' and key != 'vmNetworks'} for sub in vms]
            if get_vm_disks and not get_vm_networks:
                for sub in vms:
                    for key, val in sub.items():
                        if key == 'VmDisks':
                            vm_disks = vm_disks + [disk for disk in val]
                            break
            if get_vm_networks and not get_vm_disks:
                for sub in vms:
                    for key, val in sub.items():
                        if key == 'VmNetworks':
                            vm_networks = vm_networks + [network for network in val]
                            break
            else:
                vms = [{key : val for key, val in sub.items() if key != 'VmDisks' and key != 'VmNetworks'} for sub in vms]

            if vm_required_field_array:
                vms = [{key : val for key, val in sub.items() if key in vm_required_field_array} for sub in vms]
            if vmdisk_required_field_array:
                vm_disks = [{key : val for key, val in sub.items() if key in vmdisk_required_field_array} for sub in vm_disks]

        if not get_vms and get_vm_disks:
            vms           = self.get_all_vms()
            for sub in vms:
                for key, val in sub.items():
                    if key == 'VmDisks':
                        vm_disks = vm_disks + [disk for disk in val]
                        break
            if vmdisk_required_field_array:
                vm_disks = [{key : val for key, val in sub.items() if key in vmdisk_required_field_array} for sub in vm_disks]

            vms = []


        if get_hosts:
            hosts         = self.get_all_hosts()
        if get_rps:
            resouce_pools = self.get_all_resource_pools()
        if get_folders:
            folders       = self.get_all_folders()
        if get_tags:
            tags          = self.get_all_tags(tag_filter)

        return  {"VirtualMachines": vms,
                 "VmDisks": vm_disks,
                 "VmNetworks": vm_networks,
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

            vm_id = int(vm._GetMoId().replace('vm-', ''))
            ethvmid = str(self.vcenter_id) +  str(vm_id) + vm.config.instanceUuid
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
                "_EthVmId": ethvmid,
                "_VmId": vm_id,
                "_CustAnno": custAnno,
                "Custidx": custidx,
                "VCServer": self.vcenter_id,
                "VmId": vm_id,
                "VmPersistentId": vm.config.instanceUuid,
                "EthVmId": ethvmid,
                "VmName": vm_name,
                "VmUuid": vm.config.uuid,
                "VmHost": vm.runtime.host.name,
                "VmVersion": "v" + vm.config.version.split("-",1)[1],
                "VmBootTime": vm.runtime.bootTime.strftime("%Y-%m-%d %H:%M:%S") if vm.runtime.bootTime is not None else None,
                "VmHostName": vm.guest.hostName,
                "VmIPAddress": self._get_vm_ipaddress(vm.guest.net),
                "VmResourcePool": vmResourcePool,
                "VmEnvironment": "".join([x.value for x in vm.customValue if x.key == environment_id]),
                "VmConfiguration": vm.summary.config.guestFullName,
                "VmActive": True,
                "VmPowerState": vmPowerState,
                "VmCpu": vm.summary.config.numCpu,
                "VmRam": round(vm.summary.config.memorySizeMB/1024) if vm.summary.config.memorySizeMB is not None else None,
                "VmStorageUsed": round(vm.summary.storage.committed/1073741824),
                "VmStorageTotal": round((vm.summary.storage.committed/1073741824) + (vm.summary.storage.uncommitted/1073741824)),
                "DecommDate": None,
                "DecommBy": None,
                "LastScanTime": last_updated,
                "VmDisks": self._get_vm_disks(vm, vm_id, vm_name, ethvmid, last_updated),
                "VmNetworks": self._get_vm_networks(vm.guest.net, vm_id, vm_name, ethvmid, last_updated)
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
                network_obj['_managedID']    = ethvmid
                network_obj['_deviceKey']    = network.deviceConfigId
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

    def _get_vm_disks(self, vm, vm_id, vm_name, ethvmid, last_updated):
        disk_array = []
        devices = vm.config.hardware.device
        disk_objs = vm.layoutEx.disk
        diskGuestingo = vm.guest.disk
        report = []
        for disk in devices:
            device_type = type(disk).__name__
            if (disk.backing is None and device_type != 'vim.vm.device.VirtualDisk'):
                continue
            """if isinstance(disk, vim.VirtualDisk):
                this_virtual_disk = disk
                layout_ex_disk = next((layout for layout in vm.layoutEx.disk if layout.key == this_virtual_disk.key), None)

                if layout_ex_disk:
                    layout_ex_disk_file_keys = [chain for chain in layout_ex_disk.chain if isinstance(chain, vim.VirtualMachineFileLayoutExDiskUnit)]

                    provisioned_size_gb = round(this_virtual_disk.capacityInKB / (1024 * 1024), 1)

                    size_on_datastore_gb = 0
                    for file_key in layout_ex_disk_file_keys:
                        file_key_value = file_key.fileKey
                        layout_files = [layout_file for layout_file in vm.layoutEx.file if layout_file.key in file_key_value and layout_file.type == "diskExtent"]
                        size_on_datastore_gb += sum(layout_file.size for layout_file in layout_files) / (1024 * 1024 * 1024)

                        disk_info = {
                            "VMName": vm.name,
                            "DiskLabel": this_virtual_disk.deviceInfo.label,
                            "DatastorePath": this_virtual_disk.backing.fileName,
                            "ProvisionedSizeGB": provisioned_size_gb,
                            "SizeOnDatastoreGB": round(size_on_datastore_gb, 1)
                        }
                        print(disk_info)
            """     
            disk_obj = {}
            if hasattr(disk.backing, 'fileName'):
                datastore = disk.backing.datastore
                real_file_name = disk.backing.fileName.replace(".vmdk", "-flat.vmdk")
                layout_ex_disk = next((layout for layout in vm.layoutEx.disk if layout.key == disk.key), None)
                if layout_ex_disk:
                    layout_ex_disk_file_keys = [chain for chain in layout_ex_disk.chain if isinstance(chain, vim.VirtualMachineFileLayoutExDiskUnit)]
                    disk_used = 0
                    for disk_file_key in layout_ex_disk_file_keys:
                        file_key_value = disk_file_key.fileKey
                        for file_key in file_key_value:
                            this_disk_file = next((layout_file for layout_file in vm.layoutEx.file if layout_file.key == file_key), None)
                            if this_disk_file:
                                if "-flat" in this_disk_file.name:
                                    disk_used = round(this_disk_file.size / (1024 * 1024 * 1024), 2)

                if datastore and disk.key < 3000:
                    disk_obj['_EthVmId']          = ethvmid
                    disk_obj['_VmId']             = vm_id
                    disk_obj['_DeviceKey']        = disk.key
                    disk_obj['VCServer']          = self.vcenter_id
                    disk_obj['VmId']              = vm_id
                    disk_obj['EthVmId']           = ethvmid
                    try:
                        disk_obj['DeviceId']      = disk.backing.fileName.rsplit('/', 1)[-1]
                    except Exception as e:
                        disk_obj['DeviceId']      = disk.backing.fileName
                    disk_obj['DeviceKey']         = disk.key
                    disk_obj['DiskName']          = disk.deviceInfo.label
                    try:
                        disk_obj['DiskTier']      = "".join([d['storageTier'] for d in self.datastores if d['dsidx'] == str(self.vcenter_id) + "-" + disk.backing.datastore._GetMoId()])
                    except Exception as e:
                        disk_obj['DiskTier']      = ""
                    disk_obj['DiskInitial']       = 0 
                    if hasattr(disk, 'capacityInKB'):
                         disk_obj['DiskSize']     = round(disk.capacityInKB/1048576)
                    else:
                         disk_obj['DiskSize']     = 0
                    disk_obj["DiskUsed"]          = disk_used
                    disk_obj['DiskDataStoreId']   = disk.backing.datastore._GetMoId()
                    try:
                        disk_obj['DiskDataStore'] = re.match("\[(.*?)\]",disk.backing.fileName).group(1)
                    except Exception as e:
                        disk_obj['DiskDataStore'] = disk.backing.fileName
                    disk_obj['DiskFileName']      = disk.backing.fileName
                    disk_obj['CreateDate']        = None
                    disk_obj['RemoveDate']        = None
                    disk_obj['LastScanTime']      = last_updated
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
