# Lab 25: Kubernetes Core Components: A Hands-On Exploration

![Difficulty: Medium](https://img.shields.io/badge/Difficulty-Medium-yellow) ![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?logo=kubernetes&logoColor=white)

> **Auto-generated lab** - Created on 2025-12-30

## Description

This lab provides a hands-on experience with Kubernetes core components, focusing on understanding their interactions. You will deploy a simple application using Pods, Deployments, and Services, observing how these components work together to manage and expose your application.

## Learning Objectives

- Understand the purpose and functionality of Pods, Deployments, and Services.
- Learn how to create and manage these core components using `kubectl`.
- Observe how Deployments ensure desired state and perform rolling updates.
- Expose an application using a Service and access it.
- Gain practical experience with Kubernetes manifest files (YAML).

## Prerequisites

- kubectl installed and configured to connect to a Kubernetes cluster (minikube, Docker Desktop, or a cloud-based cluster)
- Basic understanding of containerization concepts (Docker)
- Text editor for creating and modifying YAML files

## Lab Steps

### Step 1: Step 1: Create a Pod

A Pod is the smallest deployable unit in Kubernetes. Create a file named `pod.yaml` with the following content:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-app-pod
  labels:
    app: my-app
spec:
  containers:
  - name: my-app-container
    image: nginx:latest
    ports:
    - containerPort: 80
```

Apply this configuration to your cluster:

```bash
kubectl apply -f pod.yaml
```

Verify that the Pod is running:

```bash
kubectl get pods
```

Describe the Pod to see its details:

```bash
kubectl describe pod my-app-pod
```

### Step 2: Step 2: Create a Deployment

Deployments manage Pods and ensure the desired number of replicas are running. Create a file named `deployment.yaml` with the following content:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-deployment
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
      - name: my-app-container
        image: nginx:latest
        ports:
        - containerPort: 80
```

Apply this configuration to your cluster:

```bash
kubectl apply -f deployment.yaml
```

Verify that the Deployment and its associated Pods are running:

```bash
kubectl get deployments
kubectl get pods
```

Scale the Deployment to 5 replicas:

```bash
kubectl scale deployment my-app-deployment --replicas=5
```

Verify the new number of Pods:

```bash
kubectl get pods
```

### Step 3: Step 3: Create a Service

Services provide a stable IP address and DNS name to access your application. Create a file named `service.yaml` with the following content:

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

Apply this configuration to your cluster:

```bash
kubectl apply -f service.yaml
```

Verify that the Service is running:

```bash
kubectl get services
```

Note the EXTERNAL-IP or NODEPORT assigned to your service. If using minikube, you can access the service using `minikube service my-app-service`.

Access the application in your browser using the obtained IP address or NodePort.

### Step 4: Step 4: Update the Deployment

Update the `deployment.yaml` file to use a different version of the nginx image, for example, `nginx:1.23`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-deployment
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
      - name: my-app-container
        image: nginx:1.23
        ports:
        - containerPort: 80
```

Apply the updated configuration:

```bash
kubectl apply -f deployment.yaml
```

Observe the rolling update process by watching the Pods being replaced:

```bash
kubectl get pods -w
```

Verify that the application is still accessible via the Service.

### Step 5: Step 5: Clean Up

Delete the Deployment, Service, and Pod:

```bash
kubectl delete deployment my-app-deployment
kubectl delete service my-app-service
kubectl delete pod my-app-pod
```

Verify that all resources have been deleted:

```bash
kubectl get deployments
kubectl get services
kubectl get pods
```


<details>
<summary> Hints (click to expand)</summary>

1. Make sure your `kubectl` is configured to point to your Kubernetes cluster.
2. Double-check the YAML syntax for any errors. Use a YAML validator if needed.
3. If the Service EXTERNAL-IP remains in `<pending>` state, it might be due to your cluster setup. Try using `type: NodePort` instead or use `minikube service <service-name>` if using minikube.
4. Ensure the labels in the Deployment's `selector` and the Pod's `metadata` match.

</details>


<details>
<summary>✅ Solution Notes (spoiler)</summary>

The lab demonstrates the core workflow of deploying an application on Kubernetes.  The key takeaway is understanding how Pods are the basic units, Deployments manage these Pods ensuring desired state, and Services expose the application to the outside world.  Updating the Deployment triggers a rolling update, showing Kubernetes' ability to handle updates without downtime. Remember to always clean up resources after finishing a lab.

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
