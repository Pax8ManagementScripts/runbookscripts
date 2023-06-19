import json
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

credentials = ClientSecretCredential(
    client_id = client_id,
    client_secret = client_secret,
    tenant = tenant_id
)

advisor_client = AdvisorManagementClient(credentials, subscription_id)

recommendations = advisor_client.recommendations.list()

recommendations_list = []
for recommendation in recommendations:
    recommendation_dict = recommendation.as_dict()
    recommendations_list.append(recommendation_dict)

output_file = 'azure_recommendations.json'
with open(output_file, 'w') as f:
    json.dump(recommendations_list, f)

blob_service_client = BlobServiceClient.from_connection_string(f"DefaultEndpointsProtocol=https;AccountName={storage_account_name};AccountKey={storage_account_key};EndpointSuffix=core.windows.net")
blob_client = blob_service_client.get_blob_client(container=container_name, blob=output_file)
with open(output_file, "rb") as data:
    blob_client.upload_blob(data, overwrite=True)

os.remove(output_file)
