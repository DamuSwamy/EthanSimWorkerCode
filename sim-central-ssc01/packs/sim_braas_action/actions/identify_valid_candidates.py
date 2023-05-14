from st2common.runners.base_action import Action
from operator import itemgetter
from itertools import groupby

class IdentifyValidCandidatesAction(Action):
    def run(self, backup_report, failure_array):
        failure_report  = []
        current         = datetime.now()
        current         = current.astimezone(pytz.timezone('Australia/Sydney'))
        start_date      = current.strftime("%Y-%m-%d %H:%M:%S")
        current_time    = current.strftime("%H:%M:%S")
        current_time_hr = current_time.split(":")[0]
        if current_time_hr == "00":
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
        time_remaining = int(delta.total_seconds())
        time_remaining_mins = int(time_remaining/60)

        success_report = backup_report['debug_success']
        for failure_client in failure_array:
            for success in success_report:
                if failure_client['clientName'] == success['clientName']:
                    backup_duration = success['duration']
                    if 'hour' in backup_duration:
                        hours = re.match("(\d+) hour(?:(s|))",backup_duration).group(1)
                        minutes = re.match(".*?(\d+) minute(?:(s|))",backup_duration).group(1)
                        total_minutes = int(hours)*60 + int(minutes)
                    else:
                        minutes = re.match(".*?(\d+) minute(?:(s|))",backup_duration).group(1)
                        total_minutes = int(minutes)
                    if total_minutes <= time_remaining_mins:
                        failure_report.append(failure_client)
                    else:
                        print(f"Total duration would take for backup completion is {total_minutes} minutes but maintainence window ends in {time_remaining_mins} minutes")
                    break
        return failure_report
