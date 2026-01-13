# Lab 59: ArgoCD: Shift-Left Reliability with Rollbacks

![Difficulty: Medium](https://img.shields.io/badge/Difficulty-Medium-yellow) ![ArgoCD](https://img.shields.io/badge/ArgoCD-EF7B4D?logo=argo&logoColor=white)

> **Auto-generated lab** - Created on 2026-01-13

## Description

This lab explores ArgoCD's rollback capabilities to address 'Shift-Left Reliability' by enabling quick recovery from faulty deployments. We'll simulate a broken deployment and use ArgoCD to revert to a previous, stable state, minimizing downtime.

## Learning Objectives

- Install and configure ArgoCD on a local Kubernetes cluster.
- Deploy an application using ArgoCD and GitOps principles.
- Simulate a faulty deployment and trigger a rollback using ArgoCD.
- Understand ArgoCD's rollback strategies and configuration options.

## Prerequisites

- kubectl installed and configured to connect to a Kubernetes cluster (minikube, Docker Desktop).
- helm installed.
- ArgoCD CLI installed (https://argo-cd.readthedocs.io/en/stable/cli_installation/)
- Git installed.
- Basic understanding of Kubernetes deployments and services.

## Lab Steps

### Step 1: Set up a Kubernetes Cluster and Install ArgoCD

First, ensure your Kubernetes cluster is running. If using minikube, start it with `minikube start`. Then, create a namespace for ArgoCD and install it using Helm:

```bash
kubectl create namespace argocd
helm repo add argo https://argoproj.github.io/argo-helm
helm install argocd argo/argo-cd -n argocd --version 5.51.2
```

Wait for all ArgoCD pods to be running. You can check the status with:

```bash
kubectl get pods -n argocd
```

Retrieve the initial admin password:

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d && echo
```

Finally, access the ArgoCD UI by port-forwarding the service:

```bash
kubectl port-forward svc/argo-cd-argocd-server -n argocd 8080:443
```

Open your browser and navigate to `https://localhost:8080`. Log in with the username `admin` and the password you retrieved earlier.  You may need to bypass a security warning from your browser due to the self-signed certificate.

### Step 2: Create a Sample Application Repository

Create a new Git repository (e.g., on GitHub) to store your application manifests. This repository will be the source of truth for ArgoCD. Create the following directory structure:

```
my-app/
├── base/
│   ├── deployment.yaml
│   └── service.yaml
└── overlays/
    └── production/
        └── kustomization.yaml
```

Create the following files with the specified content:

`base/deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  selector:
    matchLabels:
      app: my-app
  replicas: 2
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: nginx:1.23
        ports:
        - containerPort: 80
```

`base/service.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app
spec:
  selector:
    app: my-app
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
  type: LoadBalancer
```

`overlays/production/kustomization.yaml`:

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
- ../../base
```

Initialize a Git repository, commit the files, and push them to your remote repository:

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your_repository_url>
git push -u origin main
```

Ensure you have Kustomize installed to manage your manifests. If not, follow the installation instructions for your operating system.

### Step 3: Create an ArgoCD Application

In the ArgoCD UI, click the `+ NEW APP` button. Configure the application as follows:

*   **Application Name:** `my-app`
*   **Project:** `default`
*   **Sync Policy:** `Automatic` (Enable `Self Heal` and `Allow Empty`)
*   **Repository URL:** `<your_repository_url>`
*   **Revision:** `HEAD`
*   **Path:** `overlays/production`
*   **Cluster URL:** `https://kubernetes.default.svc`
*   **Namespace:** `default`

Click `CREATE`. ArgoCD will now deploy your application.  Wait for the application to be in a `Synced` and `Healthy` state.

### Step 4: Simulate a Faulty Deployment

Edit the `base/deployment.yaml` in your Git repository to simulate a faulty deployment. Change the image version to a non-existent one:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  selector:
    matchLabels:
      app: my-app
  replicas: 2
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: nginx:invalid-version
        ports:
        - containerPort: 80
```

Commit and push the changes to your Git repository:

```bash
git commit -am "Introduce faulty deployment"
git push origin main
```

ArgoCD will automatically detect the change and attempt to deploy the new version. This will result in a failed deployment.

### Step 5: Rollback to the Previous Version

In the ArgoCD UI, navigate to your `my-app` application. You will see that the deployment is in an `OutOfSync` state and likely unhealthy.

Click the `History and Rollback` button. You will see a list of previous deployments. Select the last successful deployment and click `ROLLBACK TO THIS`.  ArgoCD will now revert to the previous, stable version of your application.

Verify that the deployment is back in a `Synced` and `Healthy` state.  You can check the pod status using `kubectl get pods` and ensure that the pods are running with the correct image version.

### Step 6: Explore Rollback Strategies and Sync Options

ArgoCD offers various rollback strategies and sync options. Explore the following:

*   **Sync Policies:** Experiment with different sync policies (e.g., `Manual` sync with `Prune` disabled) to understand their impact on rollbacks.
*   **Rollback Strategies:**  ArgoCD automatically uses `apply` for rollbacks. For more complex scenarios, consider using pre- and post-sync hooks to manage database migrations or other stateful operations during rollbacks.
*   **Health Checks:**  Ensure that your Kubernetes resources have proper health checks defined (e.g., liveness and readiness probes) so that ArgoCD can accurately detect failed deployments and trigger rollbacks.

Consider adding annotations to your manifests to define custom health checks or rollback behavior.


<details>
<summary> Hints (click to expand)</summary>

1. Ensure your Kubernetes cluster has enough resources before installing ArgoCD.
2. Double-check the repository URL and path in the ArgoCD application settings.
3. If the rollback fails, examine the ArgoCD logs and Kubernetes events for clues.
4. Make sure the ArgoCD application is in sync with your git repository.

</details>


<details>
<summary>✅ Solution Notes (spoiler)</summary>

The solution involves setting up ArgoCD, deploying an application from a Git repository, simulating a failed deployment by introducing an invalid image version, and then using ArgoCD's rollback feature to revert to the last known good deployment. The key is understanding how ArgoCD tracks deployment history and provides a simple mechanism for reverting to previous states.

</details>


---

## Notes

- **Difficulty:** Medium
- **Estimated time:** 45-75 minutes
- **Technology:** Argocd

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
