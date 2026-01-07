# Lab 53: Secure CI/CD: Docker Image Scanning with Trivy

![Difficulty: Medium](https://img.shields.io/badge/Difficulty-Medium-yellow) ![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

> **Auto-generated lab** - Created on 2026-01-07

## Description

This lab demonstrates how to integrate security scanning into your Docker build process using Trivy, a comprehensive security scanner. By scanning Docker images during the CI/CD pipeline, you can identify and address vulnerabilities early, improving the overall security posture of your applications.

## Learning Objectives

- Learn how to integrate Trivy into a Docker build process.
- Understand how to scan Docker images for vulnerabilities.
- Implement a Dockerfile that fails the build if vulnerabilities are found.
- Gain experience using Docker multi-stage builds for security.
- Learn how to use .dockerignore to exclude sensitive files from the build context.

## Prerequisites

- Docker installed and running
- Basic knowledge of Dockerfiles and Docker commands
- Familiarity with command-line interface

## Lab Steps

### Step 1: Create a Sample Application

First, let's create a simple application. This will be a basic Python Flask app. Create a directory named `app` and add the following files:

**app/app.py:**
```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
```

**app/requirements.txt:**
```
Flask==2.0.1
Werkzeug==2.0.1
```

This is a vulnerable version of Flask. We are doing this on purpose to demonstrate vulnerability scanning.


### Step 2: Create a .dockerignore File

Create a `.dockerignore` file in the root directory. This file tells Docker which files and directories to exclude from the build context. This is essential for security, preventing sensitive files (e.g., SSH keys, API keys) from being included in the image.

**.dockerignore:**
```
.git
.gitignore
secrets.txt
```

Create an empty `secrets.txt` file to demonstrate that the `.dockerignore` file is working correctly. `touch secrets.txt`.


### Step 3: Create a Dockerfile with Trivy Integration

Now, create a `Dockerfile` in the root directory. This Dockerfile will use a multi-stage build to install dependencies, scan for vulnerabilities using Trivy, and then copy the application code into a final, minimal image.

**Dockerfile:**
```dockerfile
# Stage 1: Build stage with Trivy
FROM python:3.9-slim-buster AS builder

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app . 

# Install Trivy
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/aquasecurity/trivy/releases/download/v0.46.0/trivy_0.46.0_Linux-64bit.tar.gz
RUN tar zxvf trivy_0.46.0_Linux-64bit.tar.gz
RUN mv trivy /usr/local/bin

# Run Trivy scan and fail the build if vulnerabilities are found
RUN trivy image --exit-code 1 --severity HIGH,CRITICAL --no-progress --format json --output results.json .
RUN if [ -s results.json ]; then cat results.json; exit 1; else exit 0; fi

# Stage 2: Final image
FROM python:3.9-slim-buster AS final

WORKDIR /app

COPY --from=builder /app . 

EXPOSE 5000
CMD ["python", "app.py"]
```

This Dockerfile does the following:
1.  Uses a `builder` stage based on a Python image.
2.  Installs dependencies from `requirements.txt`.
3.  Copies the application code.
4.  Installs Trivy.
5.  Runs Trivy to scan the image for vulnerabilities.  The `--exit-code 1` flag tells Trivy to exit with a non-zero exit code if any vulnerabilities are found with HIGH or CRITICAL severity, causing the Docker build to fail.
6. Copies the application code into the final image
7. Defines the command to run the application.


### Step 4: Build the Docker Image

Build the Docker image using the following command:

```bash
docker build -t secure-app .
```

Observe the output. The build should fail because Trivy will detect vulnerabilities in the Flask package.

If the build succeeds (which is unlikely given the vulnerable dependency), double-check the `requirements.txt` file and ensure it contains the vulnerable Flask version.

### Step 5: Update the Flask Version and Rebuild

Update the `app/requirements.txt` file to use a more recent, secure version of Flask.

**app/requirements.txt:**
```
Flask==2.3.3
Werkzeug==2.3.7
```

Rebuild the Docker image:

```bash
docker build -t secure-app .
```

This time, the build should succeed because the updated Flask version does not contain the vulnerabilities detected by Trivy.

### Step 6: Run the Docker Image

Run the Docker image to verify that the application is working:

```bash
docker run -p 5000:5000 secure-app
```

Open your browser and navigate to `http://localhost:5000`. You should see the 'Hello, World!' message.


<details>
<summary> Hints (click to expand)</summary>

1. Ensure you have the correct versions of Flask in requirements.txt.
2. Verify that Trivy is installed correctly inside the Dockerfile.
3. Check your `.dockerignore` file to ensure it's excluding sensitive files.

</details>


<details>
<summary>✅ Solution Notes (spoiler)</summary>

The solution involves creating a multi-stage Dockerfile that installs Trivy, scans the image for vulnerabilities, and fails the build if any HIGH or CRITICAL vulnerabilities are found. The application's dependencies are initially set to vulnerable versions to demonstrate the scanning process, then updated to secure versions to allow the build to succeed.

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
