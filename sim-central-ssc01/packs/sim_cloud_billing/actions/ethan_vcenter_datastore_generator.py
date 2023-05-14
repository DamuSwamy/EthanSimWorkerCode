from st2common.runners.base_action import Action
from operator import itemgetter

class InsertAndUpdateListGeneratorDataStoreAction(Action):
    def run(self, vcenter_data, db_data):
        insert_list = []
        update_list = [sub for y in db_data for sub in vcenter_data if sub['dsidx'] == y['dsidx']]
        for y in sorted(vcenter_data, key=itemgetter('dsMoRef'), reverse=True):
            exist = [sub for sub in db_data if sub['dsidx'] == y['dsidx']]
            if not exist:
                insert_list.append(y)
        return {"insert": insert_list, "update": update_list}
