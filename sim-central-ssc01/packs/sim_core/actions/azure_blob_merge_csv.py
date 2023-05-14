import csv
import json
import os
import tempfile
from datetime import datetime
from azure.storage.blob import BlobServiceClient
from st2common.runners.base_action import Action

class AzuewBlobMergeCsvAction(Action):
    def __init__(self, config):
        super(AzuewBlobMergeCsvAction, self).__init__(config)
        self.config = config

    def run(self, storage_account_name, container_name, input_folder_path, output_folder_path, sas_config, sas_token=None):
        config = self.config
        if not sas_token:
            sas_token = config.get(sas_config)
        temp = tempfile.NamedTemporaryFile()
        now = datetime.now()
        csv_filename = temp.name
        self.remote_file  = f'{output_folder_path}/ethan_users_{now.strftime("%Y%m%d")}_output.csv'
        self.blob_service_client = BlobServiceClient(account_url=f"https://{storage_account_name}.blob.core.windows.net", credential=sas_token)
        blob_container_client = self.blob_service_client.get_container_client(container_name)
        if not input_folder_path:
            input_folder_path = now.strftime("%b-%Y")
        blobs = blob_container_client.walk_blobs(f'{input_folder_path}/', delimiter='/')
        users = []
        for blob in blobs:
            if self.remote_file in blob.name or "users.csv" in blob.name or ".csv" not in blob.name or blob.size <= 0:
                continue
            users += self.covert_csv_to_json(self.download_blob(container_name, blob.name))
        self.create_csv_blob(container_name, csv_filename, users)
        temp.close()
        return users

    def create_csv_blob(self, container_name, csv_filename, json_data):
        data_file = open(csv_filename, 'w+', newline='')
        writer = csv.writer(data_file)
        count = 0
        json_str = json.dumps(json_data, sort_keys=True)
        json_data = json.loads(json_str)
        for data in json_data:
            if count == 0:
                header = data.keys()
                writer.writerow(header)
                count += 1
            writer.writerow(data.values())
        data_file.close()
        csv_string = ''
        with open(csv_filename, 'r') as f:
            csv_string = f.read()
        self.upload_blob(container_name, csv_string)


    def download_blob(self, container_name, blob):
        blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=blob)
        blob_string = blob_client.download_blob().content_as_text()
        reader = csv.DictReader(blob_string.split('\n'))
        return reader

    def covert_csv_to_json(self, reader):
        data_list = []
        for row in reader:
            data_list.append(row)
        result = []
        for line in data_list:
            newline = dict([(k,None if not v else v) for k,v in line.items() ])
            result.append(newline)
        return result

    def upload_blob(self, container_name, data):
        blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=self.remote_file)
        blob_client.upload_blob(data, overwrite=True)
