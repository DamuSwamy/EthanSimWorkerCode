from st2common.runners.base_action import Action
from datetime import datetime, date, timedelta
from st2client.client import Client
from st2client.models import LiveAction
import pytz

class ActionManager(object):
    def execute(self, server, action, params):
        client = Client(base_url="https://{}/".format(server))
        client.liveactions.query(state="succeeded",context.user=')


class St2ExecutionList(Action):
    def run(self, start_date=None, end_date=None, start_time'00:00:00', end_time='23:59:59'):
        current      = datetime.now()
        current_aest = current.astimezone(pytz.timezone('Australia/Sydney'))
        if start_date is None:
            star     = current_aest - timedelta(hours=24)
        if end_date is None:
            end      = current



