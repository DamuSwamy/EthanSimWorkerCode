from st2common.runners.base_action import Action
import requests
import json
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class Msol(Action):
    def __init__(self, config=None, action_service=None):
        super(Msol, self).__init__(config, action_service)

    def run(self,input_data,customerId):
        data = input_data

        data = data.replace('\n', '')

        data = data.split("||")  
        products_list=[]

        for record in data:
            product_list_json = {
                "CustomerID":customerId,
                "ProductID":"",
                "SkuID":"",
                "AutoRenewal":"",
                "BillingPlan":"",
                "TermDuration":"",
                "UnitPrice":"",
                "Customer_BuyPrice":"",
                "EffectiveEndDate":""
            }
            record = record.split(',')
            product_list_json['ProductID'] = record[2].split(':')[0]
            product_list_json['SkuID'] = record[2].split(':')[1]
            product_list_json['BillingPlan'] = record[4]
            product_list_json['TermDuration'] = record[5]
            if len(record)>=10:
                product_list_json['EffectiveEndDate'] = record[9]
            if len(record)>=7:
                product_list_json['AutoRenewal'] = record[6]
            if len(record)>=8:
                product_list_json['UnitPrice'] = record[7]
            if len(record)>=9:
                product_list_json['Customer_BuyPrice'] = record[8]

            products_list.append(product_list_json)

        return {
            'data':products_list
        }
       



