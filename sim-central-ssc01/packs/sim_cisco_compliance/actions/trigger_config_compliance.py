from st2common.runners.base_action import Action

from st2client.client import Client
from st2client.models import LiveAction

class ActionManager(object):

    def execute(self, server, action, params):
        client = Client(base_url="https://{}/".format(server))
        client.liveactions.create(LiveAction(action=action, parameters=params))


class ActionRunner(Action):

    def run(self, automation_name, input_json):
        am = ActionManager()
        am.execute("127.0.0.1",
                   automation_name,
                   {"input_json": input_json})
