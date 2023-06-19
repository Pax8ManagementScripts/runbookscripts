import csv
import os
from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.storage.blob import BlobServiceClient


STORAGE_ACCOUNT_NAME = os.environ.get("STORAGE_ACCOUNT_NAME")
STORAGE_ACCOUNT_KEY = os.environ.get("STORAGE_ACCOUNT_KEY")
STORAGE_CONTAINER_NAME = os.environ.get("STORAGE_CONTAINER_NAME")

subscription_id = os.environ.get("SUBSCRIPTION_ID")
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
tenant_id = os.environ.get("TENANT_ID")

credentials = ClientSecretCredential(
    client_id = client_id,
    client_secret = client_secret,
    tenant_id = tenant_id
)
resource_client = ResourceManagementClient(credentials, subscription_id)

resources = resource_client.resources.list()

untagged_resources = []
for resource in resources:
    if not resource.tags:
        untagged_resources.append(resource)

for resource in untagged_resources:
    print("Resource ID: {} has untagged".format(resource.id)) 
    print("Resource Type: {}".format(resource.type))
    print("Resource Name: {}".format(resource.name))
    print()

file_name = f"{subscription_id}_untagged_resources.csv"
with open(file_name, 'w', newline='') as resources_file:
    writer = csv.writer(resources_file)
    writer.writerow(['Untagged Resource ID', 'Resource Name', 'Resource Type'])
    for resource in untagged_resources:
        resource_id = resource.id
        resource_name = resource.name
        resource_type = resource.type
        writer.writerow([resource_id, resource_name, resource_type])
        print(f"\tUntagged Resource ID: {resource_id}, Resource Name: {resource_name}, Resource Type: {resource_type}")

print(f"Resources written to {file_name}")
# Upload the file to blob storage
CONN_STR = f"DefaultEndpointsProtocol=https;AccountName={STORAGE_ACCOUNT_NAME};AccountKey={STORAGE_ACCOUNT_KEY};EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(CONN_STR)
container_client = blob_service_client.get_container_client(STORAGE_CONTAINER_NAME)
blob_client = container_client.get_blob_client(file_name)
with open(file_name, "rb") as data:
    blob_client.upload_blob(data, overwrite=True)

