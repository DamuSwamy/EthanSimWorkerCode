from lib.actions import BaseAction


class UploadAttachmentTwoAction(BaseAction):
    def run(self, table, file, number):
        s = self.client
        r = s.query(table=table, query={'number': number})  # pylint: disable=no-member
        response = r.attach(file)  # pylint: disable=no-member
        return response
