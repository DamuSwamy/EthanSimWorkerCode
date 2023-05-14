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

class ReturnCustomerUserLicensesAction(Action):
    def run(self, users, auth_token, db_connection):
        self.base_uri = 'https://api.partnercenter.microsoft.com/v1/customers'
        self.connection = db_connection
        result_array = []
        self.license_list = []
        self.serviceplan_list = []
        self.insert_count = 0
        self.purge_count = 0
        self.license_inserted = False
        self.sp_inserted = False
        for user in users:
            self.license_inserted = False
            self.sp_inserted = False
            tenant_id = user['CustomerID']
            user_id = user['UserId']
            if tenant_id is None or user_id is None:
                continue
            endpoint = '{}/{}/users/{}/licenses'.format(self.base_uri, tenant_id, user_id)
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(auth_token)
            }
            response = requests.request('get', endpoint, headers=headers, data={})
            if response.status_code > 299 and response.status_code < 600:
                result_obj = {}
                result_obj['tenant_id']  = tenant_id
                result_obj['user_id']    = user_id
                result_obj['reason']     = str(response.status_code)
                result_array.append(result_obj)
                #print("Tenant: {}, user: {}, status_code: {}".format(tenant_id, user_id, str(response.status_code)))
                continue
            response_json = response.json()
            if response_json['totalCount'] > 0:
                for license in response_json['items']:
                    license_obj = {}
                    license_obj['CustomerID']                = tenant_id
                    license_obj['UserId']                    = user_id
                    license_obj['LicensedProductSku']        = license['productSku']['id']
                    license_obj['skuPartNumber']             = license['productSku']['skuPartNumber']
                    license_obj['LicenseGroupId']            = license['productSku']['licenseGroupId']
                    license_obj['Name']                      = license['productSku']['name']
                    for service_plan in license['servicePlans']:
                        service_plan_obj = {}
                        service_plan_obj['CustomerID']       = tenant_id
                        service_plan_obj['UserId']           = user_id
                        service_plan_obj['displayName']      = service_plan['displayName']
                        service_plan_obj['serviceName']      = service_plan['serviceName']
                        service_plan_obj['id']               = service_plan['id']
                        service_plan_obj['ProductID']        = license['productSku']['id']
                        service_plan_obj['targetType']       = service_plan['targetType']
                        service_plan_obj['capabilityStatus'] = service_plan['capabilityStatus']
                        self.serviceplan_list.append(service_plan_obj)
                    self.license_list.append(license_obj)
                    if len(self.serviceplan_list) >= 1000:
                        self.sp_inserted = True
                        print("Inserted Service_Plans: {}".format(len(self.serviceplan_list)))
                        self.insert_data(self.serviceplan_list, 'PartnerCustomerUserLicense_ServicePlans')
                    if len(self.license_list) >= 500:
                        self.license_inserted = True
                        print("Inserted License: {}".format(len(self.license_list)))
                        self.insert_data(self.license_list, 'PartnerCustomerUserLicense_Temp')
        if not self.license_inserted and len(self.serviceplan_list) > 0:
            print("Inserted License: {}".format(len(self.license_list)))
            self.insert_data(self.license_list, 'PartnerCustomerUserLicense_Temp')
        if not self.sp_inserted and len(self.serviceplan_list) > 0:
            print("Inserted Service_Plans: {}".format(len(self.serviceplan_list)))
            self.insert_data(self.serviceplan_list, 'PartnerCustomerUserLicense_ServicePlans')
        return { "failures": result_array } 


    def insert_data(self, data, table_name):
        if len(data) > 0:
            self.insert_count = self.insert_count + 1
            am = ActionManager()
            am.execute("127.0.0.1",
                       "sql.insert_bulk",
                       {"connection": self.connection, "data": data, "table": table_name})
            if self.insert_count >= 9:
                self.insert_count = 0
                self.purge_executions('sql.insert_bulk')
        if table_name == 'PartnerCustomerUserLicense_ServicePlans':
            self.serviceplan_list = []
        if table_name == 'PartnerCustomerUserLicense_Temp':
            self.license_list = []

    def purge_executions(self, automation):
        self.purge_count = self.purge_count + 1
        if self.purge_count > 3:
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
