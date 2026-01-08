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
          cpu    = "10m"
          memory = "10Mi"
        }
        requests = {
          cpu    = "10m"
          memory = "10Mi"
        }
      }
    }
  }
}