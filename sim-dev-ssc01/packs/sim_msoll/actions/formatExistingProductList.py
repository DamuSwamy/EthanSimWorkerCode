from st2common.runners.base_action import Action
import requests
import json

class MSOL(Action):
    def __init__(self, config=None, action_service=None):
        super(MSOL, self).__init__(config, action_service)

    def run(self, existing_product_list, customer_id):

        new_product_list_output = {
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


        if 'OfferID' in existing_product_list:
            new_product_list_output['ProductID'] = existing_product_list['OfferID'].split(':')[0]
            new_product_list_output['SkuID'] = existing_product_list['OfferID'].split(':')[1]

        if 'autoRenewEnabled' in existing_product_list:
            new_product_list_output['AutoRenewal'] = existing_product_list['autoRenewEnabled']

        if 'BillingPlan' in existing_product_list:
            new_product_list_output['BillingPlan'] = existing_product_list['BillingPlan']    

        if 'Term' in existing_product_list:
            new_product_list_output['TermDuration'] = existing_product_list['Term']

        if 'UnitCost' in existing_product_list:
            new_product_list_output['UnitPrice'] = existing_product_list['UnitCost']
            
        if 'YourBuy' in existing_product_list:
            new_product_list_output['Customer_BuyPrice'] = existing_product_list['YourBuy']
        
        if 'Expiry' in existing_product_list:
            new_product_list_output['EffectiveEndDate'] = existing_product_list['Expiry']

        return {
            'data':new_product_list_output
        }
    



