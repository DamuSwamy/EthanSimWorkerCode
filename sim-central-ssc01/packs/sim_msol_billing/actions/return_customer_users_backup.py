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
        self.response_json = {}
        self.user_list = []
        self.user_count = 0
        self.inserted = False
        result_array = []
        result_obj = {}
        self.insert_count = 0
        self.purge_count = 0
        for num, customer in enumerate(customers, start=start):
            if(num < end and num <= len(customers) - 1):
                tenant_id = customers[num]['CustomerId']
                name = customers[num]['Name']
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
            response_json = response.json()
            if response_json['continuationToken'] != "":
                self.user_list = self.user_list + self.construct_data(tenant_id, response_json)
                self.continuation_token = response_json['continuationToken']
                self.user_count = self.more_users(tenant_id)
            if response_json['continuationToken'] == "":
                self.user_list = self.user_list + self.construct_data(tenant_id, response_json)
                self.user_count = len(self.user_list)
        if not self.inserted:
            self.insert_data(self.user_list)
            print("Category: NoMore, Inserted {} records".format(len(self.user_list)))
        return result_array

    def construct_data(self, tenant_id, response):
        user_list = []
        for user in response['items']:
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
            else:
                user['softDeletionTime'] = None
            user_list.append(user)
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
        if self.continuation_token != "":
            self.user_list = self.user_list + self.construct_data(tenant_id, self.response_json)
            self.user_count = self.user_count + len(self.user_list)
            self.continuation_token = self.response_json['continuationToken']
            if len(self.user_list) >= 1000:
                self.insert_data(self.user_list)
                print("Inserted {} records".format(len(self.user_list)))
                self.user_list = []
            return self.more_users(tenant_id)
        if self.continuation_token == "":
            self.user_list = self.user_list + self.construct_data(tenant_id, self.response_json)
            self.insert_data(self.user_list)
            self.user_count = self.user_count + len(self.user_list)
            print("Inserted {} records".format(len(self.user_list)))
            self.user_list = []
        return self.user_count

    def insert_data(self, data):
        self.insert_count = self.insert_count + 1
        am = ActionManager()
        am.execute("127.0.0.1",
                   "sql.insert_bulk",
                   {"connection": self.connection, "data": data, "table": "PartnerCustomerUser_Temp"})
        if self.insert_count >= 10:
            self.purge_executions('sql.insert_bulk')

    def purge_executions(self, automation):
        self.purge_count = self.purge_count + 1
        if self.purge_count >= 10:
            self.purge_executions('core.local')
        time.sleep(3)
        FORMAT='%Y-%m-%dT%H:%M:%S.%fZ'
        now = datetime.now()
        date=now.strftime(FORMAT)
        am = ActionManager()
        am.execute("127.0.0.1",
                   "core.local",
                   {"cmd": "/opt/stackstorm/st2/bin/st2-purge-executions --config-file /etc/st2/st2.conf --timestamp='{}' --action-ref='{}'".format(date,automation)})
