from st2common.runners.base_action import Action
from operator import itemgetter

class InsertAndUpdateListGeneratorCustomerDataAction(Action):
    def run(self, vcenter_data, custinfo_data):
        vm_update = {}
        vm_cust_insert_list = []
        vm_cust_update_list = [sub for y in custinfo_data for sub in vcenter_data if sub['_EthVmId'] == y['ethvmid']]
        for y in sorted(vcenter_data, key=itemgetter('VmId'), reverse=True):
            exist = [sub for sub in custinfo_data if sub['ethvmid'] == y['_EthVmId']]
            if not exist:
                vm_cust_insert_list.append(y)
            vm_update[y['_EthVmId']] = {"_EthVmId": y['_EthVmId'],
                                        "Custidx": y['Custidx'] if y['Custidx'] != '99999' and y['Custidx'] else ""}

        return {"insert": vm_cust_insert_list, "update": vm_cust_update_list, "vm_update": list(vm_update.values())}
