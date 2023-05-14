from st2common.runners.base_action import Action

class ConvertResultToListAction(Action):
    def run(self, customers):
        customer_list = []
        for customer in customers:
            customer_obj = {}
            customer_obj['CustomerId']            = customer['companyProfile']['tenantId']
            customer_obj['Domain']                = customer['companyProfile']['domain']
            customer_obj['Name']                  = customer['companyProfile']['companyName']
            customer_obj['RelationshipToPartner'] = customer['relationshipToPartner']
            customer_list.append(customer_obj)
        return customer_list
