# Lab 24: Kubernetes: Deconstructing a Monolith into Microservices

![Difficulty: Medium](https://img.shields.io/badge/Difficulty-Medium-yellow) ![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?logo=kubernetes&logoColor=white)

> **Auto-generated lab** - Created on 2025-12-30

## Description

This lab simulates the process of breaking down a monolithic application into microservices and deploying them on Kubernetes. It highlights the complexity introduced by Kubernetes while demonstrating its benefits for managing distributed applications.

## Learning Objectives

- Understand the basics of deploying applications on Kubernetes.
- Decompose a monolithic application into smaller microservices.
- Configure Kubernetes deployments and services for microservices.
- Explore the added complexity of managing microservices with Kubernetes.

## Prerequisites

- Docker installed and running
- kubectl installed and configured to connect to a Kubernetes cluster (e.g., minikube, Docker Desktop)
- Basic understanding of Docker and Kubernetes concepts

## Lab Steps

### Step 1: Set up the Monolithic Application

First, we'll create a simple monolithic application using Docker. This application will simulate a basic e-commerce platform.

Create a directory for the project:

```bash
mkdir monolith-app
cd monolith-app
```

Create a file named `app.py` with the following content:

```python
from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Welcome to the Monolithic E-commerce Platform!\n'

@app.route('/products')
def products():
    return 'List of Products: Product A, Product B, Product C\n'

@app.route('/orders')
def orders():
    return 'List of Orders: Order 1, Order 2, Order 3\n'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
```

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim-buster

WORKDIR /app

COPY . .

RUN pip install flask

ENV PORT=5000

EXPOSE 5000

CMD ["python", "app.py"]
```

Build the Docker image:

```bash
docker build -t monolith-app .
```

Run the Docker container locally to test:

```bash
docker run -d -p 5000:5000 monolith-app
```

Verify the application is running by accessing `http://localhost:5000`, `http://localhost:5000/products`, and `http://localhost:5000/orders` in your browser.

### Step 2: Deploy the Monolith to Kubernetes

Now, let's deploy the monolithic application to Kubernetes. Create a `monolith-deployment.yaml` file:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: monolith-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: monolith-app
  template:
    metadata:
      labels:
        app: monolith-app
    spec:
      containers:
      - name: monolith-app
        image: monolith-app
        ports:
        - containerPort: 5000
```

Create a `monolith-service.yaml` file:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: monolith-service
spec:
  selector:
    app: monolith-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
  type: LoadBalancer
```

Apply the Kubernetes manifests:

```bash
kubectl apply -f monolith-deployment.yaml
kubectl apply -f monolith-service.yaml
```

Check the status of the deployment and service:

```bash
kubectl get deployments
kubectl get services
```

Access the application through the LoadBalancer's external IP address (may take a few minutes to provision).

`minikube service monolith-service` will open the service in your browser if you are using minikube.


### Step 3: Decompose the Monolith into Microservices

Next, we'll break down the monolithic application into three separate microservices: `web`, `products`, and `orders`.

Create directories for each microservice:

```bash
mkdir web-service
mkdir products-service
mkdir orders-service
```

**web-service:**

Create `web-service/app.py`:

```python
from flask import Flask
import os
import requests

app = Flask(__name__)

PRODUCTS_URL = os.environ.get('PRODUCTS_URL', 'http://localhost:5001')
ORDERS_URL = os.environ.get('ORDERS_URL', 'http://localhost:5002')

@app.route('/')
def hello():
    return 'Welcome to the E-commerce Platform!\n'

@app.route('/products')
def products():
    response = requests.get(PRODUCTS_URL)
    return response.text

@app.route('/orders')
def orders():
    response = requests.get(ORDERS_URL)
    return response.text

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
```

Create `web-service/Dockerfile`:

```dockerfile
FROM python:3.9-slim-buster

WORKDIR /app

COPY . .

RUN pip install flask requests

ENV PORT=5000

EXPOSE 5000

CMD ["python", "app.py"]
```

**products-service:**

Create `products-service/app.py`:

```python
from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def products():
    return 'List of Products: Product A, Product B, Product C\n'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5001)))
```

Create `products-service/Dockerfile`:

```dockerfile
FROM python:3.9-slim-buster

WORKDIR /app

COPY . .

RUN pip install flask

ENV PORT=5001

EXPOSE 5001

CMD ["python", "app.py"]
```

**orders-service:**

Create `orders-service/app.py`:

```python
from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def orders():
    return 'List of Orders: Order 1, Order 2, Order 3\n'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5002)))
```

Create `orders-service/Dockerfile`:

```dockerfile
FROM python:3.9-slim-buster

WORKDIR /app

COPY . .

RUN pip install flask

ENV PORT=5002

EXPOSE 5002

CMD ["python", "app.py"]
```

Build the Docker images:

```bash
docker build -t web-service web-service/.
docker build -t products-service products-service/.
docker build -t orders-service orders-service/.
```

### Step 4: Deploy the Microservices to Kubernetes

Now, let's deploy the microservices to Kubernetes.  You will need to create deployment and service files for each microservice. Pay attention to the environment variables for service discovery.

Create `web-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: web-service
  template:
    metadata:
      labels:
        app: web-service
    spec:
      containers:
      - name: web-service
        image: web-service
        ports:
        - containerPort: 5000
        env:
        - name: PRODUCTS_URL
          value: http://products-service:5001
        - name: ORDERS_URL
          value: http://orders-service:5002
```

Create `web-service.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  selector:
    app: web-service
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
  type: LoadBalancer
```

Create `products-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: products-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: products-service
  template:
    metadata:
      labels:
        app: products-service
    spec:
      containers:
      - name: products-service
        image: products-service
        ports:
        - containerPort: 5001
```

Create `products-service.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: products-service
spec:
  selector:
    app: products-service
  ports:
    - protocol: TCP
      port: 5001
      targetPort: 5001
```

Create `orders-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: orders-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: orders-service
  template:
    metadata:
      labels:
        app: orders-service
    spec:
      containers:
      - name: orders-service
        image: orders-service
        ports:
        - containerPort: 5002
```

Create `orders-service.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: orders-service
spec:
  selector:
    app: orders-service
  ports:
    - protocol: TCP
      port: 5002
      targetPort: 5002
```

Apply the Kubernetes manifests:

```bash
kubectl apply -f web-deployment.yaml
kubectl apply -f web-service.yaml
kubectl apply -f products-deployment.yaml
kubectl apply -f products-service.yaml
kubectl apply -f orders-deployment.yaml
kubectl apply -f orders-service.yaml
```

Check the status of the deployments and services:

```bash
kubectl get deployments
kubectl get services
```

Access the application through the `web-service` LoadBalancer's external IP address.  `minikube service web-service` will open the service in your browser if you are using minikube.


### Step 5: Observe the Complexity

Consider the following:

*   The monolithic application was simpler to deploy and manage initially.
*   The microservice architecture introduces complexity in terms of service discovery, networking, and deployment.
*   Kubernetes provides the tools to manage this complexity, but it also adds its own overhead.
*   Debugging and tracing issues across multiple services can be more challenging.

This lab aims to provide a practical understanding of the trade-offs involved in adopting a microservices architecture with Kubernetes.  Consider the steps you would take to update a single product detail in this architecture. What would happen if the orders service crashed? How would you monitor the health of each service?  What happens to the web service if the product service becomes unavailable? These are all considerations that must be addressed when moving to a microservice architecture.


<details>
<summary> Hints (click to expand)</summary>

1. Ensure the Docker images are built correctly and tagged appropriately.
2. Verify that the Kubernetes deployments and services are created without errors.
3. Double-check the service names and ports in the environment variables.
4. Use `kubectl logs <pod-name>` to troubleshoot issues within the pods.

</details>


<details>
<summary>✅ Solution Notes (spoiler)</summary>

The solution involves creating a basic monolithic application, deploying it to Kubernetes, then breaking it down into microservices and deploying those to Kubernetes. The key is understanding the service discovery mechanism using Kubernetes services and environment variables. This lab demonstrates the added complexity of managing microservices in a Kubernetes environment compared to a monolithic application.

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
