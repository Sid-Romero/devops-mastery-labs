# Lab 68: Kubernetes Release Approvals with a Mock System

![Difficulty: Medium](https://img.shields.io/badge/Difficulty-Medium-yellow) ![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?logo=kubernetes&logoColor=white)

> **Auto-generated lab** - Created on 2026-01-22

## Description

This lab simulates a release approval workflow in Kubernetes. It demonstrates how to pause a deployment and require manual approval before proceeding, ensuring control over releases.

## Learning Objectives

- Understand the concept of release approvals in CD.
- Implement a basic deployment strategy that requires manual approval.
- Learn how to pause and resume Kubernetes deployments.

## Prerequisites

- kubectl installed and configured to connect to a Kubernetes cluster (e.g., minikube, Docker Desktop)
- Basic understanding of Kubernetes deployments and services
- A text editor for creating YAML files

## Lab Steps

### Step 1: Step 1: Create a Basic Deployment

First, let's create a simple deployment for a web application. Create a file named `app-deployment.yaml` with the following content:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  labels:
    app: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: nginx:latest
        ports:
        - containerPort: 80
```

Apply this deployment to your cluster:

```bash
kubectl apply -f app-deployment.yaml
```

Verify that the deployment is running:

```bash
kubectl get deployments
kubectl get pods
```

### Step 2: Step 2: Expose the Deployment with a Service

Next, expose the deployment using a service. Create a file named `app-service.yaml` with the following content:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  selector:
    app: my-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: LoadBalancer
```

Apply this service to your cluster:

```bash
kubectl apply -f app-service.yaml
```

Get the service's external IP or hostname (if using minikube, use `minikube service my-app-service`):

```bash
kubectl get services
```

Access the application in your browser using the obtained IP or hostname.

### Step 3: Step 3: Simulate a Release Approval Process

Now, let's simulate a release approval process. We will pause the deployment by scaling it down to zero replicas. This represents a hold before the actual release.

Scale the deployment down to zero:

```bash
kubectl scale deployment my-app --replicas=0
```

Verify that the pods are terminated:

```bash
kubectl get pods
```

At this point, imagine that a manual approval step is required. This could involve a person reviewing the changes, running tests, or any other validation process.

### Step 4: Step 4: 'Approve' and Resume the Deployment

After the 'approval' is granted, resume the deployment by scaling it back to the desired number of replicas (e.g., 3):

```bash
kubectl scale deployment my-app --replicas=3
```

Verify that the pods are running again:

```bash
kubectl get pods
```

Access the application in your browser to ensure it's working as expected.

### Step 5: Step 5: Implementing a Real Approval Workflow (Discussion)

This lab uses a manual `kubectl scale` command to simulate the approval process. In a real-world scenario, you would automate this process using CI/CD tools and external approval systems.

Consider these points:

*   **CI/CD Integration:** Integrate the scaling commands into your CI/CD pipeline (e.g., Jenkins, GitLab CI, Argo CD). The pipeline should pause before scaling up the deployment and wait for an external signal (e.g., an API call from an approval system).
*   **Approval System:** Use an external system (e.g., a custom web application, a service like Harness or Spinnaker) to manage the approval process. This system should provide a user interface for reviewers to approve or reject releases.
*   **Automated Rollbacks:** Implement automated rollbacks if the deployment fails after approval. This can be done by monitoring the deployment's health and automatically scaling down the deployment if errors are detected.


<details>
<summary> Hints (click to expand)</summary>

1. If the service doesn't get an external IP, try deleting and recreating it. If using minikube, make sure it's running.
2. Ensure the selector labels in the service match the pod labels in the deployment.
3. The scaling commands are essential for pausing and resuming the deployment. Double-check the deployment name.

</details>


<details>
<summary>✅ Solution Notes (spoiler)</summary>

The solution involves creating a basic deployment and service, then using `kubectl scale` to simulate pausing and resuming the deployment based on a manual approval. A real implementation would integrate this with a CI/CD pipeline and an external approval system for full automation.

</details>


---

## Notes

- **Difficulty:** Medium
- **Estimated time:** 45-75 minutes
- **Technology:** Kubernetes

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
