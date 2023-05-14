import csv
from io import StringIO
from azure.storage.blob import BlobServiceClient
from st2common.runners.base_action import Action

class AzureBlobDownloadAction(Action):
    def __init__(self, config):
        super(AzureBlobDownloadAction, self).__init__(config)
        self.config = config

    def run(self, storage_account_name, container_name, file_path, sas_config, sas_token=None):
        config = self.config
        if not sas_token:
            sas_token = config.get(sas_config)
        self.blob_service_client = BlobServiceClient(account_url=f"https://{storage_account_name}.blob.core.windows.net", credential=sas_token)
        return self.covert_csv_to_json(self.download_blob(container_name, file_path))

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
