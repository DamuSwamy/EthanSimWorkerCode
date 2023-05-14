from st2common.runners.base_action import Action
import requests
import json
from datetime import datetime
import time

from st2client.client import Client
from st2client.models import LiveAction

class ActionManager(object):
    def execute(self, server, action, params):
        client = Client(base_url="https://{}/".format(server))
        client.liveactions.create(LiveAction(action=action, parameters=params))

class ReturnCustomerUsersAction(Action):
    def run(self, customers, auth_token, start, end, db_connection):
        self.base_uri = 'https://api.partnercenter.microsoft.com/v1/customers'
        self.connection = db_connection
        self.auth_token = auth_token
        self.user_count = 0
        self.inserted = False
        self.user_list = []
        result_array = []
        result_obj = {}
        self.insert_count = 0
        self.purge_count = 0
        for num, customer in enumerate(customers, start=start):
            if(num < end and num <= len(customers) - 1):
                tenant_id = customers[num]['CustomerId']
                name = customers[num]['Name']
                self.user_list = []
            else:
                break
            endpoint = '{}/{}/users'.format(self.base_uri, tenant_id)
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
            self.response_json = response.json()
            if self.response_json['continuationToken'] == "":
                self.user_list = self.user_list + self.construct_data(tenant_id, self.response_json)
                print("Tenant:{}, Count:{}".format(tenant_id, len(self.user_list)))
            else:
                self.user_list = self.user_list + self.construct_data(tenant_id, self.response_json)
                print("Tenant:{}, Count:{}".format(tenant_id, len(self.user_list)))
                self.continuation_token = self.response_json['continuationToken']
                self.more_users(tenant_id)
        if not self.inserted:
            print("Category: NoMore, Inserted {} records".format(len(self.user_list)))
            self.insert_data(self.user_list)
        print("Total insertion: {}".format(self.user_count))
        return result_array

    def construct_data(self, tenant_id, response):
        user_list = []
        for user in response['items']:
            active_user = {}
            if 'usageLocation' in user:
                active_user['UsageLocation']        = user['usageLocation']
            else:
                active_user['UsageLocation']        = None
            active_user['CustomerID']           = tenant_id
            active_user['UserId']                   = user['id']
            active_user['UserPrincipalName']    = user['userPrincipalName']
            if 'firstName' in user:
                active_user['FirstName']        = user['firstName']
            else:
                active_user['FirstName']        = None
            if 'lastName' in user:
                active_user['LastName']         = user['lastName']
            else:
                 active_user['LastName']        = None
            active_user['DisplayName']          = user['displayName']
            if 'immutableId' in user:
                active_user['ImmutableId']      = user["immutableId"]
            else:
                active_user['ImmutableId']      = None
            active_user['UserDomainType']       = user['userDomainType']
            active_user['State']                = user['state']
            if 'softDeletionTime' in user:
                if '.' in user['softDeletionTime']:
                    active_user['SoftDeletionTime'] = datetime.strptime(user['softDeletionTime'].split('.')[0], '%Y-%m-%dT%H:%M:%S')
                else:
                    active_user['SoftDeletionTime'] = datetime.strptime(user['softDeletionTime'].split('Z')[0], '%Y-%m-%dT%H:%M:%S')
            else:
                active_user['SoftDeletionTime'] = None
            user_list.append(active_user)
        return user_list


    def more_users(self, tenant_id): 
        endpoint = '{}/{}/users?seekOperation=Next'.format(self.base_uri, tenant_id)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.auth_token),
            'MS-ContinuationToken': self.continuation_token
        }
        response = requests.request('get', endpoint, headers=headers, data={})
        if response.status_code == 403 or response.status_code == 401:
            print("More users - Tenant ID: " + tenant_id+ "; status_code: " + str(response.status_code))
            return {}
        self.inserted = True
        self.response_json = response.json()
        self.continuation_token = self.response_json['continuationToken']
        if self.continuation_token != "":
            self.user_list = self.user_list + self.construct_data(tenant_id, self.response_json)
            if len(self.user_list) >= 500:
                print("Tenant:{}, Count:{}".format(tenant_id, len(self.user_list)))
                self.insert_data(self.user_list)
            return self.more_users(tenant_id)
        if self.continuation_token == "":
            self.user_list = self.user_list + self.construct_data(tenant_id, self.response_json)
            print("Tenant:{}, Count:{}".format(tenant_id, len(self.user_list)))
            self.insert_data(self.user_list)

    def insert_data(self, data):
        self.insert_count = self.insert_count + 1
        am = ActionManager()
        am.execute("127.0.0.1",
                   "sql.insert_bulk",
                   {"connection": self.connection, "data": data, "table": "PartnerCustomerUser_Temp"})
        if self.insert_count >= 10:
            self.insert_count = 0
            self.purge_executions('sql.insert_bulk')
        self.user_count = self.user_count + len(data)
        self.user_list = []

    def purge_executions(self, automation):
        self.purge_count = self.purge_count + 1
        if self.purge_count > 4:
            self.purge_executions('core.local')
            self.purge_count = 0
        time.sleep(3)
        FORMAT='%Y-%m-%dT%H:%M:%S.%fZ'
        now = datetime.now()
        date=now.strftime(FORMAT)
        am = ActionManager()
        am.execute("127.0.0.1",
                   "core.local",
                   {"cmd": "/opt/stackstorm/st2/bin/st2-purge-executions --config-file /etc/st2/st2.conf --timestamp='{}' --action-ref='{}'".format(date,automation)})
