import json
from lib.actions import BaseAction
from lib import zerto_api
from datetime import datetime

class ZVMGetVMAction(BaseAction):
    def run(self, zvm_host, port, access_token=None):
        ret = False
        args = {}
        if access_token is None:
            access_token = self.establish_connection(zvm_host, port)

        args['access_token'] = access_token
        
        args['url'] = "https://{}:{}/v1/vms".format(zvm_host, port)
        args['method'] = "get"

        req_data = zerto_api.addArgs(**args)
        resp = zerto_api.makeRequest(**req_data)

        myresp = {}
        myresp['status_code'] = resp.status_code
        try:
            myresp['data'] = json.loads(resp.content.rstrip())
        except ValueError:
            myresp['data'] = resp.content

        result = []
        if myresp['status_code'] >= 200 and myresp['status_code'] <= 299:
            ret = True
            for vm in myresp['data']:
                '''
                if vm['LastTest'] is not None:
                    lastTestTime = datetime.strptime(vm['LastTest'], "%Y-%m-%dT%H:%M:%S.%fZ")
                    LastTest = lastTestTime.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    LastTest = vm['LastTest']
                vm_obj = {"vpgvmidx": vm['VmIdentifier'],
                          "vpgName": vm['VpgName'],
                          "vpgIdentity": vm['VpgIdentifier'],
                          "vmName": vm['VmName'],
                          "vmID": vm['VmIdentifier'].replace("vm-", ""),
                          "vmCPU": None,
                          "vmRAM": None,
                          "vmDISK": None,
                          "vmDatastore": None,
                          "vmZORG": vm['OrganizationName'].strip(),
                          "vmLastTest": LastTest,
                          "vmRPOActual": vm['ActualRPO'],
                          "vmProtectedSiteName": vm['SourceSite'],
                          "vmProtectedSiteIdentity": vm['ProtectedSite']['identifier'],
                          "vmRecoverySiteName": vm['TargetSite'],
                          "vmRecoverySiteIdentity": vm['RecoverySite']['identifier'],
                          "vmProvisionedStorageGB": round(vm['ProvisionedStorageInMB']/1024),
                          "vmUsedStorageGB": round(vm['UsedStorageInMB']/1024),
                          "vmJournalStorageGB": round(vm['JournalUsedStorageMb']/1024),
                          "vmActive": '1'}
                '''
                if "vm-" in vm['VmIdentifier']:
                    VmID = vm['VmIdentifier'].split(".vm-")[1]
                else:
                    VmID = '0'
                vm_obj = {"VmIdentifier": vm['VmIdentifier'],
                          "VmName": vm['VmName'],
                          "VmID": VmID,
                          "Volumes": len(vm['Volumes']),
                          "VpgIdentifier": vm['VpgIdentifier'],
                          "VpgName": vm['VpgName'],
                          "ProvisionedStorage": round(vm['ProvisionedStorageInMB']/1024),
                          "UsedStorage": round(vm['UsedStorageInMB']/1024),
                          "OrganizationName": vm['OrganizationName'],
                          "ActualRPO": vm['ActualRPO'],
                          "SourceSite": vm['SourceSite'],
                          "TargetSite": vm['TargetSite'],
                          "HardwareVersion": vm['HardwareVersion']}
                result.append(vm_obj)

        return (ret, result)

