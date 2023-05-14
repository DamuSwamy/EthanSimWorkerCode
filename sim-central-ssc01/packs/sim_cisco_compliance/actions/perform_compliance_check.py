from lib.actions import BaseAction
import requests
import json
import re
from collections import OrderedDict
import datetime

class GetDeviceConfigAction(BaseAction):
    def run(self, device_id, device_type, exclude_list, time_stamp, customer_id, count, **kwargs):
        print("Processing device count: " + str(count))
        currentTime = time_stamp
        complianceObj = OrderedDict()
        complianceObj["NetDBCustomerID"] = customer_id
        complianceObj["NetDBDeviceID"] = device_id
        complianceObj["Type"] = device_type
        if device_type in exclude_list:
            complianceObj["ComplianceStatus"] = "NOT APPLICABLE"
            complianceObj["Status"] = "Device type is not in supported list" 
            complianceObj["deviceComplianceCheckTime"] = currentTime
            performCheckList = self.perform_check("dummy_config", True)
            complianceObj["DeviceComplianceDetails"] = performCheckList
            return complianceObj
        query_params = "/{}/configbackup".format(device_id)
        try:
            response = self.netdb_api(query_params, **kwargs)
            config_json = response.json()
        except:
            complianceObj["ComplianceStatus"] = "FAILED"
            complianceObj["Status"] = "Failed to retrieve/parse the config compliance output"
            complianceObj["deviceComplianceCheckTime"] = currentTime
            complianceObj["DeviceComplianceDetails"] = [] 
            return complianceObj
        if str(response.status_code).strip() == "200":
            if "config" in config_json:
                complianceObj["ComplianceStatus"] = "TRUE"
                complianceObj["Status"] = "Config compliance successfully done"
                complianceObj["deviceComplianceCheckTime"] = currentTime
                performCheckList = self.perform_check(config_json["config"], False)
                complianceObj["DeviceComplianceDetails"] = performCheckList
                for check in performCheckList:
                    if "FALSE" in check.values():
                        complianceObj["ComplianceStatus"] = "FALSE"
        elif str(response.status_code).strip() == "404":
            complianceObj["ComplianceStatus"] = "FAILED"
            complianceObj["Status"] = config_json["detail"]
            complianceObj["deviceComplianceCheckTime"] = currentTime
            performCheckList = self.perform_check(config_json["detail"], True)
            complianceObj["DeviceComplianceDetails"] = performCheckList
        else:
            complianceObj["ComplianceStatus"] = "FAILED"
            complianceObj["Status"] = response.reason
            complianceObj["deviceComplianceCheckTime"] = currentTime
            performCheckList = self.perform_check("dummy_config", True)
            complianceObj["DeviceComplianceDetails"] = performCheckList
        return complianceObj


    def perform_check(self, config_str, is_not_applicable):
        ComplianceList = []
        data = self.read_config()
        for config in data:
            check_status = {}
            check_name = config["check_code"]
            regex_to_match = config["regex_to_match"]
            look_for_match_yes_no = config["look_for_match_yes_no"]
            compliance_status = "FALSE"
            regex_result = re.search(regex_to_match, config_str)
            regex_matched = re.findall(regex_to_match, config_str)
            if regex_matched:
                regex_matched_final = str(regex_matched[0])
            else:
                regex_matched_final = ""
            if is_not_applicable:
                compliance_status = "NOT APPLICABLE"
            elif regex_result and look_for_match_yes_no:
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
            check_status["DeviceCheckInformation"] = regex_matched_final
            ComplianceList.append(check_status)
        return ComplianceList
