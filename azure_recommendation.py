import json
import csv
import os
from azure.identity import ClientSecretCredential
from azure.mgmt.advisor import AdvisorManagementClient
from azure.storage.blob import BlobServiceClient

storage_account_name = os.environ.get("STORAGE_ACCOUNT_NAME")
storage_account_key = os.environ.get("STORAGE_ACCOUNT_KEY")
container_name = os.environ.get("STORAGE_CONTAINER_NAME")

subscription_id = os.environ.get("SUBSCRIPTION_ID")
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
tenant_id = os.environ.get("TENANT_ID")

def saveDataToCsv(data, csvfile):
    data_file = open(csvfile, 'w')
    csv_writer = csv.writer(data_file)
    count = 0
    for i in data:
        if count == 0:
            header = i.keys()
            csv_writer.writerow(header)
            count += 1
        csv_writer.writerow(i.values())
    data_file.close()

credentials = ClientSecretCredential(
    client_id = client_id,
    client_secret = client_secret,
    tenant_id = tenant_id
)

advisor_client = AdvisorManagementClient(credentials, subscription_id)

recommendations = advisor_client.recommendations.list()

recommendations_list = []
for recommendation in recommendations:
    recommendation_dict = recommendation.as_dict()
    recommendations_list.append(recommendation_dict)

output_file = "azure_recommendations.csv"
saveDataToCsv(recommendations_list, output_file)

# Upload the file to blob storage
CONN_STR = f"DefaultEndpointsProtocol=https;AccountName={storage_account_name};AccountKey={storage_account_key};EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(CONN_STR)
blob_client = blob_service_client.get_blob_client(container=container_name, blob=output_file)
with open(output_file, "rb") as data:
    blob_client.upload_blob(data, overwrite=True)
print(f"Resources written to {output_file}")
