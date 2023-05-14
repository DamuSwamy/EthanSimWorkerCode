import time
from datetime import datetime
from dateutil import tz
from st2client.client import Client
from st2common.runners.base_action import Action

class RuleMonitoringAction(Action):
    def __init__(self, config=None):
        super(RuleMonitoringAction, self).__init__(config=config)
        self.client = Client(base_url='http://127.0.0.1')

    def run(self):
        # Main loop
        client = self.client
        rules = client.rules.get_all()

        for rule in rules:
            # Check if the rule is enabled
            if rule.enabled:
                if rule.trigger and rule.trigger['type'] == 'core.st2.CronTimer':
                    cron_trigger = rule.trigger.get('parameters', {})
                    if cron_trigger:
                        # Calculate the interval in seconds based on the cron trigger
                        interval = datetime.now(tz.tzlocal())
                        interval = interval.replace(hour=int(cron_trigger.get('hour', 0)), minute=int(cron_trigger.get('minute', 0)),
                                                    second=int(cron_trigger.get('second', 0)), microsecond=0)
                        interval = interval.replace(day=cron_trigger.get('day', None), month=cron_trigger.get('month', None),
                                                    year=datetime.now(tz.tzlocal()).year)
                        if cron_trigger.get('timezone'):
                            interval = interval.astimezone(tz.gettz(cron_trigger.get('timezone')))
                        else:
                            interval = interval.astimezone(tz.tzlocal())

                        # Handle day_of_week and week cron parameters
                        if cron_trigger.get('day_of_week') is not None:
                            interval = interval.replace(day=1)
                            while interval.strftime('%A').lower() != cron_trigger['day_of_week'].lower():
                                interval += timedelta(days=1)

                        if cron_trigger.get('week') is not None:
                            week_num = int(cron_trigger['week'])
                            if week_num == 0:
                                week_num = 1
                            interval = interval.replace(day=1)
                            while interval.strftime('%U') != str(week_num-1) and interval.strftime('%W') != str(week_num-1):
                                interval += timedelta(days=1)

                        time_since_last_execution = 0
                        # Check if the action has been triggered in the last interval
                        trigger_instances = client.triggerinstances.get_all(trigger=rule.trigger['ref'], limit=1, sort_desc=True)
                        if len(trigger_instances) > 0:
                            last_execution_time = datetime.fromisoformat(trigger_instances[0].triggered_timestamp[:-1])
                            time_since_last_execution = (datetime.utcnow() - last_execution_time).total_seconds()

                        if time_since_last_execution >= interval.timestamp() - datetime.utcnow().timestamp():
                            print(f"Action not triggered for rule '{rule.name}' in the last interval of {interval.timestamp() - datetime.utcnow().timestamp()} seconds.")
