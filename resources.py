import csv
import os
from azure.common.credentials import ServicePrincipalCredentials
from azure.keyvault.secrets import SecretClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.subscription import SubscriptionClient
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from automationassets import get_automation_variable
from azure.identity import DefaultAzureCredential
from azure.mgmt.storage import StorageManagementClient

STORAGE_ACCOUNT_NAME = 'vustorage102'
RESOURCE_GROUP_NAME = 'vu-storage-rg'


# VAULT_URI = 'https://kv-pax8-tst.vault.azure.net/' #get_automation_variable('VAULT_URI')
AZURE_CLIENT_ID_SECRET_NAMES = ['sre-as-a-service-sbx-id', 'sre-as-a-service-tst-id', 'sre-as-a-service-prd-id'] #get_automation_variable('AZURE_CLIENT_ID_SECRET_NAMES').split(',')
AZURE_CLIENT_SECRET_SECRET_NAMES = ['sre-as-a-service-sbx-secret', 'sre-as-a-service-tst-secret', 'sre-as-a-service-prd-secret'] #get_automation_variable('AZURE_CLIENT_SECRET_SECRET_NAMES').split(',')
STORAGE_CONTAINER_NAME = 'vustorage'

credential = DefaultAzureCredential()
# secret_client = SecretClient(vault_url=VAULT_URI, credential=credential)

subscription_ids = []
azure_client_ids = []
azure_client_secrets = []

for i in range(len(AZURE_CLIENT_ID_SECRET_NAMES)):
    azure_client_id_secret_name = AZURE_CLIENT_ID_SECRET_NAMES[i]
    azure_client_secret_secret_name = AZURE_CLIENT_SECRET_SECRET_NAMES[i]

    azure_client_id = os.environ.get(azure_client_id_secret_name)
    azure_client_secret = os.environ.get(azure_client_secret_secret_name)

    credentials = ServicePrincipalCredentials(
        client_id = azure_client_id,
        secret = azure_client_secret,
        tenant = os.environ.get("TENANT_ID")
    )

    subscription_client = SubscriptionClient(credentials)
    subscription_ids.append(next(subscription_client.subscriptions.list()).subscription_id)
    azure_client_ids.append(azure_client_id)
    azure_client_secrets.append(azure_client_secret)

for i in range(len(subscription_ids)):
    subscription_id = subscription_ids[i]
    azure_client_id = azure_client_ids[i]
    azure_client_secret = azure_client_secrets[i]

    credentials = ServicePrincipalCredentials(
        client_id = azure_client_id,
        secret = azure_client_secret,
        tenant = os.environ.get("TENANT_ID")
    )

    subscription_client = SubscriptionClient(credentials)
    subscription_name = subscription_client.subscriptions.get(subscription_id).display_name
    print(f"Subscription ID: {subscription_id}, Subscription Name: {subscription_name}")

    resource_client = ResourceManagementClient(credentials, subscription_id)
    resource_list = resource_client.resources.list()

    file_name = f"resources_{subscription_id}.csv"
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
    blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=vustorage102;AccountKey=LEBMbcT4pVm2+idafWutNGw31wn1oflywxWN9UGs6uo1OcUy2gflG5L2zub7LMgnsIckZmawiRSO+AStVW5dPg==;EndpointSuffix=core.windows.net")
    container_client = blob_service_client.get_container_client(STORAGE_CONTAINER_NAME)
    blob_client = container_client.get_blob_client(f"resources_{subscription_id}.csv")
    with open(file_name, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)

print("All resources written to CSV files and uploaded to blob storage")

print("All resources written to CSV files")
