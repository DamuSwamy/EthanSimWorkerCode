from lib.actions import BaseAction
import requests
import json
import re
from collections import OrderedDict
import datetime

class GetDeviceConfigAction(BaseAction):
    def run(self, device_id, device_type, exclude_list, time_stamp, **kwargs):
        currentTime = time_stamp
        complianceObj = OrderedDict()
        complianceObj["NetDBDeviceID"] = device_id
        complianceObj["Type"] = device_type
        if device_type in exclude_list:
            complianceObj["ComplianceStatus"] = "NOT APPLICABLE"
            complianceObj["Status"] = "Device type is not in supported list" 
            complianceObj["deviceComplianceCheckTime"] = currentTime
            complianceObj["DeviceComplianceDetails"] = []
            return complianceObj
        query_params = "/{}/configbackup".format(device_id)
        response = self.netdb_api(query_params, **kwargs)
        config_json = response.json()
        if str(response.status_code).strip() == "200":
            if "config" in config_json:
                complianceObj["ComplianceStatus"] = "TRUE"
                complianceObj["Status"] = "Config compliance successfully done"
                complianceObj["deviceComplianceCheckTime"] = currentTime
                performCheckList = self.perform_check(config_json["config"])
                complianceObj["DeviceComplianceDetails"] = performCheckList
                for check in performCheckList:
                    if "FALSE" in check.values():
                        complianceObj["ComplianceStatus"] = "FALSE"
        elif str(response.status_code).strip() == "404":
            complianceObj["ComplianceStatus"] = "FAILED"
            complianceObj["Status"] = config_json["detail"]
            complianceObj["deviceComplianceCheckTime"] = currentTime
            complianceObj["DeviceComplianceDetails"] = []
        else:
            complianceObj["ComplianceStatus"] = "FAILED"
            complianceObj["Status"] = response.reason
            complianceObj["deviceComplianceCheckTime"] = currentTime
            complianceObj["DeviceComplianceDetails"] = []
        return complianceObj


    def perform_check(self, config_str):
        ComplianceList = []
        #print(config_str)
        data = self.read_config()
        for config in data:
            check_status = {}
            check_name = config["check_name"]
            regex_to_match = config["regex_to_match"]
            look_for_match_yes_no = config["look_for_match_yes_no"]
            compliance_status = "FALSE"
            regex_result = re.search(regex_to_match, config_str)
            if regex_result and look_for_match_yes_no:
                check_status["CheckControlMatchingOutput"] = (re.findall(regex_to_match, config_str))[0]
                if "lookup_value_count" in config:
                    compliance_status = "RISK"
                    if len(re.findall(regex_to_match, config_str)) == config["lookup_value_count"]:
                        compliance_status = "TRUE"
                else:
                    compliance_status = "TRUE"
                if "lookup_value" in config:
                    if config["lookup_value"] in regex_result.group(1):
                        compliance_status = "TRUE"
                else:
                    compliance_status = "TRUE"
            elif regex_result:
                if not look_for_match_yes_no:
                    compliance_status = "TRUE"
            check_status["ControlCheck"] = check_name
            check_status["ComplianceStatus"] = compliance_status
            ComplianceList.append(check_status)
        return ComplianceList
