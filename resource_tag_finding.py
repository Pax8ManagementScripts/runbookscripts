import os
from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient

subscription_id = os.environ.get("SUBSCRIPTION_ID")
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
tenant_id = os.environ.get("TENANT_ID")

credentials = ClientSecretCredential(
    client_id = client_id,
    client_secret = client_secret,
    tenant = tenant_id
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
