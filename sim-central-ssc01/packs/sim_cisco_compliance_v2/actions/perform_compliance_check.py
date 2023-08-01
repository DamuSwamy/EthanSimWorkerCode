from lib.actions import BaseAction
import requests
import json
import re
import time
from collections import OrderedDict
from datetime import datetime

class GetDeviceConfigAction(BaseAction):
    def run(self, customer_id, devices, start, end, exclude_list, **kwargs):
        self.cust_id = customer_id
        self.exclude_list = exclude_list
        deviceList = []
        for num, device in enumerate(devices, start=start):
            if(num < end and num <= len(devices) - 1):
                device_id = devices[num]['NetDBDeviceId']
                device_type = devices[num]['NetDBDeviceType']
                device_name = devices[num]['NetDBDeviceName']
                device_manufacturer = devices[num]['Manufacturer']
                time_stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                deviceList.append(self._each_device(device_id, device_type, device_name, device_manufacturer, time_stamp))
            else:
                break
        return deviceList

    def _each_device(self, device_id, device_type, device_name, manufacturer, time_stamp, **kwargs):
        currentTime = time_stamp
        complianceObj = OrderedDict()
        complianceObj["NetDBCustomerID"] = self.cust_id
        complianceObj["NetDBDeviceID"] = device_id
        complianceObj["NetDBDeviceName"] = device_name
        complianceObj["Type"] = device_type
        if device_type in self.exclude_list or manufacturer != "cisco":
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
            #print(config_json)
        except Exception as e:
            print(e)
            complianceObj["ComplianceStatus"] = "FAILED"
            complianceObj["Status"] = "Failed to retrieve the config compliance output"
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
        data = self.read_config(self.cust_id)
        for config in data:
            check_status = {}
            check_name = config["check_code"]
            regex_to_match = config["regex_to_match"]
            look_for_match_yes_no = config["look_for_match_yes_no"]
            compliance_status = ""
            if 'not_exist_success' in config:
                not_exists_success = config["not_exist_success"]
            else:
                not_exists_success = None
            if 'not_exist_not_applicable' in config:
                not_exist_not_applicable = config["not_exist_not_applicable"]
            else:
                not_exist_not_applicable = None
            if 'negate_check' in config:
                negate_check = config["negate_check"]
            else:
                negate_check = None
            if 'depends_on' in config:
                ignore_check = [item for item in ComplianceList if item.get('ControlCheck')==config["depends_on"] and item.get('ComplianceStatus')=='NOT APPLICABLE']
                if ignore_check:
                    compliance_status = "NOT APPLICABLE"
            related_to = []
            if 'related_to' in config:
                related_to = [item for item in ComplianceList if item.get('ControlCheck')==config["related_to"]]
                compliance_status = related_to[0]["ComplianceStatus"]
            if compliance_status != "NOT APPLICABLE" and len(related_to) == 0:
                compliance_status = "FALSE"
                regex_result = re.search(regex_to_match, config_str, re.MULTILINE)
                regex_matched = re.findall(regex_to_match, config_str, re.MULTILINE)
                if regex_matched:
                    regex_matched_final = str(regex_matched[0])
                else:
                    regex_matched_final = ""
                if is_not_applicable:
                    compliance_status = "NOT APPLICABLE"
                elif regex_result and look_for_match_yes_no:
                    if "lookup_value_count" in config:
                        #compliance_status = "RISK"
                        if len(re.findall(regex_to_match, config_str)) == int(config["lookup_value_count"]):
                            compliance_status = "TRUE"
                    elif "lookup_value" in config:
                        compliance_status = "FALSE"
                        if isinstance(config["lookup_value"], str) and config["lookup_value"] in regex_result.group(1):
                            compliance_status = "TRUE"
                        elif isinstance(config["lookup_value"], int):
                            #print("check %s matched %s lookup %s",check_name, regex_result.group(1), config["lookup_value"])
                            if config["lookup_value_condition"] == "less_than":
                                if int(regex_result.group(1)) < int(config["lookup_value"]):
                                    compliance_status = "TRUE"
                            elif config["lookup_value_condition"] == "greater_than":
                                if int(regex_result.group(1)) > int(config["lookup_value"]):
                                    compliance_status = "TRUE"
                            elif config["lookup_value_condition"] == "equal_to":
                                if int(config["lookup_value"]) == int(regex_result.group(1)):
                                    compliance_status = "TRUE"
                            elif config["lookup_value_condition"] == "less_than_or_equal":
                                if int(regex_result.group(1)) <= int(config["lookup_value"]):
                                    compliance_status = "TRUE"
                            elif config["lookup_value_condition"] == "greater_than_or_equal":
                                if int(regex_result.group(1)) >= int(config["lookup_value"]):
                                    compliance_status = "TRUE"
                        else:
                            compliance_status = compliance_status
                    elif 'negate_check' in config and config['negate_check']:
                        compliance_status = "FALSE"
                    else:
                        compliance_status = "TRUE"
                elif regex_result and not look_for_match_yes_no:
                    compliance_status = "TRUE"
                elif not regex_result and not_exist_not_applicable:
                    compliance_status = "NOT APPLICABLE"
                elif not regex_result and not_exists_success:
                    compliance_status = "TRUE"
                elif not regex_result and negate_check:
                    compliance_status = "TRUE"
            check_status["ControlCheck"] = check_name
            check_status["ComplianceStatus"] = compliance_status
            check_status["DeviceCheckInformation"] = regex_matched_final
            ComplianceList.append(check_status)
        return ComplianceList

