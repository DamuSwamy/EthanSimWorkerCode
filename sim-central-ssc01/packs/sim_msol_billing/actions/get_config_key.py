from st2common.runners.base_action import Action # pylint: disable=E0401
from st2common.constants.keyvalue import SYSTEM_SCOPE # pylint: disable=E0401

class GetConfigKeyAction(Action):
    def __init__(self, config={}):
        super(GetConfigKeyAction, self).__init__(config=config)
        self.config = config

    def run(self, key, value, expiry):
        # default is store entore config
        store = self.config
        print("Config content encrypted in KV store (key: %s) (expiry: %s seconds)" % (key, expiry))
        self.action_service.set_value(name=key, value=value, ttl=expiry, 
                local=False, scope=SYSTEM_SCOPE, encrypt=True)
        return (True, key)
