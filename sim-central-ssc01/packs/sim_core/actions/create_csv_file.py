import csv
import json
import tempfile
from datetime import datetime
from st2common.runners.base_action import Action

class CreateCsvFileAction(Action):
    def __init__(self, config):
        super(CreateCsvFileAction, self).__init__(config)
        self.config = config

    def run(self, json_data, file_path):
        data_file = open(file_path, 'w+', newline='')
        writer = csv.writer(data_file)
        count = 0
        for data in json_data:
            if count == 0:
                header = data.keys()
                writer.writerow(header)
                count += 1
            writer.writerow(data.values())

        data_file.close()
