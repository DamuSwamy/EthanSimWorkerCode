from st2common.runners.base_action import Action
import requests
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import json

class MSOL(Action):
    def __init__(self, config=None, action_service=None):
        super(MSOL, self).__init__(config, action_service)

    def run(self, new_items_json, existing_items_json, customer_id):

        existing_items_json = json.loads(existing_items_json)
        #new_items_json = json.loads(new_items_json)

        new_items_json = new_items_json["new_line_items_raw_json"]
        new_product_list_output=[]
        existing_items_json = existing_items_json["modify_line_items_raw_json"]
        existing_product_list_output = []

        today = datetime.today()

        for obj in new_items_json:
            if 'UnitCost' in obj and  int(obj['UnitCost'])<=0:
                continue
            product_list_json = {
                    "CustomerID":customer_id,
                    "ProductID":"",
                    "SkuID":"",
                    "AutoRenewal":"",
                    "BillingPlan":"",
                    "TermDuration":"",
                    "UnitPrice":"",
                    "Customer_BuyPrice":"",
                    "EffectiveEndDate":""
            }

            if 'OfferID' in obj:
                product_list_json['ProductID'] = obj['OfferID'].split(':')[0]
                product_list_json['SkuID'] = obj['OfferID'].split(':')[1]

            if 'autoRenewEnabled' in obj:
                product_list_json['AutoRenewal'] = obj['autoRenewEnabled']

            if 'BillingPlan' in obj:
                product_list_json['BillingPlan'] = obj['BillingPlan']    

            if 'HidTerm' in obj:
                product_list_json['TermDuration'] = obj['HidTerm']
                termDuration = obj['HidTerm']
                if termDuration == "P1Y":
                    endDate = today + relativedelta(years=1) - timedelta(1)
                    formattedEndDate = endDate.strftime("%Y-%m-%d")
                    product_list_json['EffectiveEndDate'] = formattedEndDate
                elif termDuration == "P3Y":
                    endDate = today + relativedelta(years=3) - timedelta(1)
                    formattedEndDate = endDate.strftime("%Y-%m-%d")
                    product_list_json['EffectiveEndDate'] = formattedEndDate
                elif termDuration == "P1M":
                    endDate = today + relativedelta(months=1) - timedelta(1)
                    formattedEndDate = endDate.strftime("%Y-%m-%d")
                    product_list_json['EffectiveEndDate'] = formattedEndDate
            if 'UnitCost' in obj:
                product_list_json['UnitPrice'] = obj['UnitCost']
                        
            if 'BuyPrice' in obj:
                product_list_json['Customer_BuyPrice'] = obj['BuyPrice']
                    

            new_product_list_output.append(product_list_json)



        for obj in existing_items_json:
            if 'UnitCost' in obj and  int(obj['UnitCost'])<=0:
                continue
            product_list_json = {
                    "_ProductID":"",
                    "CustomerID":customer_id,
                    "ProductID":"",
                    "SkuID":"",
                    "AutoRenewal":"",
                    "BillingPlan":"",
                    "TermDuration":"",
                    "UnitPrice":"",
                    "Customer_BuyPrice":"",
                    "EffectiveEndDate":""
            }

            if 'OfferID' in obj:
                product_list_json['_ProductID'] = obj['OfferID'].split(':')[0]
                product_list_json['ProductID'] = obj['OfferID'].split(':')[0]
                product_list_json['SkuID'] = obj['OfferID'].split(':')[1]

            if 'autoRenewEnabled' in obj:
                product_list_json['AutoRenewal'] = obj['autoRenewEnabled']

            if 'BillingPlan' in obj:
                product_list_json['BillingPlan'] = obj['BillingPlan']    

            if 'Term' in obj:
                product_list_json['TermDuration'] = obj['Term']

            if 'UnitCost' in obj:
                product_list_json['UnitPrice'] = obj['UnitCost']
            
            if 'YourBuy' in obj:
                product_list_json['Customer_BuyPrice'] = obj['YourBuy']
        
            if 'Expiry' in obj:
                date_object = datetime.strptime(obj['Expiry'], "%d/%m/%Y")
                formatted_date = date_object.strftime("%Y-%m-%d")
                product_list_json['EffectiveEndDate'] = formatted_date

            existing_product_list_output.append(product_list_json)
        
        combined_data = existing_product_list_output
        
        if len(new_product_list_output)>0:
            for data in new_product_list_output:
                combined_data.append(data)

        return {
            "combined_data":combined_data,
            "new_product_list":new_product_list_output,
            "existing_product_list":existing_product_list_output,
        }

    



