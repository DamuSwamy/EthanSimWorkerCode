from lib.actions import BaseAction


class UpdateAction(BaseAction):
    def run(self, table, payload, number):
        s = self.client
        r = s.query(table=table, query={'number': number})  # pylint: disable=no-member
        response = r.update(payload)  # pylint: disable=no-member
        return response
