from st2common.runners.base_action import Action
from operator import itemgetter

class InsertAndUpdateListGeneratorAction(Action):
    def run(self, db_data, partner_connect_data, data_type):
        changed_item_list = partner_connect_data
        subscription_details = {}
        update_list = []
        insert_list = []
        if data_type == 'Subscriptions':
            for y in sorted(changed_item_list, key=itemgetter('CustomerId', 'id'), reverse=True):
                action_needed = False
                for z in sorted(db_data, key=itemgetter('CustomerId', 'id'), reverse=True):
                    action_needed = True
                    if y['CustomerId'] == z['CustomerId'] and y['id'] == z['id']:
                        action_needed = False
                        if y['Status'] != z['Status'] or y['Quantity'] != z['Quantity']:
                            update_list.append(y)
                        break
                if action_needed:
                    insert_list.append(y)
        elif data_type == 'Invoices':
            for y in sorted(changed_item_list, key=itemgetter('id'), reverse=True):
                action_needed = False
                for z in sorted(db_data, key=itemgetter('id'), reverse=True):
                    action_needed = True
                    if y['id'] == z['id']:
                        action_needed = False
                        update_list.append(y)
                        break
                if action_needed:
                    insert_list.append(y)
        else:
            for y in sorted(changed_item_list, key=itemgetter('CustomerId', 'SkuId'), reverse=True):
                action_needed = False
                for z in sorted(db_data, key=itemgetter('CustomerId', 'SkuId'), reverse=True):
                    action_needed = True
                    if y['CustomerId'] == z['CustomerId'] and y['SkuId'] == z['SkuId']:
                        action_needed = False
                        if y['AvailableUnits'] != z['AvailableUnits'] or y['ActiveUnits'] != z['ActiveUnits'] or y['ConsumedUnits'] != z['ConsumedUnits'] or y['SuspendedUnits'] != z['SuspendedUnits'] or y['TargetType'] != z['TargetType'] or y['TotalUnits'] != z['TotalUnits'] or y['WarningUnits'] != z['WarningUnits']:
                            update_list.append(y)
                        break
                if action_needed:
                    insert_list.append(y)
        subscription_details['update'] = update_list
        subscription_details['insert'] = insert_list
        return subscription_details





