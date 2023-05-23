from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.advisor import AdvisorManagementClient
from azure.storage.blob import BlobServiceClient
import json
import os

subscription_id = '329132a7-0936-447c-ba81-63a86780f4da'
client_id = '7bf8b308-7216-47bc-9d52-673fc40df5c7'
client_secret = 'cAG8Q~hrvfcorn5wlOijJqBvCJZv3d3A~uYcxazl'
tenant_id = '76e4ac64-f84d-401d-8594-3f6ca5374437'

credentials = ServicePrincipalCredentials(
    client_id=client_id,
    secret=client_secret,
    tenant=tenant_id
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

storage_account_name = 'cs1100320029fc62a68'
storage_account_key = 'A3LOyw58sysUuBKpDbUf5EyHDfZpOFSPpqb9G2KyQhauW/N1fKyF6gt2VCanhe/1ujM/v2l4x3mJ+ASt3i7mRQ=='
container_name = 'resourcesinfo'

blob_service_client = BlobServiceClient.from_connection_string(f"DefaultEndpointsProtocol=https;AccountName={storage_account_name};AccountKey={storage_account_key};EndpointSuffix=core.windows.net")
blob_client = blob_service_client.get_blob_client(container=container_name, blob=output_file)
with open(output_file, "rb") as data:
    blob_client.upload_blob(data, overwrite=True)

os.remove(output_file)
