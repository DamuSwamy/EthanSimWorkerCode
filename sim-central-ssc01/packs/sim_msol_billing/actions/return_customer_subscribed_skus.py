from st2common.runners.base_action import Action
import requests
import json

class ReturnCustomerSubscribedSkuAction(Action):
    def run(self, customers, auth_token, start, end):
        self.base_uri = 'https://api.partnercenter.microsoft.com/v1/customers'
        custom_subscribed_sku_list = []
        for num, customer in enumerate(customers, start=start):
            if(num < end and num <= len(customers) - 1):
                tenant_id = customers[num]['CustomerId']
            else:
                break
            endpoint = '{}/{}/subscribedskus'.format(self.base_uri, tenant_id)
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(auth_token)
            }
            response = requests.request('get', endpoint, headers=headers, data={})
            if response.status_code == 403 or response.status_code == 401:
                print("Num: " + str(num) +" Tenant ID: " + tenant_id + "; status_code: " + str(response.status_code))
                continue
            response_json = response.json()
            for subscribed in response_json['items']:
                subscribed_sku = {}
                subscribed_sku['CustomerId']       = tenant_id
                subscribed_sku['SkuId']            = subscribed['productSku']['id']
                subscribed_sku['AvailableUnits']   = subscribed['availableUnits']
                subscribed_sku['ActiveUnits']      = subscribed['activeUnits']
                subscribed_sku['CapabilityStatus'] = subscribed['capabilityStatus']
                subscribed_sku['ConsumedUnits']    = subscribed['consumedUnits']
                subscribed_sku['LicenseGroupId']   = subscribed['productSku']['licenseGroupId']
                subscribed_sku['ProductName']      = subscribed['productSku']['name']
                subscribed_sku['ServicePlans']     = None
                subscribed_sku['SkuPartNumber']    = subscribed['productSku']['skuPartNumber']
                subscribed_sku['SuspendedUnits']   = subscribed['suspendedUnits']
                subscribed_sku['TargetType']       = subscribed['productSku']['targetType']
                subscribed_sku['TotalUnits']       = subscribed['totalUnits']
                subscribed_sku['WarningUnits']     = subscribed['warningUnits']
                custom_subscribed_sku_list.append(subscribed_sku)
        return custom_subscribed_sku_list
