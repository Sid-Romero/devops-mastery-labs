# Lab 09: CI/CD with Kubernetes: Automated Deployments

![Difficulty: Medium](https://img.shields.io/badge/Difficulty-Medium-yellow) ![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?logo=kubernetes&logoColor=white)

> **Auto-generated lab** - Created on 2025-12-27

## Description

This lab demonstrates a basic CI/CD pipeline for a simple application deployed on Kubernetes. It focuses on automating deployments using `kubectl` and understanding the core concepts of continuous integration and continuous delivery.

## Learning Objectives

- Understand the basic principles of CI/CD.
- Learn how to automate Kubernetes deployments.
- Practice using `kubectl` for managing deployments.
- Implement a simple deployment pipeline using shell scripting.

## Prerequisites

- kubectl installed and configured
- A Kubernetes cluster (e.g., Minikube, Docker Desktop)
- Docker installed

## Lab Steps

### Step 1: 1. Create a Simple Application

Let's start by creating a very simple application. This application will simply serve a static HTML page. Create a file named `index.html` with the following content:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Kubernetes CI/CD Demo</title>
</head>
<body>
    <h1>Hello, Kubernetes!</h1>
    <p>Version: 1.0</p>
</body>
</html>
```

Next, create a simple `Dockerfile` to serve this HTML page using a basic web server like `nginx`.

```dockerfile
FROM nginx:latest

COPY index.html /usr/share/nginx/html/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### Step 2: 2. Build and Push the Docker Image

Now, build the Docker image and push it to a container registry (e.g., Docker Hub). Replace `<your-dockerhub-username>` with your actual Docker Hub username or registry.

```bash
docker build -t <your-dockerhub-username>/k8s-cicd-demo:1.0 .
docker login -u <your-dockerhub-username>
docker push <your-dockerhub-username>/k8s-cicd-demo:1.0
```

Make sure you are logged in to Docker Hub before pushing the image.

### Step 3: 3. Create a Kubernetes Deployment

Create a Kubernetes deployment file named `deployment.yaml`.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: k8s-cicd-demo
spec:
  replicas: 2
  selector:
    matchLabels:
      app: k8s-cicd-demo
  template:
    metadata:
      labels:
        app: k8s-cicd-demo
    spec:
      containers:
      - name: k8s-cicd-demo
        image: <your-dockerhub-username>/k8s-cicd-demo:1.0
        ports:
        - containerPort: 80
```

Replace `<your-dockerhub-username>` with your Docker Hub username.  Apply the deployment:

```bash
kubectl apply -f deployment.yaml
```

### Step 4: 4. Create a Kubernetes Service

Create a Kubernetes service to expose the deployment. Create a file named `service.yaml`.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: k8s-cicd-demo-service
spec:
  selector:
    app: k8s-cicd-demo
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
  type: LoadBalancer
```

Apply the service:

```bash
kubectl apply -f service.yaml
```

Note: `LoadBalancer` type might not be supported in all local Kubernetes environments (like Minikube). If that's the case, use `NodePort` and access the service via the node's IP and assigned port.  You can get the service's URL with `kubectl get service k8s-cicd-demo-service`.

### Step 5: 5. Simulate a Code Change and Update the Deployment

Now, let's simulate a code change. Modify the `index.html` file to change the version number.

```html
<!DOCTYPE html>
<html>
<head>
    <title>Kubernetes CI/CD Demo</title>
</head>
<body>
    <h1>Hello, Kubernetes!</h1>
    <p>Version: 1.1</p>
</body>
</html>
```

Build and push a new Docker image with the updated version.

```bash
docker build -t <your-dockerhub-username>/k8s-cicd-demo:1.1 .
docker push <your-dockerhub-username>/k8s-cicd-demo:1.1
```

### Step 6: 6. Automate Deployment Update with Script

Create a script named `deploy.sh` to automate the deployment update.  This script will update the Kubernetes deployment with the new image version.

```bash
#!/bin/bash

# Set the Docker image name and tag
IMAGE_NAME=<your-dockerhub-username>/k8s-cicd-demo
IMAGE_TAG=1.1

# Update the Kubernetes deployment
kubectl set image deployment/k8s-cicd-demo k8s-cicd-demo=$IMAGE_NAME:$IMAGE_TAG

# Verify the deployment
kubectl rollout status deployment/k8s-cicd-demo
kubectl get pods -l app=k8s-cicd-demo
```

Replace `<your-dockerhub-username>` with your Docker Hub username. Make the script executable and run it:

```bash
chmod +x deploy.sh
./deploy.sh
```

Verify that the deployment has been updated and the new version is running by accessing the service endpoint. It might take a few minutes for the changes to propagate.


<details>
<summary> Hints (click to expand)</summary>

1. Make sure your Docker Hub repository is public or you've configured image pull secrets in Kubernetes.
2. If the `kubectl apply` command fails, check your YAML files for syntax errors.
3. If the service is not accessible, ensure your Kubernetes cluster is running correctly and the service is properly configured.
4. If the deployment doesn't update, check the `deploy.sh` script for errors and ensure the image tag is correct.

</details>


<details>
<summary>✅ Solution Notes (spoiler)</summary>

The complete solution involves building a simple web application, containerizing it with Docker, pushing the image to a container registry, deploying it to Kubernetes using deployment and service configurations, and automating updates using a shell script. This demonstrates a basic CI/CD pipeline for Kubernetes deployments.

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
