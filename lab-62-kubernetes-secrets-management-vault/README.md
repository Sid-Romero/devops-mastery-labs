# Lab 62: Kubernetes Secrets Management with Vault

![Difficulty: Medium](https://img.shields.io/badge/Difficulty-Medium-yellow) ![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?logo=kubernetes&logoColor=white)

> **Auto-generated lab** - Created on 2026-01-16

## Description

This lab guides you through deploying HashiCorp Vault within a Kubernetes cluster and using it to manage secrets for an application. You'll learn how to authenticate to Vault from within Kubernetes and retrieve secrets.

## Learning Objectives

- Deploy HashiCorp Vault in Kubernetes
- Configure Vault authentication using Kubernetes Service Accounts
- Create a Kubernetes application that retrieves secrets from Vault

## Prerequisites

- kubectl installed and configured
- A Kubernetes cluster (e.g., minikube, Docker Desktop)
- helm installed
- Basic understanding of Kubernetes concepts (Pods, Deployments, Services)

## Lab Steps

### Step 1: Deploy Vault using Helm

First, add the HashiCorp Helm repository:

```bash
helm repo add hashicorp https://helm.releases.hashicorp.com
helm repo update
```

Next, install Vault using Helm.  Create a `values.yaml` file to customize the Vault installation. This file will disable TLS for simplicity in this lab, but remember to enable TLS in production environments.

```bash
cat <<EOF > vault-values.yaml
server:
  ingress:
    enabled: false
  service:
    enabled: true
    type: NodePort
  ha:
    enabled: false
ui:
  enabled: true
telemetry:
  enabled: false

EOF
```

Now, install Vault:

```bash
helm install vault hashicorp/vault -f vault-values.yaml
```

Wait for the Vault pods to be ready. You can check their status using:

```bash
kubectl get pods -l app=vault
```

Note the `NodePort` assigned to the vault service. You will need this to access the Vault UI.

```bash
kubectl get svc vault
```

### Step 2: Initialize and Unseal Vault

Vault needs to be initialized and unsealed before it can be used. Since HA is disabled, we can use the `vault operator init` and `vault operator unseal` commands.

First, port-forward to the Vault pod to access the CLI:

```bash
kubectl port-forward service/vault 8200:8200
```

In a separate terminal, initialize Vault:

```bash
export VAULT_ADDR='http://127.0.0.1:8200'
vault operator init
```

This command will output unseal keys and the root token.  **Carefully store these values; you will need them.**

Next, unseal Vault using the unseal keys. Run the following command three times, each time providing one of the unseal keys:

```bash
vault operator unseal
```

Finally, log in to Vault using the root token:

```bash
vault login YOUR_ROOT_TOKEN
```

You can now access the Vault UI in your browser by navigating to `http://localhost:8200` and logging in with the root token.

### Step 3: Enable Kubernetes Authentication

Vault needs to be configured to trust the Kubernetes cluster. This is done by enabling the Kubernetes authentication method.

First, enable the Kubernetes authentication method:

```bash
vault auth enable kubernetes
```

Next, configure the Kubernetes authentication method. You will need the Kubernetes API server address and the Kubernetes CA certificate.  These can be obtained from the Kubernetes cluster.  Since we are using a local cluster, we can retrieve the API address and CA certificate from the Kubernetes service account.

```bash
export K8S_HOST=$(kubectl config view -o jsonpath='{.clusters[0].cluster.server}')
export K8S_CA_CRT=$(kubectl config view -o jsonpath='{.clusters[0].cluster.certificate-authority-data}' | base64 --decode)

vault write auth/kubernetes/config \
  token_reviewer_jwt_ttl=60 \
  kubernetes_host="$K8S_HOST" \
  kubernetes_ca_cert="$(echo $K8S_CA_CRT)"
```

Now, create a Vault policy that grants access to specific secrets.  Create a file named `policy.hcl` with the following content:

```hcl
path "secret/data/myapp/*" {
  capabilities = ["read"]
}
```

This policy allows reading secrets under the `secret/data/myapp/` path.  Write the policy to Vault:

```bash
vault policy write myapp policy.hcl
```

Finally, create a Vault role that maps the Kubernetes service account to the Vault policy.  This role will allow pods running with a specific service account to authenticate to Vault and access the secrets defined in the policy.

```bash
vault write auth/kubernetes/role/myapp \
  bound_service_account_names=default \
  bound_service_account_namespaces=default \
  policies=myapp \
  ttl=60m
```

This role is named `myapp`, is bound to the `default` service account in the `default` namespace, and grants the `myapp` policy.  The `ttl` specifies the maximum time-to-live for the Vault token.

### Step 4: Create a Kubernetes Application

Now, create a Kubernetes application that retrieves secrets from Vault.  First, create a Kubernetes deployment.  The deployment will mount the Kubernetes service account token and use it to authenticate to Vault. The application will read a secret from Vault using the Vault API.

Create a file named `app.yaml` with the following content:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 1
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: busybox:latest
        command: ['sh', '-c', 'sleep 3600']
        env:
        - name: VAULT_ADDR
          value: 'http://vault:8200'
        - name: VAULT_TOKEN_PATH
          value: '/var/run/secrets/kubernetes.io/serviceaccount/token'
        - name: VAULT_ROLE
          value: 'myapp'
        - name: SECRET_PATH
          value: 'secret/data/myapp/mysecret'
        volumeMounts:
        - name: vault-token
          mountPath: /var/run/secrets/kubernetes.io/serviceaccount
          readOnly: true
      volumes:
      - name: vault-token
        secret:
          secretName: default-token # make sure to use the correct token name
          defaultMode: 420

---
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
  type: ClusterIP

```
Before applying this file, find the actual secret name for the default-token. It will be `default-token-<random-string>`. Use this value in the spec. 

Apply the deployment and service:

```bash
kubectl apply -f app.yaml
```

Now, create a secret in Vault that the application will retrieve:

```bash
vault kv put secret/data/myapp/mysecret myvalue=hello
```

Finally, connect to the pod and verify that the application can retrieve the secret from Vault.  First, get the pod name:

```bash
kubectl get pods -l app=myapp
```

Then, execute a shell inside the pod:

```bash
kubectl exec -it YOUR_POD_NAME -- sh
```

Inside the pod, install `curl`:

```bash
apk add curl
```

Then, retrieve the Vault token from the service account token file:

```bash
VAULT_TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
```

Finally, use the Vault token to retrieve the secret from Vault:

```bash
curl -s -H "X-Vault-Token: $VAULT_TOKEN" $VAULT_ADDR/v1/$SECRET_PATH | jq -r '.data.data.myvalue'
```

You should see the value `hello` printed to the console.  This confirms that the application can successfully authenticate to Vault and retrieve secrets.


<details>
<summary> Hints (click to expand)</summary>

1. Ensure the Vault service is running before attempting to initialize it.
2. Double-check the Vault token path in the application deployment.
3. Make sure the default-token secret name in app.yaml is correct.

</details>


<details>
<summary>✅ Solution Notes (spoiler)</summary>

The lab demonstrates how to deploy Vault, configure Kubernetes authentication, and retrieve secrets from a Kubernetes application. The key steps are initializing and unsealing Vault, enabling the Kubernetes auth method, creating a Vault policy and role, and configuring the application to authenticate to Vault using its service account token. Remember to enable TLS in production environments.

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
