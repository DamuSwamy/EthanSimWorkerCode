from lib.actions import BaseAction
import json

class FormatConversionAction(BaseAction):
    def run(self, input_json):
        json_obj = input_json
        final_obj = {}
        final_obj['NetDBCompanyID'] = json_obj['NetDBCompanyID']
        final_obj['compliancecheckTimestamp'] = json_obj['compliancecheckTimestamp']
        devices = json_obj['Devices']
        deviceList = []
        for device in devices:
            for check in device['DeviceComplianceDetails']:
                deviceCheckObj = {}
                deviceCheckObj['NetDBCustomerID'] = device['NetDBCustomerID']
                deviceCheckObj['NetDBDeviceID'] = device['NetDBDeviceID']
                deviceCheckObj['Type'] = device['Type']
                deviceCheckObj['ComplianceStatus'] = device['ComplianceStatus']
                deviceCheckObj['Status'] = device['Status']
                deviceCheckObj['deviceComplianceCheckTime'] = device['deviceComplianceCheckTime']
                deviceCheckObj['DeviceComplianceDetails'] = check
                deviceList.append(deviceCheckObj)
            final_obj['devices'] = deviceList
        return final_obj
