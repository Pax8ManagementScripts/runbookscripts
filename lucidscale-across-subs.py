#!/usr/bin/env python3

from pandas import *
from argparse import ArgumentParser
import csv
import os
from azure.mgmt.subscription import SubscriptionClient
import subprocess
from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobServiceClient

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

for i in subscription_client.subscriptions.list():
    subscription_id = i.subscription_id
    subscription_name = i.display_name
    print("SubscriptionId: %s  --- SubscriptionName: %s" % (subscription_id, subscription_name))
    file_name = "lucidscale_%s.json" % (subscription_name)
    subprocess.call("python3 data/Lucidscale.py -s %s -o %s" % (subscription_id, file_name), shell=True)

    print(f"Resources written to {file_name}")
    # Upload the file to blob storage
    CONN_STR = f"DefaultEndpointsProtocol=https;AccountName={STORAGE_ACCOUNT_NAME};AccountKey={STORAGE_ACCOUNT_KEY};EndpointSuffix=core.windows.net"
    blob_service_client = BlobServiceClient.from_connection_string(CONN_STR)
    container_client = blob_service_client.get_container_client(STORAGE_CONTAINER_NAME)
    blob_client = container_client.get_blob_client(file_name)
    with open(file_name, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
    print("All resources written to CSV files")
