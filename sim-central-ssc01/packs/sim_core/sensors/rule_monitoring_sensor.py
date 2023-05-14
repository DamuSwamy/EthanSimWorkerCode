from st2client.client import Client
from datetime import datetime, timezone, timedelta
import pytz
from dateutil import tz
from croniter import croniter
from st2reactor.sensor.base import PollingSensor
import uuid
import bisect

class RuleMonitoringSensor(PollingSensor):
    def __init__(self, sensor_service, config, poll_interval=300):
        super(RuleMonitoringSensor, self).__init__(sensor_service=sensor_service, config=config, poll_interval=poll_interval)
        self._logger = self.sensor_service.get_logger(name=self.__class__.__name__)
        #self._st2client = Client(base_url='http://127.0.0.1')
        self._tz = pytz.timezone(self._config.get('timezone', 'Australia/Sydney'))
        self.trigger_name = 'rule_monitoring_sensor'
        self.trigger_pack = 'sim_core'
        self.trigger_ref = '.'.join([self.trigger_pack, self.trigger_name])
        self._poll_interval = poll_interval
        self._st2client = None

    def setup(self):
        config_api_url = self._config.get('api_url', None) or None
        config_api_key = self._config.get('api_key', None) or None

        if config_api_url is None:
            raise ValueError('"api_url" config value is required.')

        if config_api_key is None:
            raise ValueError('"api_key" config value is required.')

        self._st2client = Client(api_url=config_api_url,api_key=config_api_key)
        self._logger.info('RuleMonitoringSensor sensor has been initialized.')

    def poll(self):
        self._logger.debug('RuleMonitoringSensor: started')
        self._detect_rules()

    def _detect_rules(self):
        try:
            self.now = datetime.now(tz.tzlocal())
            rules = self._st2client.rules.get_all()
            for rule in rules:
                cron_trigger = None
                if rule.enabled and rule.trigger['type'] == 'core.st2.CronTimer':
                    cron_trigger = rule.trigger.get('parameters', {})
                    if cron_trigger and 'Ethan' in rule.ref:
                        cron_expr = '{0} {1} {2} {3} {4}'.format(
                            cron_trigger.get('minute', '0'),
                            cron_trigger.get('hour', '*'),
                            cron_trigger.get('day', '*'),
                            cron_trigger.get('month', '*'),
                            cron_trigger.get('day_of_week', '*')
                        )
                        self._logger.debug('RuleMonitoringSensor: rule %s, cron expression %s', rule.name, cron_expr)
                        if self._match_cron_trigger(cron_expr):
                            self._action_ref = rule.action.get('ref')
                            self._action_params = rule.action.get('parameters', {})
                            self._logger.debug('RuleMonitoringSensor:Rule:Matched: rule %s', rule.name)
                            self._last_execution_time = self._last_execution(rule.name)
                            if self._last_execution_time is not None:
                                last_schedule_time = self.now.replace(minute=self.closest_left(self.now.minute), second=0, microsecond=0).replace(tzinfo=None)
                                last_scheduled_time_delta = last_schedule_time + timedelta(seconds=120)

                                if last_schedule_time <= self._last_execution_time or last_scheduled_time_delta <= self._last_execution_time:
                                    self._logger.info(f'''RuleMonitoringSensor:Perfect: rule {rule.name}
                                                                                        last execution: {self._last_execution_time.strftime("%Y-%m-%d %H:%M:%S")}''')
                                else:
                                    next_schedule_time = croniter(cron_expr, last_schedule_time).get_next(datetime)
                                    time_diff_x = int((last_schedule_time - self._last_execution_time).total_seconds())
                                    #time_diff_y = int((next_schedule_time - last_schedule_time).total_seconds())
                                    if time_diff_x > 300:
                                        message = f'''<b>RuleMonitoringSensor:Missed:</b> {rule.name}<br>
                                                                                   time_diff = (last_schedule-last_execution): {time_diff_x}s<br>
                                                                                   last execution: {self._last_execution_time.strftime("%Y-%m-%d %H:%M:%S")}<br>
                                                                                   cron expresion: {cron_expr}<br>
                                                                                   expected run: {last_schedule_time.strftime("%Y-%m-%d %H:%M:%S")}<br>
                                                                                   next schedule: {next_schedule_time.strftime("%Y-%m-%d %H:%M:%S")}'''
                                        self._logger.warning(message)
                                        self._dispatch_trigger(rule.name, message)
                                    else:
                                        self._logger.info(f'''RuleMonitoringSensor:Lag: rule {rule.name}
                                                                                        Last execution: {self._last_execution_time.strftime("%Y-%m-%d %H:%M:%S")}''')
                            else:
                                message = f'RuleMonitoringSensor:FirstRun: rule {rule.name}'
                                self._logger.info(message)
                                #self._dispatch_trigger(rule.name, message)
        except Exception as e:
            self._logger.exception('RuleMonitoringSensor: %s', str(e))
            raise e
        finally:
            self._logger.debug('RuleMonitoringSensor: completed')

    def _last_execution(self, rule_name):
        latest_execution = self._st2client.executions.query(
            rule=rule_name,
            limit=1,
            sort_desc='start_timestamp'
        )
        if len(latest_execution) > 0:
            enforcement = latest_execution[0]
            self._trigger_instance_id = enforcement.id
            last_execution_time = enforcement.start_timestamp
            last_execution_time = datetime.strptime(last_execution_time, "%Y-%m-%dT%H:%M:%S.%fZ")
            last_execution_time = last_execution_time.strftime("%Y-%m-%dT%H:%M:%S")
            last_execution_time = datetime.strptime(last_execution_time, "%Y-%m-%dT%H:%M:%S")
            last_execution_time = last_execution_time.replace(tzinfo=pytz.utc).astimezone(self._tz).replace(second=0, microsecond=0).replace(tzinfo=None)
        else:
            last_execution_time = None
        return last_execution_time


    def _match_cron_trigger(self, cron_expr):
        fields = cron_expr.split()
        now_fields = [str(self.now.minute), str(self.now.hour), str(self.now.day), str(self.now.month), str(self.now.isoweekday() % 7)]
        self._logger.debug('RuleMonitoringSensor: now fields %s', now_fields)
        mapping = { "minute": now_fields[0], "hour": now_fields[1], "day": now_fields[2], "month": now_fields[3], "week": now_fields[4] }
        cron = { "minute": fields[0], "hour": fields[1], "day": fields[2], "month": fields[3], "week": fields[4] }

        if cron['minute'] != '*':
            mapping['minute'] = self.closest_left(int(mapping['minute']))
            if '/' not in cron['minute'] and '-' not in cron['minute'] and ',' not in cron['minute']:
                minute_field = [int(mapping['minute']) - i for i in range(0, 5)]
                if int(cron['minute']) not in minute_field:
                    return False
            elif int(cron['minute']) != int(mapping['minute']):
                return False
        if cron['hour'] != '*':
            if '/' in cron['hour']:
                hour_field = self._match_fields(cron['hour'])
                if int(mapping['hour']) not in hour_field:
                    return False
            elif ',' in cron['hour']:
                hour_field = cron['hour'].split(',')
                hour_field = [int(num) for num in hour_field]
                if int(mapping['hour']) not in hour_field:
                    return False
            elif '-' in cron['hour']:
                hour_field = cron['hour'].split('-')
                if int(mapping['hour']) not in range(int(hour_field[0]), int(hour_field[1])):
                    return False
            elif int(cron['hour']) != int(mapping['hour']):
                return False
        if cron['day'] != '*':
            if '/' in cron['day']:
                day_field = self._match_fields(cron['day'])
                if int(mapping['day']) not in day_field:
                    return False
            elif ',' in cron['day']:
                day_field = cron['day'].split(',')
                day_field = [int(num) for num in day_field]
                if int(mapping['day']) not in day_field:
                    return False
            elif '-' in cron['day']:
                day_field = cron['day'].split('-')
                if int(mapping['day']) not in range(int(day_field[0]), int(day_field[1])):
                    return False
            elif int(cron['day']) != int(mapping['day']):
                return False
        if cron['month'] != '*' and int(cron['month']) != int(mapping['month']):
            return False
        if cron['week'] != '*' and int(cron['week']) != int(mapping['week']):
            return False
        self._logger.info('RuleMonitoringSensor:Cron:Matched: minute %s, hour %s, day %s, month %s, week %s', cron['minute'], cron['hour'], cron['day'], cron['month'], cron['week'])
        return True

    def _match_fields(self, input_data):
        if input_data == "*/2":
            available = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22]
        elif input_data == "*/3":
            available = [0, 3, 6, 9, 12, 15, 18, 21]
        elif input_data == "*/4":
            available = [0, 4, 8, 12, 16, 20]
        elif input_data == "*/6":
            available = [0, 6, 12, 18]
        elif input_data == "*/8":
            available = [0, 8, 16]
        elif input_data == "*/12":
            available = [0, 12]
        else:
            available = input_data.replace("*/", "")
            available = int(available)
        return available

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
    
    def closest(self, K):
        if K in [58,59]:
            return 0
        lst = [0,5,10,15,20,25,30,35,40,45,50,55]
        return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-K))]

    def closest_left(self, K):
        lst = [0,5,10,15,20,25,30,35,40,45,50,55]
        return max([i for i in lst if K >= i])
