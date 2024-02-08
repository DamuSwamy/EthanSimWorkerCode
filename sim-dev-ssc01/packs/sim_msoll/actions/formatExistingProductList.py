from st2common.runners.base_action import Action
import requests
import json

class MSOL(Action):
    def __init__(self, config=None, action_service=None):
        super(MSOL, self).__init__(config, action_service)

    def run(self, existing_product_list, customer_id):
        existing_product_list =  {
	"_RowID": "4f482645-0fc3-47bf-a4cc-c30dfa33fe96",
	"OfferID": "CFQ7TTC0LFLZ:0002:CFQ7TTC0MH5N",					#PruductID:SkuID:ignore the rest
	"QTY": 1,
	"Name": "Microsoft 365 E5",
	"BillingPlan": "monthly",										#BillingPlan
	"autoRenewEnabled": "True",										#AutoRenewal
	"SubscriptionID": "a317b02b-28d1-46cb-cd3f-e86ea2f5e978",
	"Term": "P1Y",													#TermDuration
	"OrderID": "e3d42e008faa",
	"Expiry": "13/08/2024",											#EffectiveEndDate (no computation needed!!)
	"DisplayTerm": "1 Year",										
	"RRP": "85.3",
	"ExistingExtendedRRP": "85.30",
	"UnitCost": "5.42",												#UnitPrice
	"YourBuy": "5.59",												#Customer_BuyPrice
	"ExtendedYourBuy": "5.59",
	"ProductType": "Base",
	"NewQty": "20",
	"ExtendedRRP": "1706.00",
	"NewExtendedBuy": "111.80"
    }

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
    



