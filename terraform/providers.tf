terraform {
  required_providers {
    github = {
      source  = "integrations/github"
      version = "~> 5.25.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.61.0"
    }
  }
  required_version = "~> 1.5.0"
}

terraform {
  backend "azurerm" {
    resource_group_name  = "pax8-cvm-tfstate"
    storage_account_name = "pax8cvmtfstate"
    container_name       = "pax8tfstate"
    key                  = "customer_github_resources.terraform.tfstate"
  }
}

# TODO: Set up OAUth token. Currently using temporary PAT
provider "github" {
  //noinspection MissingProperty
  owner = var.github_org_name
  #  app_auth {}
}

provider "azurerm" {
  subscription_id = var.cvm_subscription_id
  tenant_id       = var.cvm_tenant_id
  client_id       = var.cvm_client_id
  client_secret   = var.cvm_client_secret
  features {}
}