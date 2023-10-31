from st2common.runners.base_action import Action
from operator import itemgetter

class TransformDSDataAction(Action):
    def run(self, ds_data, tag_data, proxy_vcenters, vcenter=None):
        result = {}
        attributes      = tag_data
        for ds in sorted(ds_data, key=itemgetter('dsMoRef'), reverse=True):
            datastore_id = ds['dsMoRef']
            dsSTRoleTag = [tag['tagName'] for attr in attributes if attr['name'] == 'SROLE' for tag in attr['tags']['tag'] if 'tagDatastores' in tag.keys() and datastore_id in tag['tagDatastores']['tagDatastore']]
            dsSTierTag = [tag['tagName'] for attr in attributes if attr['name'] == 'STIER' for tag in attr['tags']['tag'] if 'tagDatastores' in tag.keys() and datastore_id in tag['tagDatastores']['tagDatastore']]
            dsCustTag = [tag['tagName'] for attr in attributes if attr['name'] == 'CUSTID' for tag in attr['tags']['tag'] if 'tagDatastores' in tag.keys() and datastore_id in tag['tagDatastores']['tagDatastore']]
                            
            result[datastore_id] = ds
            result[datastore_id]['storageRole'] = dsSTRoleTag[0] if dsSTRoleTag else None
            result[datastore_id]['storageTier'] = dsSTierTag[0] if dsSTierTag else None
            CustID = dsCustTag[0] if dsCustTag else None
            if CustID and len(CustID) > 4:
                CustID = CustID[:4]
            result[datastore_id]['custid']      = CustID
            result[datastore_id]['_dsidx']      = ds['dsidx']
            proxy = [vsphere for vsphere in proxy_vcenters if vcenter is not None and vsphere['name'] == vcenter]
            if proxy:
                custAnno = proxy[0]['cust_anno']
                result[datastore_id]['custid']  = custAnno
        return list(result.values())
