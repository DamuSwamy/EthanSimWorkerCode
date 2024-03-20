from st2common.runners.base_action import Action
import requests
import json
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class Msol(Action):
    def __init__(self, config=None, action_service=None):
        super(Msol, self).__init__(config, action_service)

    def run(self,text):
        data = """3b20a7e3-ec4a-4585-9eac-f025622a9e53,Project Plan 3,CFQ7TTC0HDB0:0002:CFQ7TTC0PZ7G,6,Monthly,P1Y||3b20a7e3-ec4a-4585-9eac-
        f025622a9e53,Visio Plan 2,CFQ7TTC0HD32:0002:CFQ7TTC0Q5VM,4,Monthly,P1Y||3b20a7e3-ec4a-4585-9eac-f025622a9e53,Power BI Premium
        Per User,CFQ7TTC0HL8W:0001:CFQ7TTC0R11R,1,Monthly,P1Y||3b20a7e3-ec4a-4585-9eac-f025622a9e53,Power Automate per user
        plan,CFQ7TTC0LH3L:0001:CFQ7TTC0MLSR,1,Monthly,P1Y||3b20a7e3-ec4a-4585-9eac-f025622a9e53,Power BI
        Pro,CFQ7TTC0LHSF:0001:CFQ7TTC0Q7WT,60,Monthly,P1Y||3b20a7e3-ec4a-4585-9eac-f025622a9e53,Power Apps
        Premium,CFQ7TTC0LH2H:0002:CFQ7TTC0XW8D,1,Monthly,P1Y||3b20a7e3-ec4a-4585-9eac-f025622a9e53,Exchange Online (Plan
        2),CFQ7TTC0LH1P:0001:CFQ7TTC0RFD2,30,Monthly,P1Y||3b20a7e3-ec4a-4585-9eac-f025622a9e53,Microsoft 365
        F3,CFQ7TTC0LH05:0001:CFQ7TTC12KMF,10,Monthly,P1Y||3b20a7e3-ec4a-4585-9eac-f025622a9e53,Office 365
        F3,CFQ7TTC0LGZW:0001:CFQ7TTC0RJX4,2,Monthly,P1Y||3b20a7e3-ec4a-4585-9eac-f025622a9e53,Microsoft 365 Business
        Premium,CFQ7TTC0LCHC:0002:CFQ7TTC0X6RN,279,Monthly,P1Y"""

        data = data.replace('\n', '')

        data = data.split("||")  
        products_list=[]

        for record in data:
            product_list_json = {
                "CustomerID":"",
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
       



