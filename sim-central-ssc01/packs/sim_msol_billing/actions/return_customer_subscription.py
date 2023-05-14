from st2common.runners.base_action import Action
import requests
import json
from datetime import datetime

class ReturnCustomerSubscriptionAction(Action):
    def run(self, customers, auth_token, start, end):
        self.base_uri = 'https://api.partnercenter.microsoft.com/v1/customers'
        custom_subscription_list = []
        result_obj = {}
        result_array = []
        for num, customer in enumerate(customers, start=start):
            if(num < end and num <= len(customers) - 1):
                tenant_id = customers[num]['CustomerId']
            else:
                break
            print("Num: " + str(num) +" Tenant ID: " + tenant_id)
            endpoint = '{}/{}/subscriptions'.format(self.base_uri, tenant_id)
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(auth_token)
            }
            response = requests.request('get', endpoint, headers=headers, data={})
            if response.status_code > 299 and response.status_code < 600:
                result_obj['failed_tenant'] = tenant_id
                result_obj['reason']  = str(response.status_code)
                result_array.append(result_obj)
                print("Num: " + str(num) +" Tenant ID: " + tenant_id+ "; status_code: " + str(response.status_code))
                continue
            response_json = response.json()
            for subscrip in response_json['items']:
                subscription = {}
                subscription['CustomerId']           = tenant_id
                subscription['id']                   = subscrip['id']
                subscription['OfferId']              = subscrip['offerId']
                if 'entitlementId' in subscrip:
                    subscription['EntitlementId']    = subscrip['entitlementId']
                else:
                    subscription['EntitlementId']    = None
                subscription['OfferName']            = subscrip['offerName']
                subscription['FriendlyName']         = subscrip['friendlyName']
                subscription['Quantity']             = subscrip['quantity']
                if 'actions' in subscrip:
                    subscription['Actions']          = ",".join(subscrip['actions'])
                else:
                    subscription['Actions']          = None
                subscription['UnitType']             = subscrip['unitType']
                subscription['HasPurchasableAddons'] = subscrip['hasPurchasableAddons']
                if '.' in subscrip['creationDate']:
                    subscription['CreationDate']     = datetime.strptime(subscrip['creationDate'].split('.')[0], '%Y-%m-%dT%H:%M:%S')
                else: 
                    subscription['CreationDate']     = datetime.strptime(subscrip['creationDate'].split('Z')[0], '%Y-%m-%dT%H:%M:%S')

                if '.' in subscrip['effectiveStartDate']:
                    subscription['EffectiveStartDate'] = datetime.strptime(subscrip['effectiveStartDate'].split('.')[0], '%Y-%m-%dT%H:%M:%S')
                else:
                    subscription['EffectiveStartDate'] = datetime.strptime(subscrip['effectiveStartDate'].split('Z')[0], '%Y-%m-%dT%H:%M:%S')

                if '.' in subscrip['commitmentEndDate']:
                    subscription['CommitmentEndDate']    = datetime.strptime(subscrip['commitmentEndDate'].split('.')[0], '%Y-%m-%dT%H:%M:%S')
                else:
                    subscription['CommitmentEndDate']    = datetime.strptime(subscrip['commitmentEndDate'].split('Z')[0], '%Y-%m-%dT%H:%M:%S')
                subscription['Status']               = subscrip['status']
                subscription['AutoRenewEnabled']     = subscrip['autoRenewEnabled']
                subscription['IsTrial']              = subscrip['isTrial']
                subscription['BillingType']          = subscrip['billingType']
                subscription['BillingCycle']         = subscrip['billingCycle']
                subscription['TermDuration']         = subscrip['termDuration']
                subscription['IsMicrosoftProduct']   = subscrip['isMicrosoftProduct']
                if 'suspensionReasons' in subscrip:
                    subscription['SuspensionReasons']= ",".join(subscrip['suspensionReasons'])
                else:
                    subscription['SuspensionReasons']= None
                subscription['AttentionNeeded']      = subscrip['attentionNeeded']
                subscription['ActionTaken']          = subscrip['actionTaken']
                custom_subscription_list.append(subscription)
        return custom_subscription_list
