# Lab 56: Kubernetes: Biometric Data Handling Simulation

![Difficulty: Medium](https://img.shields.io/badge/Difficulty-Medium-yellow) ![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?logo=kubernetes&logoColor=white)

> **Auto-generated lab** - Created on 2026-01-10

## Description

This lab simulates a simplified biometric data handling system deployed on Kubernetes. It demonstrates how to manage sensitive data (simulated biometric data) using ConfigMaps and Secrets, and how to control access to this data within the cluster using Role-Based Access Control (RBAC).

## Learning Objectives

- Learn how to create and manage ConfigMaps and Secrets in Kubernetes.
- Understand how to use RBAC to control access to resources within a Kubernetes cluster.
- Deploy a simple application that simulates handling biometric data.
- Learn how to update a deployment with new configurations.

## Prerequisites

- kubectl installed and configured to connect to a Kubernetes cluster (minikube, Docker Desktop, or cloud provider).
- Basic understanding of Kubernetes concepts (Pods, Deployments, Services, ConfigMaps, Secrets, RBAC).

## Lab Steps

### Step 1: 1. Create a Namespace

Create a dedicated namespace for this lab to isolate the resources. This is good practice for managing different applications or environments within the same cluster.

```bash
kubectl create namespace biometric-data-ns
kubectl config set-context --current --namespace=biometric-data-ns
```

Verify the namespace creation:

```bash
kubectl get namespaces
```

### Step 2: 2. Create a ConfigMap for Application Settings

Create a ConfigMap to store non-sensitive configuration data for the application, such as the data processing algorithm version. This avoids hardcoding values in the application code.

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: biometric-app-config
data:
  algorithm_version: "v1.2"
  processing_threads: "4"
```

Apply the ConfigMap:

```bash
kubectl apply -f configmap.yaml
```

Verify the ConfigMap:

```bash
kubectl get configmaps biometric-app-config -o yaml
```

### Step 3: 3. Create a Secret for Sensitive Data

Create a Secret to store sensitive data, such as API keys or database credentials.  In this simulation, we'll use a placeholder for a biometric data encryption key.

```yaml
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: biometric-data-secret
type: Opaque
data:
  encryption_key: $(echo -n "supersecretkey" | base64)
```

Apply the Secret:

```bash
kubectl apply -f secret.yaml
```

Verify the Secret (note: you won't see the actual value, only the metadata):

```bash
kubectl get secrets biometric-data-secret -o yaml
```

**Important:** Never commit secrets to version control. Use tools like `kubectl create secret generic` or Sealed Secrets for better security in production.

### Step 4: 4. Define a Deployment

Create a Deployment that uses the ConfigMap and Secret. The application will read the configuration values from the ConfigMap and Secret as environment variables.

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: biometric-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: biometric-app
  template:
    metadata:
      labels:
        app: biometric-app
    spec:
      containers:
      - name: biometric-processor
        image: busybox:latest
        command: ["/bin/sh", "-c", "echo 'Starting biometric processor...' && env && sleep 3600"]
        env:
        - name: ALGORITHM_VERSION
          valueFrom:
            configMapKeyRef:
              name: biometric-app-config
              key: algorithm_version
        - name: PROCESSING_THREADS
          valueFrom:
            configMapKeyRef:
              name: biometric-app-config
              key: processing_threads
        - name: ENCRYPTION_KEY
          valueFrom:
            secretKeyRef:
              name: biometric-data-secret
              key: encryption_key
```

Apply the Deployment:

```bash
kubectl apply -f deployment.yaml
```

Verify the Deployment:

```bash
kubectl get deployments biometric-app
kubectl get pods -l app=biometric-app
```

### Step 5: 5. Verify Configuration

Check the logs of one of the Pods to verify that the environment variables are correctly set with the values from the ConfigMap and Secret.

```bash
POD_NAME=$(kubectl get pods -l app=biometric-app -o jsonpath='{.items[0].metadata.name}')
kubectl logs $POD_NAME
```

Look for the `ALGORITHM_VERSION`, `PROCESSING_THREADS`, and `ENCRYPTION_KEY` environment variables in the output.  You should see the values from the ConfigMap and Secret.

### Step 6: 6. Create a Service (Optional)

If you want to expose the application within the cluster, create a Service. Since the application in this example doesn't actually serve any traffic, this step is optional but demonstrates how to expose a service.

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: biometric-app-service
spec:
  selector:
    app: biometric-app
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
  type: ClusterIP
```

Apply the Service:

```bash
kubectl apply -f service.yaml
```

Verify the Service:

```bash
kubectl get services biometric-app-service
```

### Step 7: 7. Implement RBAC (Role-Based Access Control)

Control access to the sensitive data by creating a Role and RoleBinding.  This example restricts access to the `biometric-data-secret` Secret to a specific user or service account.  First create a service account:

```bash
kubectl create serviceaccount data-auditor
```

Then create a role that only allows getting the secret:

```yaml
# rbac.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: secret-reader
rules:
- apiGroups: [""]
  resources: ["secrets"]
  resourceNames: ["biometric-data-secret"]
  verbs: ["get"]
```

Apply the role:

```bash
kubectl apply -f rbac.yaml
```

Now bind the role to the service account:

```yaml
# rolebinding.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-biometric-secret
subjects:
- kind: ServiceAccount
  name: data-auditor
  namespace: biometric-data-ns
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: secret-reader
```

Apply the role binding:

```bash
kubectl apply -f rolebinding.yaml
```

This setup ensures that only the `data-auditor` service account can retrieve the `biometric-data-secret` Secret.  Attempting to access the secret with a different user or service account will be denied.

### Step 8: 8. Update the Application Configuration

Update the application configuration by modifying the ConfigMap. For example, change the `algorithm_version`.

```bash
kubectl edit configmap biometric-app-config
```

Change the `algorithm_version` to `v1.3`.

Kubernetes will automatically perform a rolling update of the Deployment, and the new Pods will use the updated configuration. Verify this by checking the logs of the new Pods.

```bash
POD_NAME=$(kubectl get pods -l app=biometric-app -o jsonpath='{.items[0].metadata.name}')
kubectl logs $POD_NAME
```

### Step 9: 9. Cleanup

Delete the namespace to remove all resources created in this lab.

```bash
kubectl delete namespace biometric-data-ns
```


<details>
<summary> Hints (click to expand)</summary>

1. If the deployment isn't starting, check the ConfigMap and Secret names in the deployment.yaml file.
2. Ensure that the `encryption_key` in the `secret.yaml` is base64 encoded.
3. If you are facing RBAC issues, ensure the service account exists and the role and rolebinding are configured correctly with the correct namespace.

</details>


<details>
<summary>✅ Solution Notes (spoiler)</summary>

The solution involves creating a Kubernetes namespace, ConfigMap, and Secret to simulate handling biometric data. A Deployment is then created to run an application that uses these configurations. Finally, RBAC is implemented to control access to the sensitive data. The application is updated by modifying the ConfigMap, demonstrating a rolling update.

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
