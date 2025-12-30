# Lab 26: Kubernetes: EmptyDir vs. HostPath for Temporary Storage

![Difficulty: Easy](https://img.shields.io/badge/Difficulty-Easy-brightgreen) ![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?logo=kubernetes&logoColor=white)

> **Auto-generated lab** - Created on 2025-12-30

## Description

This lab explores the use of `emptyDir` and `hostPath` volumes in Kubernetes for temporary storage. You'll learn the characteristics of each volume type and their implications for data persistence and security.

## Learning Objectives

- Understand the difference between `emptyDir` and `hostPath` volumes.
- Learn how to configure pods to use these volume types.
- Explore the implications of using `hostPath` for data persistence and security.
- Deploy a simple application that utilizes temporary storage.

## Prerequisites

- A running Kubernetes cluster (e.g., Minikube, Docker Desktop)
- kubectl installed and configured to connect to your cluster

## Lab Steps

### Step 1: Step 1: Create a Pod using `emptyDir`

Let's start by creating a pod that uses an `emptyDir` volume. This volume is created when the pod is assigned to a node and exists as long as that pod is running on that node. The data in `emptyDir` will be lost when the pod is deleted or evicted.

Create a file named `empty-dir-pod.yaml` with the following content:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: emptydir-pod
spec:
  containers:
    - name: busybox
      image: busybox:latest
      command: ["/bin/sh", "-c", "while true; do date >> /data/my-file.txt; sleep 5; done"]
      volumeMounts:
        - name: data-volume
          mountPath: /data
  volumes:
    - name: data-volume
      emptyDir: {}
```

Apply the configuration:

```bash
kubectl apply -f empty-dir-pod.yaml
```

Verify the pod is running:

```bash
kubectl get pods
```

Connect to the pod and verify the file is being created:

```bash
kubectl exec -it emptydir-pod -- /bin/sh
cat /data/my-file.txt
exit
```

Delete the pod:

```bash
kubectl delete pod emptydir-pod
```

Create the pod again and check the content of the file. Is it still there?

Solution note: The data is lost because `emptyDir`'s lifecycle is tied to the Pod.

### Step 2: Step 2: Create a Pod using `hostPath`

Now, let's create a pod that uses a `hostPath` volume. This volume mounts a directory or file from the host node's filesystem into the pod. This allows data to persist even after the pod is deleted, but it also introduces potential security risks and ties the pod to a specific node.

Create a file named `hostpath-pod.yaml` with the following content. **Important:** Change the `path` field to a directory that exists on your node.  A good option is `/tmp/hostpath-data` (create it if it doesn't exist).

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: hostpath-pod
spec:
  containers:
    - name: busybox
      image: busybox:latest
      command: ["/bin/sh", "-c", "while true; do date >> /data/my-file.txt; sleep 5; done"]
      volumeMounts:
        - name: data-volume
          mountPath: /data
  volumes:
    - name: data-volume
      hostPath:
        path: /tmp/hostpath-data
        type: DirectoryOrCreate
```

Apply the configuration:

```bash
kubectl apply -f hostpath-pod.yaml
```

Verify the pod is running:

```bash
kubectl get pods
```

Connect to the pod and verify the file is being created:

```bash
kubectl exec -it hostpath-pod -- /bin/sh
cat /data/my-file.txt
exit
```

Delete the pod:

```bash
kubectl delete pod hostpath-pod
```

Create the pod again and check the content of the file. Is it still there?
Check the content of the `/tmp/hostpath-data` on the node where the pod was running. Is it still there?

Solution note: The data persists because `hostPath` directly uses the node's filesystem.

### Step 3: Step 3: Scheduling considerations for `hostPath`

Since `hostPath` volumes are tied to a specific node, Kubernetes will try to schedule the pod on the same node if it's recreated. If the node is unavailable, the pod will remain in a pending state.  Let's simulate this.

First, identify the node where the `hostpath-pod` is running:

```bash
kubectl get pod hostpath-pod -o wide
```

Note the `NODE` column.

Now, try to delete the node. Since it's likely a local minikube or docker desktop node, you can't directly delete it, but you can simulate node failure by stopping your minikube or Docker Desktop.

After stopping the node, try to recreate the `hostpath-pod`:

```bash
kubectl apply -f hostpath-pod.yaml
```

Check the pod status. It will likely be in a `Pending` state.  Describe the pod to see why:

```bash
kubectl describe pod hostpath-pod
```

The output will show that Kubernetes is unable to schedule the pod because the `hostPath` volume is only available on the failed node.

Start your minikube/Docker Desktop node again.  The pod should eventually start.

Solution note: `hostPath` introduces node affinity, potentially causing scheduling issues if the node becomes unavailable. This is a significant limitation.

### Step 4: Step 4: Security implications of `hostPath`

`hostPath` volumes can pose security risks if not used carefully. If a pod with a `hostPath` volume is compromised, the attacker could potentially gain access to the host node's filesystem.

Consider a scenario where a pod mounts the root directory (`/`) of the host node using `hostPath`. This would give the container full access to the host filesystem, allowing it to modify system files, access sensitive data, or even execute arbitrary commands on the host.

**Never mount sensitive system directories like `/` or `/etc` using `hostPath`.**

To mitigate these risks:

*   Limit the scope of the `hostPath` volume to specific, isolated directories.
*   Use appropriate file permissions to restrict access to the mounted directory.
*   Consider using alternative storage solutions like Persistent Volumes and Persistent Volume Claims (PVCs) for more secure and manageable storage.

Solution note: `hostPath` should be used with caution due to potential security vulnerabilities. Always restrict the scope of the mounted directory and use appropriate file permissions.


<details>
<summary> Hints (click to expand)</summary>

1. Make sure the path specified in `hostPath` exists on your node.
2. If the pod is stuck in a `Pending` state, check the output of `kubectl describe pod <pod-name>` for clues.
3. Remember that `hostPath` volumes are tied to a specific node.

</details>


<details>
<summary>✅ Solution Notes (spoiler)</summary>

This lab demonstrates the differences between `emptyDir` and `hostPath` volumes. `emptyDir` provides temporary storage that is tied to the lifecycle of the pod. `hostPath` allows mounting directories or files from the host node, providing persistence but also introducing scheduling and security concerns. For production environments, Persistent Volumes and Persistent Volume Claims are generally preferred for managing storage.

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
