# Lab 51: ArgoCD: GitOps Deployment to NeoCities

![Difficulty: Medium](https://img.shields.io/badge/Difficulty-Medium-yellow) ![ArgoCD](https://img.shields.io/badge/ArgoCD-EF7B4D?logo=argo&logoColor=white)

> **Auto-generated lab** - Created on 2026-01-05

## Description

This lab demonstrates how to use ArgoCD to deploy a static website (inspired by Eleventy and NeoCities) using GitOps principles. It covers setting up ArgoCD, configuring an application to sync with a Git repository, and automatically deploying changes to a local directory simulating a NeoCities deployment.

## Learning Objectives

- Install and configure ArgoCD locally.
- Create an ArgoCD application that syncs with a Git repository.
- Simulate NeoCities deployment by syncing to a local directory.
- Understand ArgoCD's GitOps workflow.

## Prerequisites

- kubectl installed and configured.
- A local Kubernetes cluster (e.g., minikube, Docker Desktop).
- Git installed.
- Basic understanding of Kubernetes and GitOps.

## Lab Steps

### Step 1: Install ArgoCD

First, create a namespace for ArgoCD:

```bash
kubectl create namespace argocd
```

Then, apply the ArgoCD installation manifest:

```bash
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

Verify that all ArgoCD pods are running:

```bash
kubectl get pods -n argocd
```

It may take a few minutes for all pods to become ready.

### Step 2: Access the ArgoCD UI

To access the ArgoCD UI, you'll need to port-forward the ArgoCD server:

```bash
kubectl port-forward -n argocd svc/argo-cd-server 8080:443
```

Open your web browser and navigate to `https://localhost:8080`. You might need to accept a self-signed certificate warning.

The default username is `admin`. To retrieve the initial password, run:

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 -d
```

Log in to the ArgoCD UI using the username and password.

### Step 3: Create a Git Repository

Create a new directory for your Git repository and initialize it:

```bash
mkdir neocities-site
cd neocities-site
git init
```

Create a simple `index.html` file:

```bash
cat <<EOF > index.html
<!DOCTYPE html>
<html>
<head>
  <title>My NeoCities Site</title>
</head>
<body>
  <h1>Hello from ArgoCD and NeoCities!</h1>
  <p>This site is deployed using ArgoCD and simulates a NeoCities deployment.</p>
</body>
</html>
EOF
```

Add and commit the file:

```bash
git add .
git commit -m "Initial commit"
```

Create a remote repository on a Git hosting service like GitHub, GitLab, or Bitbucket.  Then, link your local repository to the remote repository:

```bash
git remote add origin <your_remote_repository_url>
git push -u origin main
```

Replace `<your_remote_repository_url>` with the actual URL of your remote repository.

### Step 4: Create a NeoCities Deployment Directory

Create a directory on your local machine to simulate the NeoCities deployment directory.  ArgoCD will sync the contents of your Git repository to this directory.

```bash
mkdir neocities-deploy
```

### Step 5: Create an ArgoCD Application

In the ArgoCD UI, click the `+ New App` button.

*   **Application Name:** `neocities-app`
*   **Project:** `default`
*   **Sync Policy:** `Automatic` (with `Prune` and `Self Heal` enabled)
*   **Repository URL:** `<your_remote_repository_url>` (the same as in step 3)
*   **Revision:** `HEAD`
*   **Path:** `.` (the root of the repository)
*   **Destination Namespace:** `default` (or any namespace you prefer)
*   **Destination Server:** `https://kubernetes.default.svc`
*   **Directory:** `neocities-deploy` (This is the crucial part.  ArgoCD will sync the repository contents to this directory on your local machine. This requires some extra configuration explained after these steps.)

Click `Create`.

**Important Note:** ArgoCD typically deploys *to* Kubernetes.  To deploy *to* a local directory, you'll need to configure ArgoCD to use a `kustomization.yaml` that uses the `kustomize filesystem` generator to write to the `neocities-deploy` directory. This is more advanced and requires creating a `kustomization.yaml` file in your repository with content similar to:

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources: []
generators:
- kustomize.config.k8s.io/v1/Filesystem
  files:
  - index.html
  target: neocities-deploy
```

Commit and push this `kustomization.yaml` to your repository.  Then, in the ArgoCD application settings, change the `Path` to the directory containing `kustomization.yaml` (e.g., `.`).  ArgoCD will now use Kustomize to generate files in the `neocities-deploy` directory.  Alternatively, a simpler (but less GitOps-like) approach is to create a simple pod that mounts the `neocities-deploy` directory as a volume and serves the static content. This lab focuses on the directory sync approach.

### Step 6: Verify the Deployment

After creating the application, ArgoCD will automatically start syncing.  In the ArgoCD UI, you should see the application status change to `Synced` and `Healthy`.

Check the contents of the `neocities-deploy` directory on your local machine.  It should now contain the `index.html` file from your Git repository:

```bash
ls neocities-deploy
cat neocities-deploy/index.html
```

If you make changes to the `index.html` file in your Git repository and push them, ArgoCD will automatically detect the changes and sync them to the `neocities-deploy` directory.


<details>
<summary> Hints (click to expand)</summary>

1. Ensure your ArgoCD pods are running before attempting to access the UI.
2. Double-check the Git repository URL and credentials if ArgoCD fails to sync.
3. Verify the `kustomization.yaml` syntax and that the target directory is correct.

</details>


<details>
<summary>✅ Solution Notes (spoiler)</summary>

The core of this lab lies in configuring ArgoCD to deploy to a local directory. This deviates from the typical Kubernetes-centric deployment and necessitates using a `kustomization.yaml` to generate files directly into the desired directory. Alternative solution involves using a pod to serve the static content deployed to the local directory, but the kustomize approach provides a more GitOps friendly solution.

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
