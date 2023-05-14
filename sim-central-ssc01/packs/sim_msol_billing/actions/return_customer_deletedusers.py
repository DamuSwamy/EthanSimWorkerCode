from st2common.runners.base_action import Action
import requests
import json
from datetime import datetime

class ReturnCustomerDeletedUsersAction(Action):
    def run(self, customers, auth_token, start, end):
        self.base_uri = 'https://api.partnercenter.microsoft.com/v1/customers'
        custom_del_user_list = []
        for num, customer in enumerate(customers, start=start):
            if(num < end and num <= len(customers) - 1):
                tenant_id = customers[num]['CustomerId']
                name = customers[num]['Name']
            else:
                break
            endpoint = '{}/{}/users?filter=%7B%22Field%22%3A%22UserState%22%2C%22Value%22%3A%22Inactive%22%2C%22Operator%22%3A%22equals%22%7D'.format(self.base_uri, tenant_id)
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(auth_token)
            }
            response = requests.request('get', endpoint, headers=headers, data={})
            if response.status_code == 403 or response.status_code == 401:
                print("Tenant: "+ tenant_id + ", status_code: " + str(response.status_code))
                continue
            response_json = response.json()
            #print("Processing: {} - Retrieved: {}".format(name, response_json['totalCount']))
            for user in response_json['items']:
                user.pop('usageLocation', 'AU')
                user.pop('links','')
                user.pop('attributes','')
                user['CustomerId']           = tenant_id
                if not 'firstName' in user:
                    user['firstName']        = None
                if not 'lastName' in user:
                     user['lastName']        = None
                if not 'immutableId' in user:
                    user['immutableId']      = None
                if not 'softDeletionTime' in user:
                    user['softDeletionTime'] = None
                elif user['softDeletionTime'] is not None:
                    if '.' in user['softDeletionTime']:
                        user['softDeletionTime'] = datetime.strptime(user['softDeletionTime'].split('.')[0], '%Y-%m-%dT%H:%M:%S')
                    else:
                        user['softDeletionTime'] = datetime.strptime(user['softDeletionTime'].split('Z')[0], '%Y-%m-%dT%H:%M:%S')
                custom_del_user_list.append(user)
        return custom_del_user_list
