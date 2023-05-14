from lib.actions import BaseAction

class GetAccessTokenAction(BaseAction):
    def run(self, braas):
        return self.establish_connection(braas)
