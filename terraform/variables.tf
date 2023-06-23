variable "clients" {
  type = map(object({
    default_branch = optional(string, "prod")
    branches       = optional(list(string))
    github_variables = optional(map(object({
      akv_key = optional(string) # Either AKV key or plaintext value must be set
      value   = optional(string)
      secret  = bool
    })))
  }))
  description = "Map of clients to create"
  default     = {}
}

variable "repo_prefix" {
  type        = string
  description = "(Optional) The prefix to append to the repository name. Defaults to cvm"
  default     = "cvm"
}

variable "github_org_name" {
  type        = string
  description = "(Required) The name of the GitHub organization/owner"
}

variable "template_owner" {
  type        = string
  description = "(Required) The GitHub organization or user the template repository is owned by"
}

variable "template_repo_name" {
  type        = string
  description = "(Required) The name of the template repository"
}

variable "cvm_sa_name" {
  type        = string
  description = "(Required) The name of the Azure Key Vault that stores customers data"
  sensitive   = true
}

variable "cvm_sa_resource_group_name" {
  type        = string
  description = "(Required) The name of the CVM AKV resource group"
  sensitive   = true
}

variable "cvm_akv_name" {
  type        = string
  description = "(Required) The name of the Azure Key Vault that stores customers data"
  sensitive   = true
}

variable "cvm_akv_resource_group_name" {
  type        = string
  description = "(Required) The name of the CVM AKV resource group"
  sensitive   = true
}

variable "cvm_subscription_id" {
  type        = string
  description = "(Required) Subscription ID where AKV is located"
  sensitive   = true
}

variable "cvm_tenant_id" {
  type        = string
  description = "(Required) Tenant ID where AKV is located"
  sensitive   = true
}
variable "cvm_client_id" {
  type        = string
  description = "(Required) App/SP ID that has access to AKV"
  sensitive   = true
}
variable "cvm_client_secret" {
  type        = string
  description = "(Required) App/SP secret that has access to AKV"
  sensitive   = true
}