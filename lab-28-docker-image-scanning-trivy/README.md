# Lab 28: Docker Image Scanning and Security with Trivy

![Difficulty: Medium](https://img.shields.io/badge/Difficulty-Medium-yellow) ![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

> **Auto-generated lab** - Created on 2025-12-31

## Description

This lab focuses on integrating security scanning into your Docker workflow. You'll learn how to use Trivy, a popular open-source vulnerability scanner, to identify security issues in your Docker images and implement a basic security gate.

## Learning Objectives

- Learn how to install and configure Trivy.
- Scan Docker images for vulnerabilities using Trivy.
- Integrate Trivy into a Docker build process to enforce security policies.
- Understand how to interpret Trivy scan results.

## Prerequisites

- Docker installed and running.
- Basic understanding of Docker images and Dockerfiles.
- Internet connection for downloading Trivy and vulnerability databases.

## Lab Steps

### Step 1: Install Trivy

First, you need to install Trivy. The installation method varies depending on your operating system. Here's how to install it on Linux using apt:

```bash
sudo apt-get install wget apt-transport-https gnupg lsb-release
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main | sudo tee /etc/apt/sources.list.d/trivy.list
sudo apt-get update
sudo apt-get install trivy
```

For other operating systems (macOS, Windows), refer to the official Trivy documentation: [https://aquasecurity.github.io/trivy/v0.49/getting-started/installation/](https://aquasecurity.github.io/trivy/v0.49/getting-started/installation/)

Verify the installation by running:

```bash
trivy --version
```

### Step 2: Update Trivy Vulnerability Database

Trivy relies on a vulnerability database to identify security issues. Update the database before scanning images:

```bash
trivy image --download-db-only
```

This command downloads the latest vulnerability database without scanning any images. This process can take several minutes depending on your internet connection.

### Step 3: Create a Sample Dockerfile

Create a simple Dockerfile to use for scanning. This Dockerfile will be based on `ubuntu:latest` and install `curl`.

Create a file named `Dockerfile` with the following content:

```dockerfile
FROM ubuntu:latest

RUN apt-get update && apt-get install -y curl

CMD ["/bin/bash"]
```

### Step 4: Build the Docker Image

Build the Docker image using the Dockerfile you created:

```bash
docker build -t my-ubuntu-image .
```

This command builds an image named `my-ubuntu-image` from the current directory.

### Step 5: Scan the Docker Image with Trivy

Now, scan the Docker image for vulnerabilities using Trivy:

```bash
trivy image my-ubuntu-image
```

Trivy will analyze the image and report any identified vulnerabilities.  Examine the output carefully.  It will list vulnerabilities by severity and component.

### Step 6: Integrate Trivy into the Docker Build Process

To automatically scan images during the build process, you can add a Trivy scan step to your Dockerfile.  However, Dockerfiles cannot execute arbitrary commands that would stop the build. Instead, we'll use a script to perform the scan and exit with a non-zero code if vulnerabilities are found.

Create a file named `scan.sh` with the following content:

```bash
#!/bin/bash

trivy image --exit-code 1 --severity HIGH,CRITICAL my-ubuntu-image
```

Make the script executable:

```bash
chmod +x scan.sh
```

Now modify the Dockerfile to include the scan. Add these lines *after* the `RUN` instruction and *before* the `CMD` instruction.  Also, install Trivy inside the docker image using the same command from Step 1.

```dockerfile
FROM ubuntu:latest

RUN apt-get update && apt-get install -y curl

RUN apt-get install wget apt-transport-https gnupg lsb-release && \
    wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | apt-key add - && \
    echo deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main | tee /etc/apt/sources.list.d/trivy.list && \
    apt-get update && \
    apt-get install -y trivy

RUN trivy image --exit-code 1 --severity HIGH,CRITICAL ubuntu:latest || exit 1

CMD ["/bin/bash"]
```

Rebuild the image:

```bash
docker build -t my-ubuntu-image .
```

If Trivy finds any vulnerabilities with `HIGH` or `CRITICAL` severity, the build will fail.


<details>
<summary> Hints (click to expand)</summary>

1. Ensure that Trivy is correctly installed and configured.
2. Make sure the vulnerability database is up-to-date before scanning.
3. Double-check the Dockerfile for any syntax errors.
4. Verify that the scan.sh script is executable.
5. The `|| exit 1` part of the Dockerfile `RUN` command is crucial for failing the build if Trivy finds issues.

</details>


<details>
<summary>✅ Solution Notes (spoiler)</summary>

The solution involves installing Trivy, updating its database, creating a sample Dockerfile, building an image, and then scanning the image with Trivy. Finally, the lab demonstrates how to integrate Trivy into the Docker build process to automatically fail builds if vulnerabilities are found. The key is using `--exit-code 1` in the `trivy` command and `|| exit 1` in the Dockerfile to propagate the failure.

</details>


---

## Notes

- **Difficulty:** Medium
- **Estimated time:** 45-75 minutes
- **Technology:** Docker

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
