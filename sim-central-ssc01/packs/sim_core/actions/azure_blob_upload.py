import csv
import tempfile
from datetime import datetime
from azure.storage.blob import BlobServiceClient
from st2common.runners.base_action import Action

class AzureBlobUploadAction(Action):
    def __init__(self, config):
        super(AzureBlobUploadAction, self).__init__(config)
        self.config = config

    def run(self, storage_account_name, container_name, json_data, input_folder_path, input_file_name, sas_config, sas_token=None):
        config = self.config
        if not sas_token:
            sas_token = config.get(sas_config)
        self.blob_service_client = BlobServiceClient(account_url=f"https://{storage_account_name}.blob.core.windows.net", credential=sas_token)
        temp = tempfile.NamedTemporaryFile()
        now = datetime.now()
        csv_filename = temp.name
        if not input_folder_path:
            input_folder_path = now.strftime("%b-%Y")
        data_file = open(csv_filename, 'w+', newline='')
        writer = csv.writer(data_file)
        count = 0
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
        temp.close()
        self.remote_file  = f'{input_folder_path}/{input_file_name}'
        self.upload_blob(container_name, csv_string)

    def upload_blob(self, container_name, csv_string):
        blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=self.remote_file)
        blob_client.upload_blob(csv_string, overwrite=True)
