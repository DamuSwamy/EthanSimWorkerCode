from st2common.runners.base_action import Action
import requests
import json

class MSOL(Action):
    def __init__(self, config=None, action_service=None):
        super(MSOL, self).__init__(config, action_service)

    def run(self, new_items_json, existing_items_json, customer_id):


        new_items_json = new_items_json["new_line_items_raw_json"]
        new_product_list_output=[]
        existing_items_json = existing_items_json["modify_line_items_raw_json"]
        existing_product_list_output = []


        for obj in new_items_json:
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

            if 'UnitCost' in obj:
                product_list_json['UnitPrice'] = obj['UnitCost']
                        
            if 'BuyPrice' in obj:
                product_list_json['Customer_BuyPrice'] = obj['BuyPrice']
                    
            if 'Term' in obj:
                product_list_json['EffectiveEndDate'] = obj['Term']

            new_product_list_output.append(product_list_json)



        for obj in existing_items_json:

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
        
            if 'Term' in obj:
                product_list_json['EffectiveEndDate'] = obj['Term']

            existing_product_list_output.append(product_list_json)

        return {
            "new_product_list":new_product_list_output,
            "existing_product_list":existing_product_list_output,
        }

    



