from st2common.runners.base_action import Action
from datetime import datetime

class ReturnCustomerInvoicesAction(Action):
    def run(self, invoices):
        custom_invoice_list = []
        for invoice in invoices:
            invoice_obj                     = {}
            invoice_obj['_id']              = invoice['id']
            invoice_obj['id']               = invoice['id']
            invoice_obj['DocumentType']     = invoice['documentType']
            invoice_obj['InvoiceType']      = invoice['invoiceType']
            invoice_obj['CurrencyCode']     = invoice['currencyCode']
            invoice_obj['CurrencySymbol']   = invoice['currencySymbol']
            invoice_obj['PaidAmount']       = invoice['paidAmount']
            invoice_obj['PdfDownloadLink']  = invoice['pdfDownloadLink']
            #if invoice['invoiceType'] == 'OneTime':
            #    invoice_obj['InvoiceDetails'] = None
            #else:
            #    invoice_obj['InvoiceDetails'] = 0
            if '.' in invoice['invoiceDate']:
                invoice_obj['InvoiceDate']  = datetime.strptime(invoice['invoiceDate'].split('.')[0], '%Y-%m-%dT%H:%M:%S')
            else:
                invoice_obj['InvoiceDate']  = datetime.strptime(invoice['invoiceDate'].split('Z')[0], '%Y-%m-%dT%H:%M:%S')
            invoice_obj['TotalCharges']     = invoice['totalCharges']
            custom_invoice_list.append(invoice_obj)
        return custom_invoice_list
