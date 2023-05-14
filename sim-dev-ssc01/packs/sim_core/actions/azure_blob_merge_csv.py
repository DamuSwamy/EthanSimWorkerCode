import csv
import os
import tempfile
from datetime import datetime
from azure.storage.blob import BlobServiceClient
from st2common.runners.base_action import Action

class AzuewBlobMergeCsvAction(Action):
    def __init__(self, config):
        super(AzuewBlobMergeCsvAction, self).__init__(config)

    def run(self, storage_account_name, container_name, sas_token):
        temp = tempfile.NamedTemporaryFile()
        now = datetime.now()
        csv_filename = temp.name
        self.remote_file  = f'Automation/ethan_users_{now.strftime("%Y%m%d")}.csv'
        self.blob_service_client = BlobServiceClient(account_url=f"https://{storage_account_name}.blob.core.windows.net", credential=sas_token)
        blob_container_client = self.blob_service_client.get_container_client(container_name)
        folder_path = now.strftime("%b-%Y")
        blobs = blob_container_client.walk_blobs(f'{folder_path}/', delimiter='/')
        rows = []
        count = 0
        for blob in blobs:
            if self.remote_file in blob.name or "users.csv" in blob.name or blob.size <= 0:
                continue
            rows += self.download_blob(container_name, blob, count)
            count = count + 1
        csv_string = ''
        if len(rows) > 0:
            with open(csv_filename, 'w+', newline='') as merged_file:
                writer = csv.writer(merged_file)
                writer.writerows(rows)
            with open(csv_filename, 'r') as f:
                csv_string = f.read()
        self.upload_blob(container_name, csv_string)
        temp.close()

    def download_blob(self, container_name, blob, counter):
        blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=blob.name)
        blob_string = blob_client.download_blob().content_as_text()
        reader = csv.reader(blob_string.split('\n'))
        if counter != 0:
            header = next(reader)
        return [row for row in reader if any(cell.strip() for cell in row)]

    def upload_blob(self, container_name, data):
        blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=self.remote_file)
        blob_client.upload_blob(data, overwrite=True)
