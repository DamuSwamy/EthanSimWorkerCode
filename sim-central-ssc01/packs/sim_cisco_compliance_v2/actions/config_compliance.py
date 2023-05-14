from lib.actions import BaseAction

class ConfigComplianceAction(BaseAction):
    def run(self, input_json):
        json_obj = input_json
        devices = json_obj['Devices']
        statusList = []
        detailsList = []
        for device in devices:
            deviceStatusObj = {}
            deviceStatusObj['NetDBCompanyID']       = device['NetDBCustomerID']
            deviceStatusObj['NetDBDeviceID']        = device['NetDBDeviceID']
            deviceStatusObj['Type']                 = device['Type']
            deviceStatusObj['Compliance_status']    = device['ComplianceStatus']
            deviceStatusObj['status']               = device['Status']
            deviceStatusObj['LastComplianceCheck']  = device['deviceComplianceCheckTime']
            statusList.append(deviceStatusObj)
            for check in device['DeviceComplianceDetails']:
                deviceDetailsObj = {}
                deviceDetailsObj['NetDBDeviceID']          = device['NetDBDeviceID']
                deviceDetailsObj['DeviceName']             = device['NetDBDeviceName']
                deviceDetailsObj['ControlCheck']           = check['ControlCheck']
                deviceDetailsObj['Compliance_status']      = check['ComplianceStatus']
                deviceDetailsObj['DeviceCheckInformation'] = check['DeviceCheckInformation']
                detailsList.append(deviceDetailsObj)
        return { 'ComplianceStatus': statusList, 'ComplianceDetails': detailsList }
