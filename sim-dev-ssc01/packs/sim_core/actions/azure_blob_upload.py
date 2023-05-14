import csv
import os
from azure.storage.blob import BlobServiceClient
from st2common.runners.base_action import Action

class AzureBlobUploadAction(Action):
    def __init__(self, config):
        super(AzureBlobUploadAction, self).__init__(config)

    def run(self, storage_account_name, container_name, sas_token, data, file_name):
        self.remote_file  = f'Automation/{file_name}'
        self.blob_service_client = BlobServiceClient(account_url=f"https://{storage_account_name}.blob.core.windows.net", credential=sas_token)
        self.upload_blob(container_name, data)

    def upload_blob(self, container_name, csv_string):
        blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=self.remote_file)
        blob_client.upload_blob(csv_string, overwrite=True)
