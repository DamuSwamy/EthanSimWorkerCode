from st2client.client import Client
from datetime import datetime, timezone, timedelta
import pytz
from dateutil import tz
from croniter import croniter
from st2reactor.sensor.base import PollingSensor
import uuid

class RuleMonitoringSensor(PollingSensor):
    def __init__(self, sensor_service, config, poll_interval=300):
        super(RuleMonitoringSensor, self).__init__(sensor_service=sensor_service, config=config)
        self._logger = self.sensor_service.get_logger(name=self.__class__.__name__)
        self._st2client = Client(base_url='http://127.0.0.1')
        self._tz = pytz.timezone(self._config.get('timezone', 'Australia/Sydney'))
        self._last_execution_time = None
        self.trigger_name = 'rule_monitoring_sensor'
        self.trigger_pack = 'sim_cloud_billing'
        self.trigger_ref = '.'.join([self.trigger_pack, self.trigger_name])
        self._poll_interval = poll_interval

    def setup(self):
        self._logger.debug('RuleMonitoringSensor sensor has been initialized.')
        self.now = datetime.now(tz.tzlocal())
        self.rules = self._st2client.rules.get_all()

    def poll(self):
        self._logger.debug('Running GroupHandlerSensor ...')
        self.run()

    def run(self):
        try:
            for rule in self.rules:
                cron_trigger = None
                if rule.enabled and rule.trigger['type'] == 'core.st2.CronTimer':
                    self._logger.debug('RuleMonitoringSensor: action ref %s', rule.action.get('ref'))
                    self._logger.debug('RuleMonitoringSensor: action params %s', rule.action.get('parameters'))
                    cron_trigger = rule.trigger.get('parameters', {})
                    if cron_trigger and 'Ethan' in rule.ref:
                        cron_expr = '{0} {1} {2} {3} {4}'.format(
                            cron_trigger.get('minute', '0'),
                            cron_trigger.get('hour', '*'),
                            cron_trigger.get('day_of_month', '*'),
                            cron_trigger.get('month', '*'),
                            cron_trigger.get('day_of_week', '*')
                        )
                        if self._match_cron_trigger(cron_expr):
                            self._action_ref = rule.action.get('ref')
                            self._action_params = rule.action.get('parameters', {})
                            self._logger.debug('RuleMonitoringSensor: matched trigger %s', rule.name)
                            self._logger.debug('RuleMonitoringSensor: cron expression %s', cron_expr)
                            enforcements = self._st2client.executions.query(
                                rule=rule.name,
                                limit=1,
                                sort_desc='start_timestamp'
                            )
                            if len(enforcements) > 0:
                                enforcement = enforcements[0]
                                self._trigger_instance_id = enforcement.id
                                self._last_execution_time = enforcement.start_timestamp
                                self._last_execution_time = datetime.strptime(self._last_execution_time, "%Y-%m-%dT%H:%M:%S.%fZ")
                                self._last_execution_time = self._last_execution_time.strftime("%Y-%m-%dT%H:%M:%S")
                                self._last_execution_time = datetime.strptime(self._last_execution_time, "%Y-%m-%dT%H:%M:%S")
                                self._last_execution_time = self._last_execution_time.replace(tzinfo=pytz.utc).astimezone(self._tz).replace(second=0, microsecond=0).replace(tzinfo=None)
                                last_schedule_time = self.now.replace(second=0, microsecond=0).replace(tzinfo=None)
                                next_schedule_time = croniter(cron_expr, last_schedule_time).get_next(datetime)
                                if last_schedule_time <= self._last_execution_time:
                                    self._logger.debug('RuleMonitoringSensor: rule %s has last executed at %s', rule.name, self._last_execution_time.strftime('%Y-%m-%d %H:%M:%S'))
                                else:
                                    message = f'RuleMonitoringSensor: rule {rule.name} has not run at scheduled time. last executed at {self._last_execution_time.strftime("%Y-%m-%d %H:%M:%S")}, last scheduled at {last_schedule_time.strftime("%Y-%m-%d %H:%M:%S")}'
                                    self._logger.info(message)
                                    self._dispatch_trigger(rule.name, message)
                            else:
                                self._last_execution_time = None
                                message = f'RuleMonitoringSensor: unable to find the last execution details for {rule.name}'
                                self._logger.info(message)
                                self._dispatch_trigger(rule.name, message)
        except Exception as e:
            self._logger.exception('RuleMonitoringSensor: %s', str(e))
        finally:
            self._logger.debug('RuleMonitoringSensor: next will happen in %s seconds', self._poll_interval)

    def _match_cron_trigger(self, cron_expr):
        fields = cron_expr.split()
        now_fields = [str(self.now.minute), str(self.now.hour), str(self.now.day), str(self.now.month), str(self.now.isoweekday() % 7)]
        self._logger.debug('RuleMonitoringSensor: now fields %s', now_fields)
        mapping = { "minute": now_fields[0], "hour": now_fields[1], "day": now_fields[2], "month": now_fields[3], "week": now_fields[4] } 
        return True
        if fields[0] != '*' and fields[0] != mapping['minute']:
            return False
        if fields[1] != '*' and fields[1] != mapping['hour']:
            return False
        if fields[2] != '*' and fields[2] != mapping['day']:
            return False
        if fields[3] != '*' and fields[3] != mapping['month']:
            return False
        if fields[4] != '*' and fields[2] != mapping['week']:
            return False
        return True

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def _dispatch_trigger(self, rule, message):
        trigger = self.trigger_ref
        payload                  = {}
        action_payload           = {}
        action_payload['name']   = self._action_ref
        action_payload['params'] = self._action_params
        payload['rule']          = rule
        payload['message']       = message
        payload['payload']       = action_payload
        trace_tag                = uuid.uuid4().hex
        self.sensor_service.dispatch(trigger=trigger, payload=payload, trace_tag=trace_tag)
