from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient

subscription_id = '329132a7-0936-447c-ba81-63a86780f4da'

client_id = '7bf8b308-7216-47bc-9d52-673fc40df5c7'
client_secret = 'cAG8Q~hrvfcorn5wlOijJqBvCJZv3d3A~uYcxazl'
tenant_id = '76e4ac64-f84d-401d-8594-3f6ca5374437'

credentials = ServicePrincipalCredentials(
    client_id=client_id,
    secret=client_secret,
    tenant=tenant_id
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
