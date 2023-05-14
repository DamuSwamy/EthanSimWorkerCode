from st2common.runners.base_action import Action
from operator import itemgetter

class TransformDSDataAction(Action):
    def run(self, ds_data, tag_data, vcenter=None):
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
            result[datastore_id]['custid']      = dsCustTag[0] if dsCustTag else None
            result[datastore_id]['_dsidx']      = ds['dsidx']
            if vcenter is not None and vcenter == 'JCUN-TSV-VC01':
                result[datastore_id]['custid']  = 'JCUN'
        return list(result.values())
