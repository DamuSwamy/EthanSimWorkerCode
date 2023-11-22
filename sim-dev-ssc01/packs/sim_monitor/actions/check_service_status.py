from st2common.runners.base_action import Action
import paramiko

class CheckServiceStatusAction(Action):
    def run(self, remote_server, username, password, service_name):
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(remote_server, username=username, password=password)

            command = "service {} status".format(service_name)
            stdin, stdout, stderr = client.exec_command(command)
            output = stdout.read().decode().strip()

            client.close()

            if "active (running)" in output:
                return True
            else:
                return False

        except Exception as e:
            print("Error:", e)
            return False
