# Lab 15: Kubernetes Zero-Downtime Deployment with Canary Release

![Difficulty: Medium](https://img.shields.io/badge/Difficulty-Medium-yellow) ![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?logo=kubernetes&logoColor=white)

> **Auto-generated lab** - Created on 2025-12-28

## Description

This lab demonstrates how to perform zero-downtime deployments in Kubernetes using rolling updates and canary releases. You will deploy a simple application and then update it with a new version, ensuring no service interruption. The lab implements canary deployment by routing a small percentage of traffic to the new version.

## Learning Objectives

- Understand the concept of zero-downtime deployments.
- Implement rolling updates in Kubernetes.
- Configure a canary release strategy using Kubernetes services.

## Prerequisites

- kubectl installed and configured to connect to a Kubernetes cluster (minikube, Docker Desktop, or cloud provider)
- Basic understanding of Kubernetes deployments and services
- Docker installed (if building the image locally)

## Lab Steps

### Step 1: Step 1: Deploy the Initial Application

First, we'll deploy a simple application. Create a `deployment.yaml` file with the following content:

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
        version: v1
    spec:
      containers:
      - name: my-app
        image: nginx:1.20 # Replace with your image, or use this simple nginx image
        ports:
        - containerPort: 80

---
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
  type: LoadBalancer # Use NodePort if LoadBalancer is not supported
```

Apply the deployment and service:

```bash
kubectl apply -f deployment.yaml
```

Verify that the pods are running and the service is available:

```bash
kubectl get deployments
kubectl get pods
kubectl get services
```

Note the external IP or NodePort assigned to the service. You may need to wait a few minutes for the LoadBalancer to provision.

### Step 2: Step 2: Create a Canary Deployment

Now, let's create a canary deployment with a new version of the application.  We will use `nginx:1.21` for the new version. Create a new file `canary-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-canary
  labels:
    app: my-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: my-app
      version: v2
  template:
    metadata:
      labels:
        app: my-app
        version: v2
    spec:
      containers:
      - name: my-app
        image: nginx:1.21 # Replace with your new version image
        ports:
        - containerPort: 80
```

Apply the canary deployment:

```bash
kubectl apply -f canary-deployment.yaml
```

Verify that the canary pod is running:

```bash
kubectl get deployments
kubectl get pods --selector=version=v2
```

### Step 3: Step 3: Configure Traffic Splitting

To direct a small percentage of traffic to the canary deployment, we'll modify the existing service. We will use labels and selectors to achieve this.

First, add a `version` label to the original deployment's pod template.  Modify your original `deployment.yaml` file to include the `version: v1` label if you haven't already.

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
        version: v1 # Add this label
    spec:
      containers:
      - name: my-app
        image: nginx:1.20
        ports:
        - containerPort: 80

---
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
  type: LoadBalancer # Use NodePort if LoadBalancer is not supported
```

Apply the updated deployment.yaml:

```bash
kubectl apply -f deployment.yaml
```

Since we are using a single service with selector `app: my-app`, Kubernetes will automatically load balance requests across all pods with that label, including both v1 and v2.  With 3 v1 replicas and 1 v2 replica, roughly 25% of traffic will go to the canary deployment.

Access the application through the service's external IP or NodePort. You should see both nginx 1.20 and nginx 1.21 responses intermittently. If you don't see the canary, verify your labels and selectors.

### Step 4: Step 4: Monitor and Validate the Canary Release

Monitor the canary deployment for errors or performance issues.  You can use tools like Prometheus and Grafana to collect metrics and visualize the performance of both versions. You can also check the logs of the canary pod:

```bash
kubectl logs -f <canary-pod-name>
```

If the canary release is successful, you can proceed to fully roll out the new version. If issues are found, you can quickly roll back the canary deployment by scaling it down to zero replicas:

```bash
kubectl scale deployment my-app-canary --replicas=0
```

### Step 5: Step 5: Full Rollout (if Canary is Successful)

If the canary release proves successful, scale down the original deployment and scale up the canary deployment to match the desired number of replicas.

Scale down the original deployment:

```bash
kubectl scale deployment my-app --replicas=0
```

Scale up the canary deployment and rename it to the original deployment name:

```bash
kubectl scale deployment my-app-canary --replicas=3
kubectl set deployment my-app-canary --selector app=my-app,version=v2 -o yaml | sed 's/name: my-app-canary/name: my-app/g' | kubectl apply -f -
```

Cleanup the old canary deployment:
```bash
kubectl delete deployment my-app-canary
```

Update the service selector to point to the new version (v2). Edit the `deployment.yaml` file and update service `spec.selector` to match the new selector (`app: my-app`):

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
  type: LoadBalancer # Use NodePort if LoadBalancer is not supported
```

Apply the updated `deployment.yaml`

```bash
kubectl apply -f deployment.yaml
```

Verify that all traffic is now directed to the new version. Access the application through the service's external IP or NodePort.


<details>
<summary> Hints (click to expand)</summary>

1. Ensure your labels and selectors are correctly configured to route traffic to both versions.
2. Check the logs of your pods to identify any errors.
3. If the LoadBalancer service type is not supported, use NodePort and access the application through the node's IP address and the assigned port.

</details>


<details>
<summary>✅ Solution Notes (spoiler)</summary>

The solution involves creating two deployments: one for the original version and one for the canary version. A single service is used to route traffic to both deployments based on labels and selectors. By adjusting the number of replicas and monitoring the canary release, a full rollout can be performed with zero downtime.

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
