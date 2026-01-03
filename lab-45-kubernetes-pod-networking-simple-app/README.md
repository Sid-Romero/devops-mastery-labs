# Lab 45: Kubernetes Pod Networking: Connecting to a Simple App

![Difficulty: Easy](https://img.shields.io/badge/Difficulty-Easy-brightgreen) ![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?logo=kubernetes&logoColor=white)

> **Auto-generated lab** - Created on 2026-01-03

## Description

This lab guides you through deploying a simple web application to Kubernetes and exposing it within the cluster. You will learn how to create a Pod, expose it with a Service, and access it from another Pod in the same cluster.

## Learning Objectives

- Deploy a simple web application as a Pod in Kubernetes.
- Create a Service to expose the Pod within the cluster.
- Access the deployed application from another Pod using the Service's cluster IP.

## Prerequisites

- kubectl installed and configured to connect to a Kubernetes cluster (e.g., minikube, Docker Desktop with Kubernetes enabled)
- Docker installed (for building the image if needed)
- Basic understanding of Kubernetes Pods and Services

## Lab Steps

### Step 1: Create a Simple Web Application

First, let's create a simple web application. We'll use Python with Flask for this example. Create a file named `app.py`:

```python
from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return f'Hello from {os.getenv("POD_NAME", "Unknown")}!'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

This application serves a simple greeting and includes the pod name, if the `POD_NAME` environment variable is set. This will be useful for identifying which pod is serving the request.

Next, create a `requirements.txt` file to specify the dependencies:

```
Flask
```

### Step 2: Create a Dockerfile

Now, let's create a Dockerfile to containerize our application:

```dockerfile
FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py ./

EXPOSE 5000

CMD ["python", "app.py"]
```
Build the Docker image. Replace `your-dockerhub-username` with your Docker Hub username or any other registry you prefer:

```bash
docker build -t your-dockerhub-username/simple-web-app:latest .
docker push your-dockerhub-username/simple-web-app:latest
```

If you are using minikube, you can build the docker image directly into minikube:
```bash
eval $(minikube docker-env)
docker build -t simple-web-app:latest .
```
In this case, you don't need to push the image to a registry.  You can use `image: simple-web-app:latest` in your pod definition.


### Step 3: Create a Kubernetes Pod Definition

Create a file named `pod.yaml` with the following content. Replace `your-dockerhub-username/simple-web-app:latest` with the image you built in the previous step:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: simple-web-app-pod
  labels:
    app: web-app
spec:
  containers:
  - name: web-app
    image: your-dockerhub-username/simple-web-app:latest
    ports:
    - containerPort: 5000
    env:
    - name: POD_NAME
      valueFrom:
        fieldRef:
          fieldPath: metadata.name
```

This defines a Pod named `simple-web-app-pod` that runs the Docker image we built.  The `POD_NAME` environment variable is set to the pod's name.

Apply the pod definition:

```bash
kubectl apply -f pod.yaml
```

Verify that the pod is running:

```bash
kubectl get pods
```

### Step 4: Create a Kubernetes Service

Now, let's create a Service to expose the Pod within the cluster. Create a file named `service.yaml` with the following content:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: simple-web-app-service
spec:
  selector:
    app: web-app
  ports:
  - protocol: TCP
    port: 80
    targetPort: 5000
  type: ClusterIP
```

This defines a Service named `simple-web-app-service` that selects Pods with the label `app: web-app` and forwards traffic on port 80 to port 5000 on the selected Pods.

Apply the service definition:

```bash
kubectl apply -f service.yaml
```

Verify that the service is created:

```bash
kubectl get services
```

Note the `CLUSTER-IP` assigned to the service. We'll use this to access the application from another Pod.

### Step 5: Create a Client Pod to Access the Application

Finally, let's create a Pod that we can use to access the application through the Service. Create a file named `client-pod.yaml` with the following content:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: client-pod
spec:
  containers:
  - name: client
    image: curlimages/curl:latest
    command: ["sleep", "3600"]
```

This defines a Pod named `client-pod` that runs the `curlimages/curl` image and simply sleeps for an hour.  We'll use `kubectl exec` to run `curl` inside this Pod.

Apply the client pod definition:

```bash
kubectl apply -f client-pod.yaml
```

Verify that the client pod is running:

```bash
kubectl get pods
```

Now, execute `curl` inside the `client-pod` to access the application through the Service. Replace `<CLUSTER-IP>` with the Cluster IP address of your `simple-web-app-service`:

```bash
kubectl exec -it client-pod -- curl simple-web-app-service:80
```

You should see the greeting from the web application, including the name of the Pod serving the request. This confirms that the Service is correctly routing traffic to the Pod.

Cleanup (optional):
```bash
kubectl delete -f pod.yaml
kubectl delete -f service.yaml
kubectl delete -f client-pod.yaml
```


<details>
<summary> Hints (click to expand)</summary>

1. Ensure the Docker image is pushed to a registry that your Kubernetes cluster can access, or build the image directly into minikube.
2. Double-check the selector in the Service definition matches the labels of your Pod.
3. Verify the Cluster IP of the service before attempting to access it from the client pod.

</details>


<details>
<summary>✅ Solution Notes (spoiler)</summary>

The solution involves creating a simple web application, containerizing it with Docker, deploying it as a Kubernetes Pod, exposing it with a Service, and then accessing it from another Pod using the Service's Cluster IP. This demonstrates basic Kubernetes networking concepts.

</details>


---

## Notes

- **Difficulty:** Easy
- **Estimated time:** 30-45 minutes
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
