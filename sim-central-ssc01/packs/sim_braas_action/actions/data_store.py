from st2common.runners.base_action import Action # pylint: disable=E0401
from st2common.constants.keyvalue import SYSTEM_SCOPE # pylint: disable=E0401
from datetime import datetime, timedelta
import pytz

class IgnoreListStoreAction(Action):
    def __init__(self, config={}):
        super(IgnoreListStoreAction, self).__init__(config=config)
        self.config = config

    def run(self, key, value, expiry):
        current         = datetime.now()
        current         = current.astimezone(pytz.timezone('Australia/Sydney'))
        start_date      = current.strftime("%Y-%m-%d %H:%M:%S")
        current_time    = current.strftime("%H:%M:%S")
        current_time_hr = current.strftime("%H")
        if int(current_time_hr) >= 0 and int(current_time_hr) <= 8:
            end_date    = current.strftime("%Y-%m-%d 05:30:00")
        else:
            end_date    = current + timedelta(days=1)
            end_date    = end_date.strftime("%Y-%m-%d 05:30:00")


        t1 = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
        print('Start time:', t1)

        t2 = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
        print('End time:', t2)

        delta = t2 - t1
        print(f"Time difference is {delta.total_seconds()} seconds")
        try:
            if 'None' in value:
                original = value
                sustained = value
                value = original.remove("None")
        except Exception as e:
            value = sustained
            print(e)
        if value[0] != "COMPLETED":
            value = [*set(value)]
            value = list(filter(None, value))
        value = ','.join(f"{w}" for w in value)
        print(value)

        # default is store entore config
        expiry = int(delta.total_seconds())
        store = self.config
        print("Config content encrypted in KV store (key: %s) (expiry: %s seconds)" % (key, expiry))
        self.action_service.set_value(name=key, value=value, ttl=expiry, 
                local=False, scope=SYSTEM_SCOPE, encrypt=False)
        return (True, key)

