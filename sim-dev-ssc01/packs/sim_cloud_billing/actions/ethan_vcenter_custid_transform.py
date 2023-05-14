from st2common.runners.base_action import Action
from operator import itemgetter

class TransformCustomerDataAction(Action):
    def run(self, db_data, vc_data, vcenter=None):
        result = {}
        virtualMachines = vc_data['VirtualMachines']
        virtualDisks    = vc_data['VMDisks']
        attributes      = vc_data['Categories']
        dsCustTag = vmCustTag = ""
        for vm in sorted(virtualMachines, key=itemgetter('vmID'), reverse=True):
            vmID = vm['vmID']
            vm_id = 'vm-{}'.format(str(vmID))
            vmCustAnno = vm['_custAnno']
            datastore_id = [vd['vmDatastoreID'] for vd in virtualDisks if vm['_ethvmid'] == vd['_ethvmid'] and int(vd['_deviceKey']) == 2000]
            if not datastore_id:
                if len(virtualDisks) > 0:
                    datastore_id = virtualDisks[0]['vmDatastoreID']
                else:
                    datastore_id = None
            else:
                datastore_id = datastore_id[0]

            for attr in attributes:
                vmFound = False
                dsFound = False
                if attr['name'] == 'CUSTID':
                    try:
                        dsCustTag = [tag['tagName'] for tag in attr['tags']['tag'] if 'tagDatastores' in tag.keys() and datastore_id in tag['tagDatastores']['tagDatastore']]
                    except Exception as e:
                        dsCustTag = None
                    try:
                        vmCustTag = [tag['tagName'] for tag in attr['tags']['tag'] if 'tagVMs' in tag.keys() and vm_id in tag['tagVMs']['tagVM']]
                    except Exception as e:
                        vmCustTag = None
                    break
             
            result[vmID] = {"ethvmid": vm['_ethvmid'],
                            "_ethvmid": vm['_ethvmid'],
                            "vmID": vmID,
                            "vmName": vm['vmName'],
                            "vmCustTag": vmCustTag[0] if vmCustTag else "",
                            "vmCustAnno": vmCustAnno, 
                            "dsCustTag": dsCustTag[0] if dsCustTag else "",
                            "custSelectMethod": "AUTO"}
            found = True
            if vmCustTag:
                cust_list = [cust for cust in db_data if cust['custid'] == vmCustTag[0]]
                if cust_list:
                    result[vmID]['custidx']           = cust_list[0]['custidx']
                    result[vmID]['cmdbCustID']        = cust_list[0]['custid']
                    result[vmID]['cmdbCustShortName'] = cust_list[0]['custShortName']
                else:
                    found = False
            elif dsCustTag:
                cust_list = [cust for cust in db_data if cust['custid'] == dsCustTag[0]]
                if cust_list:
                    result[vmID]['custidx']           = cust_list[0]['custidx']
                    result[vmID]['cmdbCustID']        = cust_list[0]['custid']
                    result[vmID]['cmdbCustShortName'] = cust_list[0]['custShortName']
                else:
                    found = False
            elif len(vmCustAnno) > 0:
                cust_list = [cust for cust in db_data if cust['custid'] == vmCustAnno]
                if cust_list:
                    result[vmID]['custidx']           = cust_list[0]['custidx']
                    result[vmID]['cmdbCustID']        = cust_list[0]['custid']
                    result[vmID]['cmdbCustShortName'] = cust_list[0]['custShortName']
                else:
                    found = False
            else:
                result[vmID]['custidx']           = '99999'
                result[vmID]['cmdbCustID']        = 'ERR'
                result[vmID]['cmdbCustShortName'] = 'NOTFOUND'
            if not found:
                result[vmID]['custidx']           = '99999'
                result[vmID]['cmdbCustID']        = 'ERR'
                result[vmID]['cmdbCustShortName'] = 'NOTFOUND'

            if vcenter is not None and vcenter == 'JCUN-TSV-VC01':
                result[vmID]['vmCustTag']         = 'JCUN'
                result[vmID]['vmCustAnno']        = 'JCUN'
                result[vmID]['dsCustTag']         = 'JCUN'
                result[vmID]['custidx']           = 128
                result[vmID]['cmdbCustID']        = 'JCUN'
                result[vmID]['cmdbCustShortName'] = 'JCUN'

        return list(result.values())
