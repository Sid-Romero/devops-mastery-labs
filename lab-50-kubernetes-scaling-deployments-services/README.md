# Lab 50: Kubernetes: Scaling with Deployments and Services

![Difficulty: Medium](https://img.shields.io/badge/Difficulty-Medium-yellow) ![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?logo=kubernetes&logoColor=white)

> **Auto-generated lab** - Created on 2026-01-04

## Description

This lab demonstrates how to scale applications in Kubernetes using Deployments and Services. You'll learn how to create a Deployment, expose it with a Service, and scale the Deployment to handle increased traffic.

## Learning Objectives

- Create a Kubernetes Deployment
- Expose a Deployment using a Service
- Scale a Deployment
- Test the scaled application

## Prerequisites

- kubectl installed and configured to connect to a Kubernetes cluster (minikube, Docker Desktop, or cloud provider)
- Basic understanding of Kubernetes concepts (Pods, Deployments, Services)

## Lab Steps

### Step 1: Create a Simple Application

First, let's create a simple web application using Python and Flask. Create a file named `app.py` with the following content:

```python
from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    hostname = os.environ.get('HOSTNAME', 'unknown')
    return f'Hello from Pod: {hostname}\n'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

This application simply returns 'Hello from Pod: <hostname>' when accessed. Next, create a `requirements.txt` file:

```
Flask
```

Finally, create a Dockerfile to containerize the application:

```dockerfile
FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py ./

EXPOSE 8080

CMD ["python", "app.py"]
```

Build the Docker image:

```bash
docker build -t my-app:v1 .
```

Push the image to a container registry (Docker Hub, etc.). Replace `<your-dockerhub-username>` with your actual username:

```bash
docker tag my-app:v1 <your-dockerhub-username>/my-app:v1
docker push <your-dockerhub-username>/my-app:v1
```

### Step 2: Create a Kubernetes Deployment

Now, let's create a Kubernetes Deployment to manage our application. Create a file named `deployment.yaml` with the following content. Replace `<your-dockerhub-username>` with your Docker Hub username:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-deployment
spec:
  replicas: 2
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
        image: <your-dockerhub-username>/my-app:v1
        ports:
        - containerPort: 8080
```

Apply the Deployment:

```bash
kubectl apply -f deployment.yaml
```

Verify that the Deployment is running:

```bash
kubectl get deployments
kubectl get pods
```

### Step 3: Create a Kubernetes Service

To expose our application, we need to create a Kubernetes Service. Create a file named `service.yaml` with the following content:

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
    targetPort: 8080
  type: LoadBalancer
```

Apply the Service:

```bash
kubectl apply -f service.yaml
```

Verify that the Service is running:

```bash
kubectl get services
```

Note the `EXTERNAL-IP` assigned to the Service. It may take a few minutes for the `EXTERNAL-IP` to be assigned, especially in minikube or Docker Desktop. If you are using minikube, you can use the `minikube service my-app-service` command to open the service in your browser. If you are using Docker Desktop, the service will be exposed on localhost.

Access the application using the `EXTERNAL-IP` and port 80 in your browser or using `curl`.

### Step 4: Scale the Deployment

Now, let's scale the Deployment to increase the number of replicas. Scale the Deployment to 5 replicas:

```bash
kubectl scale deployment my-app-deployment --replicas=5
```

Verify that the Deployment has been scaled:

```bash
kubectl get deployments
kubectl get pods
```

Access the application again using the Service's `EXTERNAL-IP`. You should see the hostname change as the requests are distributed across the different Pods. You can test this by repeatedly refreshing the page or using `curl` in a loop.

```bash
while true; do curl <EXTERNAL-IP>; sleep 1; done
```

Replace `<EXTERNAL-IP>` with the actual external IP of your service. You should observe the hostname changing in the output, confirming that requests are being distributed across the scaled pods.


<details>
<summary> Hints (click to expand)</summary>

1. Make sure the Docker image is pushed to a public or private registry that your Kubernetes cluster can access.
2. Double-check the image name and tag in the `deployment.yaml` file.
3. If the `EXTERNAL-IP` for the Service remains in a `<pending>` state, it might indicate an issue with your Kubernetes cluster's load balancer implementation (especially in minikube or Docker Desktop).  Try `minikube tunnel` if using minikube.
4. Use `kubectl describe pod <pod-name>` to troubleshoot pod creation issues.

</details>


<details>
<summary>✅ Solution Notes (spoiler)</summary>

The solution involves creating a simple Python application, containerizing it with Docker, deploying it to Kubernetes using a Deployment, exposing it with a Service, and then scaling the Deployment to increase the number of replicas. The key is understanding how Deployments manage Pods and how Services provide a stable endpoint for accessing the application, even as Pods are created or destroyed.

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
