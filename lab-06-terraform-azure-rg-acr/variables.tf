variable "resource_group_name" {
  type        = string
  description = "The name of the resource group"
  default     = "devops-rg"
}

variable "location" {
  type        = string
  description = "The Azure region to deploy resources into"
  default     = "canadacentral"
}

variable "acr_name" {
  type        = string
  description = "The name of the Azure Container Registry"
  default     = "myuniqueacrname"
}

variable "acr_sku" {
  type        = string
  description = "The SKU of the Azure Container Registry"
  default     = "Basic"
}