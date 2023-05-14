from st2common.runners.base_action import Action
from datetime import datetime
import requests
import json

class ReturnCustomerInvoiceLineItemAction(Action):
    def run(self, max_invoice_id, auth_token, line_item):
        self.base_uri = 'https://api.partnercenter.microsoft.com/v1/invoices'
        self.auth_token = auth_token
        line_item_list = []
        if line_item == 'Azure':
            endpoint = '{}/{}/lineitems/Azure/BillingLineItems'.format(self.base_uri, max_invoice_id)
            response = self.make_an_api_call(endpoint)
            for item in response['items']:
                lineLitem = {}
                lineLitem['DetailLineItemId']             = item['detailLineItemId']
                lineLitem['Sku']                          = item['sku']
                lineLitem['IncludedQuantity']             = item['includedQuantity']
                lineLitem['OverageQuantity']              = item['overageQuantity']
                lineLitem['ListPrice']                    = item['listPrice']
                lineLitem['Currency']                     = item['currency']
                lineLitem['PretaxCharges']                = item['pretaxCharges']
                lineLitem['TaxAmount']                    = item['taxAmount']
                lineLitem['PostTaxTotal']                 = item['postTaxTotal']
                lineLitem['PretaxEffectiveRate']          = item['pretaxEffectiveRate']
                lineLitem['PostTaxEffectiveRate']         = item['postTaxEffectiveRate']
                lineLitem['ChargeType']                   = item['chargeType']
                lineLitem['InvoiceLineItemType']          = item['invoiceLineItemType']
                lineLitem['PartnerId']                    = item['partnerId']
                lineLitem['PartnerName']                  = item['partnerName']
                lineLitem['PartnerBillableAccountId']     = item['partnerBillableAccountId']
                lineLitem['CustomerId']                   = item['customerId']
                lineLitem['DomainName']                   = item['domainName']
                lineLitem['CustomerCompanyName']          = item['customerCompanyName']
                lineLitem['MpnId']                        = item['mpnId']
                lineLitem['Tier2MpnId']                   = item['tier2MpnId']
                lineLitem['InvoiceNumber']                = item['invoiceNumber']
                lineLitem['SubscriptionId']               = item['subscriptionId'] 
                lineLitem['SubscriptionName']             = item['subscriptionName']
                lineLitem['SubscriptionDescription']      = item['subscriptionDescription']
                lineLitem['BillingCycleType']             = item['billingCycleType']
                lineLitem['OrderId']                      = item['orderId']
                lineLitem['ServiceName']                  = item['serviceName']
                lineLitem['ServiceType']                  = item['serviceType']
                lineLitem['ResourceGuid']                 = item['resourceGuid']
                lineLitem['ResourceName']                 = item['resourceName']
                lineLitem['Region']                       = item['region']
                lineLitem['ConsumedQuantity']             = item['consumedQuantity']
                lineLitem['ChargeStartDate']              = item['chargeStartDate']
                lineLitem['ChargeEndDate']                = item['chargeEndDate']
                lineLitem['Unit']                         = item['unit']
                lineLitem['BillingProvider']              = item['billingProvider']
                line_item_list.append(lineLitem)
     
        if line_item == 'Office':
            endpoint = '{}/{}/lineitems/Office/BillingLineItems'.format(self.base_uri, max_invoice_id)
            response = self.make_an_api_call(endpoint)
            for item in response['items']:
                lineItem                                          = {}
                lineItem['PartnerId']                             = item['partnerId']
                lineItem['CustomerId']                            = item['customerId']
                lineItem['CustomerName']                          = item['customerName']
                lineItem['MpnId']                                 = item['mpnId']
                lineItem['Tier2MpnId']                            = item['tier2MpnId']
                lineItem['OrderId']                               = item['orderId']
                lineItem['InvoiceNumber']                         = item['invoiceNumber']
                lineItem['SubscriptionId']                        = item['subscriptionId']
                lineItem['SyndicationPartnerSubscriptionNumber']  = item['syndicationPartnerSubscriptionNumber']
                lineItem['OfferId']                               = item['offerId']
                lineItem['DurableOfferId']                        = item['durableOfferId']
                lineItem['OfferName']                             = item['offerName']
                lineItem['DomainName']                            = item['domainName']
                lineItem['BillingCycleType']                      = item['billingCycleType']
                lineItem['SubscriptionName']                      = item['subscriptionName']
                lineItem['SubscriptionDescription']               = item['subscriptionDescription']
                lineItem['SubscriptionStartDate']                 = item['subscriptionStartDate']
                lineItem['SubscriptionEndDate']                   = item['subscriptionEndDate']
                lineItem['ChargeStartDate']                       = item['chargeStartDate']
                lineItem['ChargeEndDate']                         = item['chargeEndDate']
                lineItem['ChargeType']                            = item['chargeType']
                lineItem['UnitPrice']                             = item['unitPrice']
                lineItem['Quantity']                              = item['quantity']
                lineItem['Amount']                                = item['amount']
                lineItem['TotalOtherDiscount']                    = item['totalOtherDiscount']
                lineItem['Subtotal']                              = item['subtotal']
                lineItem['Tax']                                   = item['tax']
                lineItem['TotalForCustomer']                      = item['totalForCustomer']
                lineItem['Currency']                              = item['currency']
                lineItem['InvoiceLineItemType']                   = item['invoiceLineItemType']
                lineItem['BillingProvider']                       = item['billingProvider']
                line_item_list.append(lineItem)
        return line_item_list

    def make_an_api_call(self, endpoint):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.auth_token)
        }
        response = requests.request('get', endpoint, headers=headers, data={})
        if response.status_code == 403 or response.status_code == 401:
            print("Endpoint: "+ endpoint + ", status_code: " + str(response.status_code))
            return []
        response_json = response.json()
        return response_json
