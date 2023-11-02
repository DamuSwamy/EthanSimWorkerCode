from st2common.runners.base_action import Action
from operator import itemgetter

class TransformEventsAction(Action):
    def run(self, events, data):
        event_list = []
        for event in sorted(events, key=itemgetter('VmId'), reverse=True):
            event_array = [dict(event, EthVmId=sub['EthVmId']) for sub in data if event['VmId'] == sub['VmId']] 
            if not event_array:
                #event['ethvmid'] = None
                event_array = [event]
            event_list = event_list + event_array
        return event_list
