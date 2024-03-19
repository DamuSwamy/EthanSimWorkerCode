from azure.storage.blob import BlobServiceClient, BlobClient
import os

# Provided details
root_directory = 'https://adlsreconprodeastus2001.blob.core.windows.net/unbilledusagefastpath/v1/202403040206/PartnerTenantId=d0aaafc0-4f56-478a-b986-fd9eb70046d6/BillingMonth=202402/Currency=AUD/Fragment=full/PartitionType=default'
sas_token = 'skoid=40e83195-ec1b-41e1-96eb-b4514bdbc027&sktid=975f013f-7f24-47e8-a7d3-abc4752bf346&skt=2024-03-19T08%3A55%3A11Z&ske=2024-03-20T08%3A55%3A11Z&sks=b&skv=2021-08-06&sv=2021-08-06&se=2024-03-19T09%3A55%3A11Z&sr=d&sp=rl&sdd=7&sig=r80gcGwD6cNw7kMF%2BYxDwHFsY6awBqWGf9kYYzsQJjM%3D'
blob_name = 'part-00187-b58e86ff-7ff7-4aa7-82a5-aa2294c7cd2e.c000.json.gz'

# Construct the full blob URL
blob_url = "{}/{}?{}".format(root_directory, blob_name, sas_token)


# Initialize a BlobClient
blob_client = BlobClient.from_blob_url(blob_url=blob_url)

# Download the blob
file_name = blob_name.split('/')[-1]
with open(file_name, "wb") as download_file:
    download_blob = blob_client.download_blob()
    download_blob.readinto(download_file)

print("Blob downloaded to " + file_name)
