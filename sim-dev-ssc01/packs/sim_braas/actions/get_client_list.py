from st2common.runners.base_action import Action

class GetClientListAction(Action):
    def run(self, dpa_report, **kwargs):
        clientList = []
        clientData = dpa_report.splitlines()
        print(len(clientData))
        for data in clientData:
            client = data.split(",")
            clientdata = {"client":client[5],"group":client[3],"schedule":client[4]}
            if clientdata["client"] != 'Client':
                clientList.append(clientdata)
        return clientList

