import paramiko
from st2reactor.sensor.base import PollingSensor

class StatusSensor(PollingSensor):
    def __init__(self, sensor_service, config=None, poll_interval=7200):
        super(StatusSensor, self).__init__(sensor_service=sensor_service,
                                                config=config,
                                                poll_interval=poll_interval)
        self._logger = self._sensor_service.get_logger(__name__)
        self._username = self._config.get('username')
        self._password = self._config.get('password')
        self._server = self._config.get('server')
        self._service_name = self._config.get('service_name')  
        self._trigger_name = 'sim_monitor'
        self._trigger_pack = 'sim_monitor'
        self._trigger_ref = '.'.join([self._trigger_pack, self._trigger_name])

    def setup(self):
        pass
        
    def poll(self):

        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(self._server, username=self._username, password=self._password)
            command = "service {} status".format(self._service_name)
            stdin, stdout, stderr = client.exec_command(command)
            output = stdout.read().decode().strip()

            client.close()

            if "active (running)" in output:
                self._logger.debug("{} server is working".format(self._service_name))
            else:
                self._logger.debug("{} server has stopped".format(self._service_name))
            self.emit_custom_trigger(output)
        except paramiko.AuthenticationException as auth_error:
            self._logger.error(f"Authentication error: {str(auth_error)}")
        except paramiko.SSHException as ssh_error:
            self._logger.error(f"SSH error: {str(ssh_error)}")
        except Exception as e:
            self._logger.error(f"Error while checking {self._service_name} status: {str(e)}")

    def cleanup(self):
        pass

    def emit_custom_trigger(self, output):
        payload= { 
            "message": "{} server has stopped.".format(self._service_name) ,
            "Output_log": output
            }
        self._sensor_service.dispatch(trigger=self._trigger_ref, payload=payload)

    def add_trigger(self, trigger):
        # Implement the trigger addition logic here
        pass

    def update_trigger(self, trigger):
        # Implement the trigger update logic here
        pass

    def remove_trigger(self, trigger):
        # Implement the trigger removal logic here
        pass
