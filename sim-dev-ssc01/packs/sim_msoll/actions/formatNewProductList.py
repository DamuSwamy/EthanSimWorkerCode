from st2common.runners.base_action import Action
import requests
import json

class MSOL(Action):
    def __init__(self, config=None, action_service=None):
        super(MSOL, self).__init__(config, action_service)

    def run(self, new_product_list, customer_id):

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


        if 'OfferID' in new_product_list:
            new_product_list_output['ProductID'] = new_product_list['OfferID'].split(':')[0]
            new_product_list_output['SkuID'] = new_product_list['OfferID'].split(':')[1]

        if 'autoRenewEnabled' in new_product_list:
            new_product_list_output['AutoRenewal'] = new_product_list['autoRenewEnabled']

        if 'BillingPlan' in new_product_list:
            new_product_list_output['BillingPlan'] = new_product_list['BillingPlan']    

        if 'HidTerm' in new_product_list:
            new_product_list_output['TermDuration'] = new_product_list['HidTerm']

        if 'UnitCost' in new_product_list:
            new_product_list_output['UnitPrice'] = new_product_list['UnitCost']
            
        if 'BuyPrice' in new_product_list:
            new_product_list_output['Customer_BuyPrice'] = new_product_list['BuyPrice']
        
        if 'Term' in new_product_list:
            new_product_list_output['EffectiveEndDate'] = new_product_list['Term']

        return {
            'data':new_product_list_output
        }
    



