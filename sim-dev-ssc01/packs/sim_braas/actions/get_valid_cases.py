from st2common.runners.base_action import Action
import re

class GetValidCasesAction(Action):
    def run(self, client_list, case_list):
        validList = []
        #pattern = re.compile("Backup.+?- (.+)?(?: - \d+ Failure)")
        pattern = "backupGroup: (.+)[\s\S]+?clientName: (.+)[\s\S]+?pluginName: (.+)[\s\S]+?schedule: (.+)$"
        #pattern = re.compile("backupGroup: (.+?)\\n backupServer[\s\S]+?clientName: (.+?)\\n custid[\s\S]+?schedule: (.+?)\\n.+$")
        for case in case_list:
            result = re.findall(pattern, case['description'], re.M)
            if len(result) > 0 and len(result[0]) == 4:
                for x in client_list:
                    if (x['backupGroup'] == result[0][0] and x['clientName'] == result[0][1] and x['pluginName'] == result[0][2] and  x['schedule'] == result[0][3] and case['number'] not in validList):
                        #print(case['number']+" - "+x['group'] +"==" + result[0][0] + ";" + x['client'] +"=="+ result[0][1]+";"+x['schedule']+ "==" +result[0][2])
                        validList.append(case)
                        break
        print(len(validList))
        return validList
