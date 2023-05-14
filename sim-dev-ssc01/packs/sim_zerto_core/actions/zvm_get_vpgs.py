import json
from lib.actions import BaseAction
from lib import zerto_api
from datetime import datetime

class ZVMGetVPGAction(BaseAction):
    def run(self, zvm_host, port, access_token=None):
        ret = False
        args = {}
        if access_token is None:
            access_token = self.establish_connection(zvm_host, port)

        args['access_token'] = access_token
        
        args['url'] = "https://{}:{}/v1/vpgs".format(zvm_host, port)
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
            for vpg in myresp['data']:
                '''
                if vpg['LastTest'] is not None:
                    lastTestTime = datetime.strptime(vpg['LastTest'], "%Y-%m-%dT%H:%M:%S.%fZ")
                    LastTest = lastTestTime.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    LastTest = '9999-12-31 12:00:00'
                vpg_obj = {"vpgName": vpg['VpgName'],
                            "vpgIdentity": vpg['VpgIdentifier'],
                            "vpgStatus": vpg['Status'],
                            "vpgZORG": vpg['OrganizationName'],
                            "vpgZORGIdentity": vpg['Zorg']['identifier'],
                            "vpgRPOsla": vpg['ConfiguredRpoSeconds'],
                            "vpgRPOActual": vpg['ActualRPO'],
                            "vpgBackupEnable": vpg['BackupEnabled'],
                            "vpgProtectedSiteName": vpg['SourceSite'],
                            "vpgProtectedSiteIdentity": vpg['ProtectedSite']['identifier'],
                            "vpgRecoverySiteName": vpg['TargetSite'],
                            "vpgRecoverySiteIdentity": vpg['RecoverySite']['identifier'],
                            "vpgServiceProfileName": vpg['ServiceProfileName'],
                            "vpgServiceProfileIdentity": vpg['ServiceProfile']['identifier'],
                            "vpgUsedStorageGB": round(vpg['UsedStorageInMB']/1024),
                            "vpgVMs": vpg['VmsCount'],
                            "vpgLastTest": LastTest,
                            "lastUpdated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                '''
                vpg_obj = {"VpgIdentifier": vpg['VpgIdentifier'],
                           "ServiceProfileName": vpg['ServiceProfileName'],
                           "ServiceProfileIdentifier": vpg['ServiceProfileIdentifier'],
                           "ConfiguredRpoSeconds": vpg['ConfiguredRpoSeconds'],
                           "ConfiguredHistoryInMinutes": vpg['HistoryStatusApi']['ConfiguredHistoryInMinutes'],
                           "ActualHistoryInMinutes": vpg['HistoryStatusApi']['ActualHistoryInMinutes']}
                result.append(vpg_obj)

        return (ret, result)
