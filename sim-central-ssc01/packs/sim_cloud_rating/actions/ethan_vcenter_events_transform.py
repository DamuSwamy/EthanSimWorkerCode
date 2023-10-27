from st2common.runners.base_action import Action
from operator import itemgetter

class TransformEventsAction(Action):
    def run(self, events, data):
        event_list = []
        for event in sorted(events, key=itemgetter('EthVmId'), reverse=True):
            event_array = [dict(event, ethvmid=sub['EthVmId']) for sub in data if event['EthVmId'] == sub['EthVmId']] 
            if not event_array:
                #event['ethvmid'] = None
                event_array = [event]
            event_list = event_list + event_array
        return event_list
