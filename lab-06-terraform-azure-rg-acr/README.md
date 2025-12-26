# Lab 06: Terraform: Azure Resource Group & ACR Setup

![Difficulty: Easy](https://img.shields.io/badge/Difficulty-Easy-brightgreen) 

> **Auto-generated lab** - Created on 2025-12-26

## Description

This lab guides you through setting up an Azure Resource Group and Azure Container Registry using Terraform. You'll learn how to define resources, manage state, and apply configurations to Azure.

## Learning Objectives

- Learn to define Azure resources using Terraform.
- Understand Terraform state management.
- Deploy an Azure Resource Group and Container Registry.
- Use Terraform providers and variables.

## Prerequisites

- Azure subscription
- Terraform installed (version 1.0 or later)
- Azure CLI installed and configured (az login)
- Text editor or IDE

## Lab Steps

### Step 1: Step 1: Project Setup and Provider Configuration

Create a new directory for your Terraform project, e.g., `terraform-azure-acr`. Inside this directory, create a file named `main.tf`. This file will contain your Terraform configuration.

Add the Azure provider configuration to `main.tf`:

```terraform
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
  required_version = ">= 1.0"
}

provider "azurerm" {
  features {}
}
```

Create a `variables.tf` file to define input variables. This helps make your configuration reusable and configurable. Add the following variables:

```terraform
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
```

**Note:** Replace `myuniqueacrname` with a globally unique name for your ACR. ACR names must be globally unique within Azure.


### Step 2: Step 2: Define the Azure Resource Group

In your `main.tf` file, define the Azure Resource Group using the `azurerm_resource_group` resource. Reference the variables defined in `variables.tf`:

```terraform
resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
}
```

### Step 3: Step 3: Define the Azure Container Registry

Now, define the Azure Container Registry using the `azurerm_container_registry` resource in `main.tf`.  Reference the resource group and ACR variables:

```terraform
resource "azurerm_container_registry" "acr" {
  name                = var.acr_name
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = var.acr_sku
  admin_enabled       = false
}
```

### Step 4: Step 4: Initialize, Plan, and Apply

Open your terminal and navigate to the Terraform project directory. Run the following commands:

1.  **Initialize Terraform:**

    ```bash
    terraform init
    ```

    This command downloads the necessary provider plugins.

2.  **Create a Terraform Plan:**

    ```bash
    terraform plan
    ```

    This command shows you the changes that Terraform will make to your Azure environment. Review the plan carefully.

3.  **Apply the Configuration:**

    ```bash
    terraform apply
    ```

    Type `yes` when prompted to confirm the changes. This command will create the Resource Group and Container Registry in Azure.

4. **Verify in Azure Portal**: Login to the Azure Portal and verify the resource group and container registry have been created.

### Step 5: Step 5: Output Values (Optional)

To output the ACR login server URL, add the following to `main.tf`:

```terraform
output "acr_login_server" {
  value = azurerm_container_registry.acr.login_server
}
```

Then, run `terraform apply` again.  The login server URL will be displayed as an output.

### Step 6: Step 6: Cleanup

To destroy the resources created by Terraform, run the following command:

```bash
terraform destroy
```

Type `yes` when prompted to confirm. This will delete the Resource Group and Container Registry from Azure.


<details>
<summary> Hints (click to expand)</summary>

1. Make sure your Azure CLI is logged in and configured correctly using `az login` and `az account set --subscription <your_subscription_id>`.
2. The ACR name must be globally unique. If you get an error about the name being taken, choose a different name.
3. Ensure the azurerm provider version in your Terraform configuration is compatible with your Terraform version.
4. If `terraform init` fails, check your Terraform configuration for syntax errors and verify that the provider is available.

</details>


<details>
<summary>✅ Solution Notes (spoiler)</summary>

This lab demonstrates a basic Terraform setup for Azure. The solution involves creating a `main.tf` file to define the resources and using `terraform init`, `terraform plan`, and `terraform apply` to deploy the infrastructure. Remember to destroy the resources using `terraform destroy` when you are finished.

</details>


---

## Notes

- **Difficulty:** Easy
- **Estimated time:** 30-45 minutes
- **Technology:** Terraform

##  Cleanup

Don't forget to clean up resources after completing the lab:

```bash
# Example cleanup commands (adjust based on lab content)
docker system prune -f
# or
kubectl delete -f .
# or
helm uninstall <release-name>
```

---

*This lab was auto-generated by the [Lab Generator Bot](../.github/workflows/generate-lab.yml)*
