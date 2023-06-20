import csv
import os
from azure.common.credentials import ServicePrincipalCredentials
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.subscription import SubscriptionClient
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
# from automationassets import get_automation_variable
from azure.identity import DefaultAzureCredential
from azure.mgmt.storage import StorageManagementClient

STORAGE_ACCOUNT_NAME = os.environ.get("STORAGE_ACCOUNT_NAME")
STORAGE_ACCOUNT_KEY = os.environ.get("STORAGE_ACCOUNT_KEY")
STORAGE_CONTAINER_NAME = os.environ.get("STORAGE_CONTAINER_NAME")

azure_client_id = os.environ.get("CLIENT_ID")
azure_client_secret = os.environ.get("CLIENT_SECRET")
tenant_id = os.environ.get("TENANT_ID")

credentials = ClientSecretCredential(
    client_id = azure_client_id,
    client_secret = azure_client_secret,
    tenant_id = tenant_id
)

subscription_client = SubscriptionClient(credentials)
file_name = f"resources.csv"

for i in subscription_client.subscriptions.list():
    subscription_id = i.subscription_id
    subscription_name = i.display_name
    print(f"Subscription ID: {subscription_id}, Subscription Name: {subscription_name}")

    resource_client = ResourceManagementClient(credentials, subscription_id)
    resource_list = resource_client.resources.list()

    with open(file_name, 'w', newline='') as resources_file:
        writer = csv.writer(resources_file)
        writer.writerow(['Subscription ID', 'Subscription Name', 'Resource Name', 'Resource Type'])
        for resource in resource_list:
            resource_name = resource.name
            resource_type = resource.type
            writer.writerow([subscription_id, subscription_name, resource_name, resource_type])
            print(f"\tResource Name: {resource_name}, Resource Type: {resource_type}")

print(f"Resources written to {file_name}")
# Upload the file to blob storage
CONN_STR = f"DefaultEndpointsProtocol=https;AccountName={STORAGE_ACCOUNT_NAME};AccountKey={STORAGE_ACCOUNT_KEY};EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(CONN_STR)
container_client = blob_service_client.get_container_client(STORAGE_CONTAINER_NAME)
blob_client = container_client.get_blob_client(file_name)
with open(file_name, "rb") as data:
    blob_client.upload_blob(data, overwrite=True)

print("All resources written to CSV files and uploaded to blob storage")

print("All resources written to CSV files")
