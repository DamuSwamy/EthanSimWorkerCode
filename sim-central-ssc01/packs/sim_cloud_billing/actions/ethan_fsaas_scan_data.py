from st2common.runners.base_action import Action
import json
from datetime import datetime
import math
import pytz

class ScanData(Action):
    def __init__(self, config=None, action_service=None):
        super(ScanData, self).__init__(config, action_service)

    def run(self, quotas, clusterName, guid):
        parsed_data = json.loads(quotas)

        guid = guid
        clusterName = clusterName
        current_datetime_utc = datetime.utcnow()
        australia_timezone = pytz.timezone('Australia/Sydney')
        current_datetime_australia = pytz.utc.localize(current_datetime_utc).astimezone(australia_timezone)

        formatted_datetime = current_datetime_australia.strftime('%Y-%m-%d %H:%M:%S')

        scanned_data = []


        for obj in parsed_data["quotas"]:
            scanned_data_obj={}
            scanned_data_obj["scanTime"] = formatted_datetime
            scanned_data_obj["clusterName"] = clusterName
            scanned_data_obj["clusterUUID"] = guid
            if 'path' in obj:
                scanned_data_obj['path'] = obj['path']
            if 'container' in obj:
                scanned_data_obj["container"] = obj["container"]
            if 'id' in obj:
                scanned_data_obj['id'] = obj['id']
            if 'include_snapshots' in obj:
                scanned_data_obj["snapshotsIncluded"] = obj['include_snapshots']
            if 'hard' in obj["thresholds"]:
                if obj['thresholds']['hard']!=None:
                    hardQuotaGB = math.floor(float(float(float(obj['thresholds']["hard"])/1024)/1024)/1024)
                    scanned_data_obj['hardQuota'] = hardQuotaGB 
                else:
                    scanned_data_obj['hardQuota'] = obj['thresholds']['hard']    
            if 'thresholds' in obj and 'soft' in obj["thresholds"]:
                if obj["thresholds"]["soft"]!=None:
                    softQuotaGB = math.floor(float(float(float(obj['thresholds']["soft"])/1024)/1024)/1024)
                    scanned_data_obj['softQuota'] = softQuotaGB
                else:
                    scanned_data_obj['softQuota'] = obj['thresholds']['soft']
            if 'thresholds' in obj and 'advisory' in obj['thresholds']:
                if obj["thresholds"]["advisory"]!=None:
                    advisoryQuotaGB = math.floor(float(float(float(obj['thresholds']["advisory"])/1024)/1024)/1024)
                    scanned_data_obj['advisoryQuota'] = advisoryQuotaGB
                else:
                    scanned_data_obj['advisoryQuota'] = obj['thresholds']['advisory']
            if 'usage' in obj and 'fslogical' in obj['usage']:
                if obj["usage"]["fslogical"]!=None:
                    usedQuotaGB = math.floor(float(float(float(obj['usage']["fslogical"])/1024)/1024)/1024)
                    scanned_data_obj['usedGB'] = usedQuotaGB
                else:
                    scanned_data_obj['usedGB'] = obj['usage']['fslogical']
            if 'usage' in obj and 'fsphysical' in obj['usage']:
                if obj["usage"]["fsphysical"]!=None:
                    allocatedQuotaGB = math.floor(float(float(float(obj['usage']["fsphysical"])/1024)/1024)/1024)
                    scanned_data_obj['allocatedGB'] = allocatedQuotaGB
                else:
                    scanned_data_obj['allocatedGB'] = obj['usage']['fsphysical']
            if 'usage' in obj and 'physical' in obj['usage']:
                if obj["usage"]["physical"]!=None:
                    physicalQuotaGB = math.floor(float(float(float(obj['usage']["physical"])/1024)/1024)/1024)
                    scanned_data_obj['physicalGB'] = physicalQuotaGB
                else:
                    scanned_data_obj['physicalGB'] = obj['usage']['physical']
            if 'usage' in obj and 'physical_protection' in obj['usage']:
                if obj["usage"]["physical_protection"]!=None:
                    physicalProtectedQuotaGB = math.floor(float(float(float(obj['usage']["physical_protection"])/1024)/1024)/1024)
                    scanned_data_obj['physicalProtectedGB'] = physicalProtectedQuotaGB
                else:
                    scanned_data_obj['physicalProtectedGB'] = obj['usage']['physical_protection']
            scanned_data_obj['processed'] = 1 

            scanned_data.append(scanned_data_obj)

        return {
            'data':scanned_data
        }

        
