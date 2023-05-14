from st2common.runners.base_action import Action
import csv

class CsvReaderAction(Action):
    def run(self, csv_path):
        data_list = []
        with open(csv_path, mode='r', encoding='utf-8-sig') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            data_list = []
            for row in csv_reader:
                data_list.append(row)
        result = []
        for line in data_list:
            newline = dict([(k,None if not v else v) for k,v in line.items() ])
            result.append(newline)
        return result
