import os
from github import GithubIntegration, Auth
# GitHub App ID and private key

# GitHub repository details
owner = os.environ.get("GITHUB_REPOSITORY_OWNER")
repo = os.environ.get("GITHUB_REPOSITORY")

# GitHub App ID and private key
app_id = os.environ.get("GITHUB_APP_ID")
private_key = os.environ.get("GITHUB_PRIVATE_KEY")

# ### DEBUG
# # GitHub repository details
# owner = os.environ.get("GITHUB_REPOSITORY_OWNER")
# repo = "CloudVendingMachine/cvm-pax8"

# # GitHub App ID and private key
# app_id = os.environ.get("GITHUB_APP_ID")
# private_key = os.environ.get("GITHUB_APP_ID")


# Create a GitHub integration object
integration = GithubIntegration(auth=Auth.AppAuth(app_id=app_id, private_key=private_key))

# Get an installation access token
installation_id = integration.get_repo_installation(owner=owner, repo=repo).id

access_token = integration.get_access_token(installation_id).token

print(access_token)