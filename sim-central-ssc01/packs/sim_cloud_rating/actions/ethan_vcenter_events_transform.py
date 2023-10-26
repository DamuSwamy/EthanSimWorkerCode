from st2common.runners.base_action import Action
from operator import itemgetter

class TransformEventsAction(Action):
    def run(self, events, data):
        event_list = []
        for event in sorted(events, key=itemgetter('vmID'), reverse=True):
            event_array = [dict(event, ethvmid=sub['ethvmid']) for sub in data if event['vmID'] == sub['vmID']] 
            if not event_array:
                #event['ethvmid'] = None
                event_array = [event]
            event_list = event_list + event_array
        return event_list
