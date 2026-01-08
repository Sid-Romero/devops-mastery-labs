# Lab 54: Terraform: Recovering from RunContainerError

![Difficulty: Medium](https://img.shields.io/badge/Difficulty-Medium-yellow) 

> **Auto-generated lab** - Created on 2026-01-08

## Description

This lab simulates a common 'RunContainerError' scenario in Kubernetes caused by insufficient resources. You will use Terraform to define and deploy a Kubernetes pod, intentionally trigger the error, and then use Terraform to adjust resource limits and redeploy, resolving the issue.

## Learning Objectives

- Understand how Terraform can be used to define Kubernetes resources.
- Learn to identify and diagnose 'RunContainerError' issues in Kubernetes.
- Practice modifying Kubernetes pod resource limits using Terraform.
- Understand the Terraform apply process for updating existing infrastructure.

## Prerequisites

- Terraform installed (>= 1.0)
- kubectl installed and configured to connect to a Kubernetes cluster (minikube, Docker Desktop, or similar)
- Basic understanding of Kubernetes pods and resource limits
- A code editor

## Lab Steps

### Step 1: Initialize Terraform and Define Provider

Create a new directory for your Terraform project. Inside this directory, create a file named `main.tf` and add the following content to configure the Kubernetes provider:

```terraform
terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.0"
    }
  }
}

provider "kubernetes" {
  # Configuration options for connecting to your Kubernetes cluster
  # If kubectl is configured, Terraform will use the same configuration
}
```

Next, initialize the Terraform project:

```bash
terraform init
```

### Step 2: Define a Kubernetes Pod with Limited Resources

In the `main.tf` file, define a Kubernetes pod with intentionally limited resources. This will trigger a `RunContainerError` when the pod is deployed. Add the following code block to your `main.tf` file:

```terraform
resource "kubernetes_namespace" "example" {
  metadata {
    name = "runcontainererror-example"
  }
}

resource "kubernetes_pod" "example" {
  metadata {
    name      = "resource-limited-pod"
    namespace = kubernetes_namespace.example.metadata.0.name
  }

  spec {
    container {
      image = "nginx:latest"
      name  = "nginx"

      resources {
        limits = {
          cpu    = "10m" # 10 millicores
          memory = "10Mi" # 10 megabytes
        }
        requests = {
          cpu    = "10m"
          memory = "10Mi"
        }
      }
    }
  }
}
```

### Step 3: Apply the Terraform Configuration

Apply the Terraform configuration to create the Kubernetes pod:

```bash
terraform apply
```

Type `yes` when prompted to confirm the changes.

### Step 4: Verify the 'RunContainerError'

Use `kubectl` to check the status of the pod. You should see that the pod is in a state like `ImagePullBackOff` or `CrashLoopBackOff` related to resource constraints.

```bash
kubectl get pods -n runcontainererror-example
kubectl describe pod resource-limited-pod -n runcontainererror-example
```

Examine the output of `kubectl describe pod` to confirm the `RunContainerError` due to insufficient resources. Look for events related to resource limits.

### Step 5: Modify Resource Limits in Terraform

Edit the `main.tf` file to increase the resource limits for the pod. Change the `cpu` and `memory` limits to more reasonable values, such as:

```terraform
      resources {
        limits = {
          cpu    = "200m"
          memory = "256Mi"
        }
        requests = {
          cpu    = "100m"
          memory = "128Mi"
        }
      }
```

### Step 6: Apply the Updated Configuration

Apply the updated Terraform configuration:

```bash
terraform apply
```

Type `yes` when prompted to confirm the changes.

### Step 7: Verify the Pod is Running

Use `kubectl` to check the status of the pod again. This time, the pod should be running successfully.

```bash
kubectl get pods -n runcontainererror-example
```

The pod's status should now be `Running`.

### Step 8: Clean Up

To clean up the resources created by Terraform, run:

```bash
terraform destroy
```

Type `yes` when prompted to confirm the destruction.


<details>
<summary> Hints (click to expand)</summary>

1. If `terraform init` fails, ensure you have the correct provider configured and that your network allows Terraform to download the provider.
2. If the pod remains in a failing state after increasing resource limits, double-check your resource definitions in `main.tf` and ensure you have applied the changes correctly with `terraform apply`.
3. Ensure your Kubernetes context is correctly set to your desired cluster before running `terraform apply`.

</details>


<details>
<summary>✅ Solution Notes (spoiler)</summary>

The solution involves creating a basic Kubernetes pod using Terraform, observing the 'RunContainerError' due to insufficient resources, and then modifying the resource limits in the Terraform configuration to resolve the error. The key is understanding how to define and update Kubernetes resources using Terraform and how to interpret Kubernetes pod status to diagnose resource-related issues. Remember to destroy the resources after the lab.

</details>


---

## Notes

- **Difficulty:** Medium
- **Estimated time:** 45-75 minutes
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
