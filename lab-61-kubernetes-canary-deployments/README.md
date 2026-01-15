# Lab 61: Kubernetes: Canary Deployments for App Updates

![Difficulty: Medium](https://img.shields.io/badge/Difficulty-Medium-yellow) ![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?logo=kubernetes&logoColor=white)

> **Auto-generated lab** - Created on 2026-01-15

## Description

This lab demonstrates how to perform canary deployments in Kubernetes. You'll deploy a sample application, then gradually roll out a new version using deployments and services, minimizing risk during updates.

## Learning Objectives

- Understand the concept of canary deployments.
- Create and manage Kubernetes deployments.
- Utilize Kubernetes services for traffic routing.
- Implement a canary deployment strategy.

## Prerequisites

- kubectl installed and configured to connect to a Kubernetes cluster (minikube, Docker Desktop, or a cloud provider cluster)
- Basic understanding of Kubernetes deployments and services

## Lab Steps

### Step 1: Deploy the Initial Application Version

First, we'll deploy the initial version of our application. Create a file named `app.yaml` with the following content:

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
        image: nginx:1.21 # Replace with your app image
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
  type: LoadBalancer # Change to NodePort if LoadBalancer is not supported
```

Apply this configuration:

```bash
kubectl apply -f app.yaml
```

Verify the deployment and service are running:

```bash
kubectl get deployments
kubectl get services
```

Access the application via the service's external IP or NodePort. If using minikube, you can use `minikube service my-app-service` to get the URL.

### Step 2: Deploy the Canary Version

Now, we'll deploy the canary version of our application. Create a new deployment file named `app-canary.yaml` with the following content:

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
        image: nginx:latest # Replace with your canary image. Use a different image than the original deployment.
        ports:
        - containerPort: 80
```

Apply this configuration:

```bash
kubectl apply -f app-canary.yaml
```

Verify the canary deployment is running:

```bash
kubectl get deployments
```

### Step 3: Update the Service to Route Traffic to the Canary

To route a small percentage of traffic to the canary deployment, we'll modify the service to select pods with both `version: v1` and `version: v2`. Update the `app.yaml` file (specifically the service part) to include the `version` label in the selector.  Remove the `version` label from the selector initially. Then, edit the service and add the `version` label to the selector. This will initially route all traffic to the `v1` deployment.

After observing the `v1` deployment, modify the service to include the `version` label in the selector. This will distribute the traffic between the `v1` and `v2` deployments.

First, remove the `version` label from the service selector in `app.yaml`:

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

Apply the updated `app.yaml`:

```bash
kubectl apply -f app.yaml
```

Now, edit the service directly using `kubectl edit service my-app-service` and add the `version` label to the selector:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  selector:
    app: my-app
    version: v1 # Add this line initially
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
  type: LoadBalancer
```

After confirming the v1 deployment is working correctly, modify the service to include both v1 and v2 versions.  Remove the `version: v1` line and don't add `version: v2`.  The `app: my-app` selector will now match both deployments.

Observe the traffic distribution. You can scale up the canary deployment (`kubectl scale deployment my-app-canary --replicas=2`) to increase the percentage of traffic it receives.

### Step 4: Analyze and Promote or Rollback

Monitor the canary deployment for errors, performance issues, or other anomalies. You can use Kubernetes dashboard, Prometheus, or other monitoring tools.  If the canary performs well, you can promote it by scaling down the original deployment and scaling up the canary deployment.  If issues are detected, scale down the canary deployment and investigate the problems.  To promote, scale down the original deployment to 0 and scale up the canary deployment to the desired number of replicas:

```bash
kubectl scale deployment my-app --replicas=0
kubectl scale deployment my-app-canary --replicas=3
```

If you need to rollback, simply scale down the canary deployment to 0:

```bash
kubectl scale deployment my-app-canary --replicas=0
```

Optionally, you can update the original deployment with the changes from the canary and re-deploy it.


<details>
<summary> Hints (click to expand)</summary>

1. Ensure your image names are correct in the deployment files.
2. If your service is not exposing an external IP, try changing the service type to NodePort.
3. Carefully observe the output of `kubectl get pods` to understand which pods are serving traffic.

</details>


<details>
<summary>✅ Solution Notes (spoiler)</summary>

The solution involves deploying two deployments: the stable version and the canary version. The service is configured to initially route all traffic to the stable version. Then, the service is modified to route a percentage of traffic to the canary version. Finally, based on the analysis of the canary deployment, it is either promoted or rolled back.

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
