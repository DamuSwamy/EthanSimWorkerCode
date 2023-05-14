from st2common.runners.base_action import Action
import datetime
import csv

class GetClientListAction(Action):
    def run(self, dpa_report, report_name, **kwargs):
        clientList = []
        failedList = []
        clientData = dpa_report.splitlines()
        print(len(clientData))
        print(report_name)
        print("Coming here1")
        if report_name == "Backup All Jobs":
            for client in csv.reader(clientData, quotechar='"', delimiter=',',quoting=csv.QUOTE_ALL):
                if client[5] != 'Client':
                    if client[0] == 'hak.braas.ethoria.services':
                        custid = client[3].split("-")[0]
                    else:
                        custid = client[1].split("/")[-1]
                    if client[19] != "":
                        try:
                            print("Coming here")
                            startTime = datetime.datetime.strptime(client[19], "%m/%d/%y %I:%M %p")
                            startTime = startTime.strftime("%Y-%m-%d %H:%M:%S")
                        except Exception as e:
                            startTime = ""
                    if client[20] != "":
                        try:
                            finishTime = datetime.datetime.strptime(client[20], "%m/%d/%y %I:%M %p")
                            finishTime = finishTime.strftime("%Y-%m-%d %H:%M:%S")
                        except Exception as e:
                            finishTime = ""
                    clientdata = {"clientName":client[5],"pluginName":client[29],"backupGroup":client[3],"schedule":client[4],"custid":custid,"domainName":client[1],"duration":client[21],"startTime":startTime,"finishTime":finishTime,"backupServer":client[0],"status":client[8],"statusCode":client[11],"statusCodeSummary":client[12],"errorCode":client[9],"errorCodeSummary":client[10]}
                    if client[11] == '30000':
                        clientList.append(clientdata)
                    else:
                        failedList.append(clientdata)
        else:
            print("Failed to match Job Name")
        return (True, (clientList, failedList))
