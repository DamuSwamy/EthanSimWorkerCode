from lib.actions import BaseAction

class GetAccessTokenAction(BaseAction):
    def run(self, host, port):
        return self.establish_connection(host, port)
