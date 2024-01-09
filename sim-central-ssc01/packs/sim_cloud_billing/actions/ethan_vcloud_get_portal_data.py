from st2common.runners.base_action import Action
import xml.etree.ElementTree as ET
import datetime
import json
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import pytz


class DataSync(Action):
    def __init__(self, config=None, action_service=None):
        super(DataSync, self).__init__(config, action_service)

    def run(self,username, password):
        iaas_vcloud_records = []
        orgs = []

    
        #    Start collection of IaaS vCloud records
        username = username
        password = password
        vmorg_uri = 'https://portal.iaas.ethoria.services/api/org'
        base_uri = 'https://portal.iaas.ethoria.services/api'
        endpoint = '{}/sessions'.format(base_uri)
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/*;version=31.0'
            }
        response = requests.request('post', endpoint, headers=headers, auth=HTTPBasicAuth(username, password))
        response_status = response.status_code
        response_session = response.headers['x-vmware-vcloud-access-token']
        response_body = response.text

        

        endpoint = '{}/session'.format(base_uri)
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/*;version=31.0',
            'Authorization': f'Bearer {response_session}'
            }

        response = requests.request('get', endpoint, headers=headers)
        response_status = response.status_code
        response_body = response.text


        if response_status == 200:
            
            namespace = {'ns0': 'http://www.vmware.com/vcloud/v1.5',
                        'ns1': 'http://www.vmware.com/vcloud/extension/v1.5',
                        'ns2': 'http://schemas.dmtf.org/ovf/envelope/1',
                        'ns3': 'http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_VirtualSystemSettingData',
                        'ns5': 'http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_ResourceAllocationSettingData',
                        'ns6': 'http://www.vmware.com/schema/ovf',
                        'ns7': 'http://schemas.dmtf.org/ovf/environment/1',
                        'ns8': 'http://www.vmware.com/schema/ovfenv'}
            
            headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/*;version=31.0',
            'Authorization': f'Bearer {response_session}'
            }    
            endpoint = vmorg_uri
            response = requests.request('get', endpoint, headers=headers)

            response_body = response.text
            org_body = ET.fromstring(response_body)
        #   ET.dump(org_body)
            org_raw_records = org_body.findall('.//ns0:Org', namespaces=namespace)
            for org in org_raw_records:
                org_record = {}
                org_record['href'] = org.get('href')
                org_record['name'] = org.get('name')
                orgs.append(org_record)

        def process_admin_vm_record(admin_vm_record):

            if admin_vm_record.get('status') == 'UNKNOWN' or admin_vm_record.get('status') == 'FAILED_CREATION':
                nothing = 'nothing'
            else:
                if admin_vm_record.get('isVAppTemplate') != 'true':
                    total_virtual_quantity = 0
                    vmhref = admin_vm_record.get('href')
                    vm_response = requests.request('get', vmhref, headers=headers)
                    vm_response_body = vm_response.text
                    xml_vm_body = ET.fromstring(vm_response_body)
                    vmName = xml_vm_body.find('.//ns0:ComputerName', namespaces=namespace)
                    #vmName  = xml_vm_body.find('.', namespaces=namespace).get('name')
                    if vmName is not None and vmName.text:
                
                        ethvCloudID = xml_vm_body.find('.', namespaces=namespace).get('id')
                        vCloudvAppID = 'urn:vcloud:vapp:' + xml_vm_body.find('.//ns0:Link[@rel="up"]', namespaces=namespace).get('href').split('vapp-')[-1]
                        vCloudvdc = 'urn:vcloud:vdc:' + admin_vm_record.get('vdc').split('/')[-1]
                        #vmName = xml_vm_body.find('.//ns0:ComputerName', namespaces=namespace)
                        vmName  = xml_vm_body.find('.', namespaces=namespace).get('name')
                        moref = admin_vm_record.get('moref')
                        vmRam = int(int(admin_vm_record.get('memoryMB')) / 1024)
                        for item in xml_vm_body.findall('.//ns2:Item', namespaces=namespace):
                            description = item.find('./ns5:Description', namespaces=namespace)
                            virtual_quantity = item.find('./ns5:VirtualQuantity', namespaces=namespace)
                            # Check if the 'Description' is 'Hard Disk'
                            if description is not None and description.text == 'Hard disk' and virtual_quantity is not None:
                                # Convert 'VirtualQuantity' to an integer and add it to the total
                                total_virtual_quantity += int(virtual_quantity.text)

                        powerState = xml_vm_body.find('.', namespaces=namespace).get('status')
                        systemType = xml_vm_body.find('.//ns2:System/ns3:VirtualSystemType', namespaces=namespace)
                        vm_Org = [check["name"] for check in orgs if check["href"] == admin_vm_record.get('org')]
                        date_created = xml_vm_body.find('.//ns0:DateCreated', namespaces=namespace) 
                        CPUHotAdd = xml_vm_body.find('.//ns0:CpuHotAddEnabled', namespaces=namespace)
                        MEMHotAdd = xml_vm_body.find('.//ns0:MemoryHotAddEnabled', namespaces=namespace)
                        current_datetime = datetime.now()
                        current_utc_datetime = current_datetime.utcnow()

                        # Set the desired time zone to Australian Eastern Standard Time (AEST)
                        australian_timezone = pytz.timezone('Australia/Sydney')
                        current_australian_datetime = current_utc_datetime.replace(tzinfo=pytz.utc).astimezone(australian_timezone)

                        # Format the datetime string with microseconds and manually format the timezone offset
                        formatted_datetime = current_australian_datetime.strftime("%Y-%m-%dT%H:%M:%S")

                        formatted_datetime = formatted_datetime.replace('T', ' ')
                        date_created=date_created.text.split('.')[0]
                        date_created= date_created.replace('T',' ')
                        vmRecord = {}
                    
                        vmRecord['ethvCloudID']= ethvCloudID
                        vmRecord['vCloudID']= ethvCloudID
                        vmRecord['vCloudvAppID']= vCloudvAppID
                        vmRecord['vCloudvApp']= admin_vm_record.get('containerName')
                        vmRecord['vDCS']= vCloudvdc
                        vmRecord['ethvmid']= ethvCloudID
                        vmRecord['vmID']= moref.split('vm-')[-1]
                        vmRecord['vmName']= vmName
                        vmRecord['vmCPU']= admin_vm_record.get('numberOfCpus')
                        vmRecord['vmRAM']= vmRam
                        vmRecord['vmStorageTotal']= int(total_virtual_quantity / 1073741824)
                        vmRecord['vmPowerState']= powerState
                        vmRecord['vmSystemType']= systemType.text
                        vmRecord['vmGuestToolsVersion']= admin_vm_record.get('vmToolsVersion')
                        vmRecord['vmGuestOSName']= admin_vm_record.get('guestOs')
                        vmRecord['vmOrg']= vm_Org[0]
                        vmRecord['vmCreatedDate']= date_created
                        vmRecord['vmActive']= admin_vm_record.get('isDeployed')
                        vmRecord['CPUHotadd']= CPUHotAdd.text
                        vmRecord['MemoryHotadd']= MEMHotAdd.text
                        vmRecord['lastUpdated']= formatted_datetime
                        iaas_vcloud_records.append(vmRecord)

        page = 0
        pageSize = 100

        while True:
            page += 1
                
            endpoint = '{}/query?type=adminVM&page={}&pageSize={}'.format(base_uri,page,pageSize)
            response = requests.request('get', endpoint, headers=headers)


            if response.status_code == 200:
                    
                response_body = response.text
                #print(response_body)
                xml_body = ET.fromstring(response_body)
                #   ET.dump(xml_body)
                    
                admin_vm_records = xml_body.findall('.//ns0:AdminVMRecord', namespaces=namespace)

                num_workers=20

                with ThreadPoolExecutor(max_workers=num_workers) as executor:
                    executor.map(process_admin_vm_record, admin_vm_records)

            else:
                break    


        output_vms = iaas_vcloud_records
    

        return {
            "output_vms":output_vms
        }        



        
    



