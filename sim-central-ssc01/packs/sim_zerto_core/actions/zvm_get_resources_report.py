import json
from lib.actions import BaseAction
from lib import zerto_api

class ZVMGetResourceAction(BaseAction):
    def run(self, zvm_host, port, start_date, end_date, site_version="9", start_time=None, end_time=None, access_token=None):
        self.host        = zvm_host
        self.port        = port
        self.start_date  = start_date
        self.end_date    = end_date
        if start_time is None:
            start_time = "00:00:00"
        if end_time is None:
            end_time = "23:59:59"
        self.start_time = start_time
        self.end_time   = end_time
        self.resources   = []
        self.page_number = 1
        result = []
        if access_token is None:
            access_token = self.establish_connection(zvm_host, port)
        self.access_token = access_token
        self.get_resources_v7()
        for resource in self.resources:
            res_obj = {"rvmGUID": resource['ProtectedSite']['VmInfo']['VmIdentifier'].replace(".vm",""),
                       "rvmZorg": resource['Vpg']['ZorgName'],
                       "rvmVPG": resource['Vpg']['VpgName'],
                       "rvmName": resource['ProtectedSite']['VmInfo']['VmName'],
                       "rvmID": resource['ProtectedSite']['VmInfo']['VmIdentifier'].split(".vm-")[1],
                       "rvmProtectedSiteName": resource['ProtectedSite']['SiteName'],
                       "rvmRecoverySiteName": resource['RecoverySite']['SiteName'],
                       "rvmCPU": resource['ProtectedSite']['VmInfo']['Cpu']['NumberOfvCpus'],
                       "rvmRAM": round(resource['ProtectedSite']['VmInfo']['Memory']['MemoryInMB']/1024),
                       "rvmDISK": round(resource['RecoverySite']['Storage']['VolumesProvisionedStorageInGB']),
                       "rvmRecoveryDatastore": resource['RecoverySite']['Storage']['DatastoreName'],
                       "rvmScanDate": resource['SampleTime'].replace("Z", ""),
                       "rvmVpgType": resource['Vpg']['ProtectedAndRecoveryType'],
                       "rvmServiceProfile": resource['Vpg']['ServiceProfileName']}
            result.append(res_obj)
        return result

    def get_resources_v7(self):
        args = {}
        args['access_token'] = self.access_token
        args['url'] = "https://{}:{}/v1/reports/resources?startTime={}T{}&endTime={}T{}&pageNumber={}&pageSize=500".format(self.host, self.port, self.start_date, self.start_time, self.end_date, self.end_time, self.page_number)
        #https://:9669//ZvmService/ResourcesReport/getSamples?fromTimeString=&toTimeString=&startIndex=&count=
        args['method'] = "get"

        req_data = zerto_api.addArgs(**args)
        resp = zerto_api.makeRequest(**req_data)

        myresp = {}
        myresp['status_code'] = resp.status_code
        try:
            myresp['data'] = json.loads(resp.content.rstrip())
        except ValueError:
            myresp['data'] = resp.content

        if myresp['status_code'] >= 200 and myresp['status_code'] <= 299:
            self.resources   = self.resources + myresp['data']
            print("Page number: {}".format(self.page_number))
            self.page_number = self.page_number + 1 
            if len(myresp['data']) == 500:
                return self.get_resources_v7()
