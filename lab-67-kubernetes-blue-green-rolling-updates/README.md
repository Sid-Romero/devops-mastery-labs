# Lab 67: Kubernetes: Blue-Green Deployments with Rolling Updates

![Difficulty: Medium](https://img.shields.io/badge/Difficulty-Medium-yellow) ![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?logo=kubernetes&logoColor=white)

> **Auto-generated lab** - Created on 2026-01-21

## Description

This lab demonstrates how to implement blue-green deployments in Kubernetes using rolling updates. You will deploy two versions of an application and seamlessly transition traffic between them using Kubernetes services.

## Learning Objectives

- Understand the concept of blue-green deployments.
- Learn how to perform rolling updates in Kubernetes.
- Manage application versions using Kubernetes deployments.
- Configure Kubernetes services for traffic routing.

## Prerequisites

- kubectl installed and configured to connect to a Kubernetes cluster (minikube, Docker Desktop, or a cloud provider cluster)
- Basic understanding of Kubernetes deployments and services.

## Lab Steps

### Step 1: Step 1: Create the Initial Application Deployment (Blue)

First, we'll create the initial 'blue' deployment of our application.  This deployment will serve the initial version of the application.  Create a file named `blue-deployment.yaml` with the following content:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: blue-app
  labels:
    app: my-app
    version: blue
spec:
  replicas: 2
  selector:
    matchLabels:
      app: my-app
      version: blue
  template:
    metadata:
      labels:
        app: my-app
        version: blue
    spec:
      containers:
      - name: my-app
        image: nginx:1.21 # You can replace this with your application image
        ports:
        - containerPort: 80
```

Apply the deployment using kubectl:

```bash
kubectl apply -f blue-deployment.yaml
```

Verify the deployment is running:

```bash
kubectl get deployments
```

### Step 2: Step 2: Create the 'Blue' Service

Now, we'll create a service to expose the 'blue' deployment. Create a file named `blue-service.yaml` with the following content:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  selector:
    app: my-app
    version: blue
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
  type: LoadBalancer # Use NodePort if LoadBalancer is not available
```

Apply the service:

```bash
kubectl apply -f blue-service.yaml
```

Get the service's external IP or NodePort:

```bash
kubectl get service my-app-service
```

Access the application in your browser using the obtained IP or NodePort.  You should see the default Nginx page (or your application if you replaced the image).

### Step 3: Step 3: Create the 'Green' Deployment

Next, we'll create the 'green' deployment, representing the new version of our application. Create a file named `green-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: green-app
  labels:
    app: my-app
    version: green
spec:
  replicas: 2
  selector:
    matchLabels:
      app: my-app
      version: green
  template:
    metadata:
      labels:
        app: my-app
        version: green
    spec:
      containers:
      - name: my-app
        image: nginx:1.23 # Use a different version of your application image
        ports:
        - containerPort: 80
```

Apply the 'green' deployment:

```bash
kubectl apply -f green-deployment.yaml
```

Verify the deployment is running:

```bash
kubectl get deployments
```

### Step 4: Step 4: Update the Service to Point to 'Green'

Now, we'll modify the service to point to the 'green' deployment.  Edit the `blue-service.yaml` file (or create a new one named `green-service.yaml` and apply it): 

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  selector:
    app: my-app
    version: green
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
  type: LoadBalancer # Use NodePort if LoadBalancer is not available
```

Apply the updated service definition:

```bash
kubectl apply -f blue-service.yaml # Or kubectl apply -f green-service.yaml if you created a new file
```

Now, when you access the application through the service's IP or NodePort, you should see the 'green' version of the application (Nginx 1.23 or your new application version).

### Step 5: Step 5: Rolling Update (Alternative to Direct Service Update)

Instead of directly modifying the service's selector, we can perform a rolling update. This is a more gradual and controlled way to transition traffic.

First, revert the service to point to the 'blue' deployment (if you changed it in the previous step).

Then, execute a rolling update on the 'blue' deployment to update the image to the 'green' version.  This can be achieved by patching the deployment:

```bash
kubectl set image deployment/blue-app my-app=nginx:1.23 # Replace nginx:1.23 with your new image
```

Monitor the rollout status:

```bash
kubectl rollout status deployment/blue-app
```

During the rolling update, Kubernetes will gradually replace the old pods with new pods running the 'green' version.  The service will continue to route traffic to the available pods, ensuring minimal downtime.

After the rolling update is complete, all pods in the 'blue-app' deployment will be running the 'green' version.

Finally, update the deployment's labels to reflect the 'green' version.  This step is important for future deployments:

```bash
kubectl label deployment blue-app version=green --overwrite
```

### Step 6: Step 6: Cleanup (Optional)

To clean up the resources created in this lab, you can delete the deployments and service:

```bash
kubectl delete deployment blue-app green-app
kubectl delete service my-app-service
```


<details>
<summary> Hints (click to expand)</summary>

1. Ensure the correct image name and tag are used in the deployment definitions.
2. Double-check the service selectors to ensure they match the deployment labels.
3. If using NodePort, make sure your firewall allows access to the exposed port.

</details>


<details>
<summary>✅ Solution Notes (spoiler)</summary>

The complete solution involves creating two deployments representing different versions of an application. A Kubernetes service is used to route traffic to one of the deployments. By updating the service's selector, traffic can be seamlessly switched between the 'blue' and 'green' deployments. Rolling updates provide an alternative, gradual transition strategy.

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
