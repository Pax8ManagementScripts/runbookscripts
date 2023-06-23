module "github" {
  source   = "./modules/github"
  for_each = var.clients

  repo_name                   = "${var.repo_prefix}-${each.key}"
  github_org_name             = var.github_org_name
  template_owner              = var.template_owner
  template_repo_name          = var.template_repo_name
  github_variables            = each.value.github_variables
  branches                    = each.value.branches
  cvm_subscription_id         = var.cvm_subscription_id
  cvm_tenant_id               = var.cvm_tenant_id
  cvm_client_id               = var.cvm_client_id
  cvm_client_secret           = var.cvm_client_secret
  cvm_akv_name                = var.cvm_akv_name
  cvm_akv_resource_group_name = var.cvm_akv_resource_group_name
  cvm_backend_container_name  = azurerm_storage_container.client[each.key].name
  cvm_backend_key             = "cvm_${each.key}.terraform.tfstate"
  cvm_backend_rg_name         = var.cvm_sa_resource_group_name
  cvm_backend_sa_name         = var.cvm_sa_name
}