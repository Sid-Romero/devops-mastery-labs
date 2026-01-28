# Lab 74: Kubernetes Resource Optimization: CPU & Memory Limits

![Difficulty: Medium](https://img.shields.io/badge/Difficulty-Medium-yellow) ![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?logo=kubernetes&logoColor=white)

> **Auto-generated lab** - Created on 2026-01-28

## Description

Learn how to optimize Kubernetes resource usage by setting CPU and memory limits and requests. This lab guides you through deploying an application, observing its resource consumption, and then applying resource constraints to improve efficiency and reduce potential AWS costs.

## Learning Objectives

- Understand Kubernetes resource requests and limits.
- Deploy a sample application to a Kubernetes cluster.
- Monitor resource usage of a pod.
- Configure CPU and memory requests and limits for a deployment.
- Observe the impact of resource constraints on pod behavior.

## Prerequisites

- A running Kubernetes cluster (minikube, Docker Desktop, or a cloud provider cluster)
- kubectl installed and configured
- Basic understanding of Kubernetes deployments and pods

## Lab Steps

### Step 1: Step 1: Deploy a Sample Application

We'll deploy a simple application that consumes some CPU and memory. Create a file named `app.yaml` with the following content:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: resource-demo
spec:
  replicas: 1
  selector:
    matchLabels:
      app: resource-demo
  template:
    metadata:
      labels:
        app: resource-demo
    spec:
      containers:
      - name: resource-demo-container
        image: polinux/stress
        command: ['stress']
        args: ['--cpu', '1', '--vm', '1', '--vm-bytes', '256M', '--timeout', '3600s']
```

Apply the deployment:

```bash
kubectl apply -f app.yaml
```

Verify the deployment and pod are running:

```bash
kubectl get deployments
kubectl get pods
```

### Step 2: Step 2: Monitor Resource Usage

To understand the application's resource consumption, use `kubectl top`.  If you don't have metrics server installed, you'll need to install it.  Follow the instructions here: [https://github.com/kubernetes-sigs/metrics-server](https://github.com/kubernetes-sigs/metrics-server). For minikube, you can enable it with: `minikube addons enable metrics-server`.

Once metrics server is installed, run the following commands:

```bash
kubectl top pod
kubectl top node
```

Observe the CPU and memory usage of the `resource-demo` pod.  Note the values.  Let the application run for a few minutes to get a stable reading.

### Step 3: Step 3: Configure Resource Requests and Limits

Now, let's add resource requests and limits to the `app.yaml` file. Edit the file and add the `resources` section to the container definition:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: resource-demo
spec:
  replicas: 1
  selector:
    matchLabels:
      app: resource-demo
  template:
    metadata:
      labels:
        app: resource-demo
    spec:
      containers:
      - name: resource-demo-container
        image: polinux/stress
        command: ['stress']
        args: ['--cpu', '1', '--vm', '1', '--vm-bytes', '256M', '--timeout', '3600s']
        resources:
          requests:
            cpu: 500m
            memory: 128Mi
          limits:
            cpu: 1000m
            memory: 256Mi
```

Apply the updated deployment:

```bash
kubectl apply -f app.yaml
```

Kubernetes will attempt to reschedule the pod with the new resource constraints. Check the status of the pod:

```bash
kubectl get pods
```

### Step 4: Step 4: Observe the Impact of Resource Constraints

After the pod is running, monitor its resource usage again using `kubectl top pod`.

```bash
kubectl top pod
```

Observe how the resource usage compares to the previous values. Also, describe the pod:

```bash
kubectl describe pod <pod-name>
```

Look for events related to resource constraints (e.g., OOMKilled). Try adjusting the resource limits to see how it affects the pod's behavior. For example, set the memory limit lower than the application's actual usage and observe what happens.

### Step 5: Step 5: Cleanup

To clean up the resources created in this lab, delete the deployment:

```bash
kubectl delete deployment resource-demo
```


<details>
<summary> Hints (click to expand)</summary>

1. If `kubectl top pod` shows errors, ensure metrics-server is properly installed and running. Check its logs for any issues.
2. If the pod fails to start after applying resource limits, check if the limits exceed the available resources on the node.
3. Consider using horizontal pod autoscaling (HPA) to automatically adjust the number of pods based on resource utilization.

</details>


<details>
<summary>✅ Solution Notes (spoiler)</summary>

This lab provides a basic understanding of resource management in Kubernetes. Setting appropriate resource requests and limits is crucial for ensuring efficient resource utilization and preventing resource contention. Regularly monitoring and adjusting these settings based on application needs is essential for optimizing performance and reducing costs in a Kubernetes environment. The `stress` tool is useful for simulating resource intensive workloads for testing purposes.

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
