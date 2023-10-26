from vmwarelib import inventory
#from vmwarelib.serialize import DatastoreGetJSONEncoder
from vmwarelib.actions import BaseAction
from pyVmomi import vim  # pylint: disable-msg=E0611
from datetime import datetime
import pytz


class DatastoreGet(BaseAction):
    def get_datastore_dict(self, datastore):
        #summary = json.loads(json.dumps(datastore.summary, cls=DatastoreGetJSONEncoder))
        ds_id = datastore._GetMoId()
        ds_type = type(datastore.info).__name__
        ds_type = ds_type.replace('vim.host.', '')
        if ds_type == 'NasDatastoreInfo':
            dsType = 'NAS'
            dsUUID = "{}:{}".format(datastore.info.nas.remoteHost, datastore.info.nas.remotePath)
        elif ds_type == 'VmfsDatastoreInfo':
            dsType = 'LUN'
            dsUUID = datastore.info.vmfs.uuid
        else:
            dsType = None
            dsUUID = None

        return_dict = {
            'dsMoRef': ds_id,
            'dsidx': "{}-{}".format(str(self.vcenter_id), ds_id),
            'dsVCid': self.vcenter_id,
            'dsName': datastore.name,
            'dsType': dsType,
            'dsUUID': dsUUID,
            'dsActive': True,
            'dsTotalSize': round(datastore.summary.capacity/1073741824),
            'dsUsed': round((datastore.summary.capacity/1073741824) - (datastore.summary.freeSpace/1073741824)),
            'lastUpdated': datetime.now().astimezone(pytz.timezone('Australia/Sydney')).strftime("%Y-%m-%d %H:%M:%S")
        }

        return return_dict

    def get_all(self):
        datastores = inventory.get_managed_entities(self.si_content, vim.Datastore)
        return [self.get_datastore_dict(d) for d in datastores.view]

    def get_by_id_or_name(self, datastore_ids=[], datastore_names=[]):
        results = {}

        for did in datastore_ids:
            datastore = inventory.get_datastore(self.si_content, moid=did)
            if datastore and datastore.name not in results:
                results[datastore.name] = self.get_datastore_dict(datastore)

        for datastore in datastore_names:
            datastore = inventory.get_datastore(self.si_content, name=datastore)
            if datastore and datastore.name not in results:
                results[datastore.name] = self.get_datastore_dict(datastore)

        return list(results.values())

    def run(self, vcenter_id, datastore_ids, datastore_names, vsphere=None):
        """
        Retrieve summary information for given datastores (ESXi)

        Args:
        - datastore_ids: Moid of datastore to retrieve
        - datastore_names: Name of datastore to retrieve
        - vsphere: Pre-configured vsphere connection details (config.yaml)

        Returns:
        - array: Datastore objects
        """
        return_results = []
        self.vcenter_id = vcenter_id

        self.establish_connection(vsphere)

        if not datastore_ids and not datastore_names:
            return_results = self.get_all()
        else:
            return_results = self.get_by_id_or_name(datastore_ids, datastore_names)

        return return_results
