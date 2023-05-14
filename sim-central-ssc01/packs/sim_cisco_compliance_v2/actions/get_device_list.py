from lib.actions import BaseAction
import requests
import json

class GetDeviceListAction(BaseAction):
    def run(self, customer_id, limit, **kwargs):
        query_params = "/?active=true&customer={}".format(customer_id)
        response = self.netdb_api(query_params, **kwargs)
        deviceList = []
        if str(response.status_code).strip() == '200':
            devices = response.json()
            if limit is None or limit <= 0:
                limit = 0
            for num, device in enumerate(devices):
                deviceObj = {}
                if 'id' in device:
                    deviceObj['NetDBDeviceId'] = device['id']
                if 'devicename' in device:
                    deviceObj['NetDBDeviceName'] = device['devicename']
                if 'cpetype' in device:
                    deviceObj['NetDBDeviceType'] = device['cpetype']['name']
                if 'manufacturer' in device:
                    deviceObj['Manufacturer'] = device['manufacturer']['code']
                deviceList.append(deviceObj)
                if limit != 0 and num > limit:
                    break
        return deviceList
