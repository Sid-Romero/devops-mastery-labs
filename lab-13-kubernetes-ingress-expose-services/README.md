# Lab 13: Kubernetes: Exposing Services with Ingress

![Difficulty: Medium](https://img.shields.io/badge/Difficulty-Medium-yellow) ![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?logo=kubernetes&logoColor=white)

> **Auto-generated lab** - Created on 2025-12-28

## Description

This lab demonstrates how to expose multiple services running within a Kubernetes cluster to the outside world using an Ingress controller.  You will deploy a simple application with two services and configure an Ingress resource to route traffic to them based on hostnames.

## Learning Objectives

- Understand the purpose of Kubernetes Ingress.
- Deploy an Nginx Ingress controller.
- Define Ingress resources to route traffic to multiple services.
- Test the exposed services using hostnames.

## Prerequisites

- kubectl installed and configured to connect to a Kubernetes cluster (minikube, Docker Desktop, or a cloud provider)
- Basic understanding of Kubernetes deployments and services
- A tool like `curl` or `httpie` to make HTTP requests.

## Lab Steps

### Step 1: Step 1: Deploy Sample Applications (user-service and order-service)

First, we'll deploy two simple applications, `user-service` and `order-service`, as Kubernetes Deployments and Services. These services will simply return a JSON response indicating their name. Create the following deployment and service definitions in separate YAML files (e.g., `user-service.yaml` and `order-service.yaml`).

**user-service.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-service
spec:
  selector:
    matchLabels:
      app: user-service
  replicas: 1
  template:
    metadata:
      labels:
        app: user-service
    spec:
      containers:
      - name: user-service
        image: nginx:latest
        ports:
        - containerPort: 80
        command: ["/bin/sh", "-c"]
        args: ["echo '<h1>User Service</h1>' > /usr/share/nginx/html/index.html && nginx -g 'daemon off;'"]
---
apiVersion: v1
kind: Service
metadata:
  name: user-service
spec:
  selector:
    app: user-service
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
  type: ClusterIP
```

**order-service.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
spec:
  selector:
    matchLabels:
      app: order-service
  replicas: 1
  template:
    metadata:
      labels:
        app: order-service
    spec:
      containers:
      - name: order-service
        image: nginx:latest
        ports:
        - containerPort: 80
        command: ["/bin/sh", "-c"]
        args: ["echo '<h1>Order Service</h1>' > /usr/share/nginx/html/index.html && nginx -g 'daemon off;'"]
---
apiVersion: v1
kind: Service
metadata:
  name: order-service
spec:
  selector:
    app: order-service
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
  type: ClusterIP
```

Apply these configurations:
```bash
kubectl apply -f user-service.yaml
kubectl apply -f order-service.yaml
```

Verify that the deployments and services are running:
```bash
kubectl get deployments
kubectl get services
```

### Step 2: Step 2: Deploy the Nginx Ingress Controller

To expose our services, we'll deploy an Ingress controller.  For this lab, we'll use the Nginx Ingress controller.  The installation process varies slightly depending on your Kubernetes environment.  Here's how to install it on Minikube:

```bash
minikube addons enable ingress
```

If you are using Docker Desktop, you can install the Ingress controller using Helm. First, add the ingress-nginx repository:

```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
```

Then, install the Ingress controller:

```bash
helm install my-ingress ingress-nginx/ingress-nginx
```

For other Kubernetes environments (EKS, GKE, AKS), refer to the official Nginx Ingress controller documentation for installation instructions: [https://kubernetes.github.io/ingress-nginx/deploy/](https://kubernetes.github.io/ingress-nginx/deploy/)

Verify that the Ingress controller is running. Look for a pod in the `ingress-nginx` namespace (or the namespace you deployed it to):

```bash
kubectl get pods -n ingress-nginx
```

If you are using Minikube, get the Ingress IP:
```bash
minikube ip
```
If you are using Docker Desktop, use `localhost` as the Ingress IP.

### Step 3: Step 3: Configure DNS (or /etc/hosts)

Since we're using host-based routing, we need to configure DNS (or your `/etc/hosts` file) to resolve the hostnames to the Ingress controller's IP address.  Add the following lines to your `/etc/hosts` file (replace `<INGRESS_IP>` with the IP address obtained in the previous step):

```
<INGRESS_IP> user.example.com
<INGRESS_IP> order.example.com
```

If you have a real DNS server, create A records for `user.example.com` and `order.example.com` pointing to the Ingress controller's IP address. For testing purposes using nip.io is also a valid alternative. (e.g., `<INGRESS_IP>.nip.io`)

### Step 4: Step 4: Define the Ingress Resource

Now, we'll create an Ingress resource that routes traffic to our services based on the hostname. Create a file named `ingress.yaml` with the following content:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: example-ingress
spec:
  rules:
  - host: user.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: user-service
            port:
              number: 80
  - host: order.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: order-service
            port:
              number: 80
```

Apply the Ingress resource:

```bash
kubectl apply -f ingress.yaml
```

Verify that the Ingress resource is created:

```bash
kubectl get ingress
```

### Step 5: Step 5: Test the Services

Now, you can test the services by sending HTTP requests to the configured hostnames. Use `curl` or `httpie`:

```bash
curl http://user.example.com
curl http://order.example.com
```

You should see the `User Service` and `Order Service` HTML output from each service, respectively. If you are using nip.io, replace `user.example.com` and `order.example.com` with `<INGRESS_IP>.nip.io`.

If you encounter issues, check the Ingress controller logs:

```bash
kubectl logs -n ingress-nginx <ingress-controller-pod-name>
```


<details>
<summary> Hints (click to expand)</summary>

1. Ensure the Ingress controller is properly installed and running before creating the Ingress resource.
2. Double-check the service names and ports in the Ingress resource to match the services you deployed.
3. Verify your /etc/hosts file is correctly configured to point the hostnames to the Ingress controller's IP address.
4. If you are using Minikube, make sure the Ingress addon is enabled (`minikube addons enable ingress`).
5. If you are using Docker Desktop, make sure the Ingress controller is deployed and running.

</details>


<details>
<summary>✅ Solution Notes (spoiler)</summary>

The complete solution involves deploying two basic services, installing an Nginx Ingress controller, configuring DNS (or /etc/hosts) to resolve the hostnames to the Ingress controller's IP address, and defining an Ingress resource that routes traffic to the correct services based on the hostname. The key is ensuring that the Ingress controller is correctly installed and configured for your Kubernetes environment and that the service names and ports in the Ingress resource match the actual services.

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
