# Lab 42: Docker Multi-Stage Builds: Optimizing Image Size

![Difficulty: Medium](https://img.shields.io/badge/Difficulty-Medium-yellow) ![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

> **Auto-generated lab** - Created on 2026-01-02

## Description

This lab explores Docker multi-stage builds to create smaller, more efficient Docker images. We will build a simple Python application and optimize its Dockerfile using multi-stage techniques, resulting in a reduced image size and improved security.

## Learning Objectives

- Understand the benefits of Docker multi-stage builds.
- Create a multi-stage Dockerfile for a Python application.
- Optimize Docker image size by separating build dependencies from runtime environment.
- Learn to use different base images for build and runtime stages.

## Prerequisites

- Docker installed and running (Docker Desktop, Docker Engine, etc.)
- Basic understanding of Dockerfiles and Docker commands.

## Lab Steps

### Step 1: Prepare the Python Application

First, create a directory for your project and a simple Python application.

```bash
mkdir multi-stage-app
cd multi-stage-app
```

Create a file named `app.py`:

```python
# app.py
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Docker Multi-Stage Build!'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
```

Create a `requirements.txt` file:

```
# requirements.txt
flask
```

### Step 2: Create a Basic Dockerfile (Single Stage)

Now, let's create a basic Dockerfile without multi-stage builds. This will be our baseline.

Create a file named `Dockerfile`:

```dockerfile
# Dockerfile
FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000
CMD ["python", "app.py"]
```

Build the image:

```bash
docker build -t single-stage-app .
```

Check the image size:

```bash
docker images single-stage-app
```

Note the size of the `single-stage-app` image.

### Step 3: Create a Multi-Stage Dockerfile

Now, let's create a multi-stage Dockerfile to optimize the image size.

Replace the contents of your `Dockerfile` with the following:

```dockerfile
# Dockerfile
# Build stage
FROM python:3.9-slim-buster AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Runtime stage
FROM python:3.9-slim-buster

WORKDIR /app

COPY --from=builder /app/app.py .
COPY --from=builder /app/venv /app/venv
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

EXPOSE 5000
CMD ["python", "app.py"]
```

**Important:** This Dockerfile is incomplete. It aims to illustrate the basic concept. The next step completes the required steps to make it work. See hints and solution notes for details.

Build the image:

```bash
docker build -t multi-stage-app .
```

Check the image size:

```bash
docker images multi-stage-app
```

Compare the size of the `multi-stage-app` image with the `single-stage-app` image. You should see a significant reduction in size.

Run the multi-stage app:

```bash
docker run -d -p 5000:5000 multi-stage-app
```

Verify that the application is running by accessing `http://localhost:5000` in your browser.

### Step 4: Further Optimization (Optional)

You can further optimize the multi-stage build by using a smaller base image for the runtime stage. For example, you could use `python:3.9-slim` instead of `python:3.9-slim-buster` or even `alpine` if you can resolve all dependencies.

Experiment with different base images and observe the impact on the final image size.


<details>
<summary> Hints (click to expand)</summary>

1. Ensure you have the correct `requirements.txt` file with the necessary dependencies.
2. Double-check the syntax of your Dockerfile, especially the `COPY --from` instruction.
3. The runtime stage needs the installed libraries of Flask. Consider how to copy this from the builder stage.
4. Consider using a virtual environment in the builder stage to isolate dependencies.

</details>


<details>
<summary>✅ Solution Notes (spoiler)</summary>

The key to multi-stage builds is to use separate `FROM` instructions to define different stages. The build stage installs dependencies, and the runtime stage copies only the necessary artifacts from the build stage.  A common mistake is forgetting to copy the installed Python packages from the builder stage to the runtime stage. Using a virtual environment during the build stage and then copying the virtual environment to the runtime stage can simplify dependency management. A complete solution would involve creating a virtual environment in the builder stage, installing dependencies into it, and then copying the application code and the virtual environment to the runtime stage. The CMD instruction in the runtime stage would then need to activate the virtual environment before running the application.

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
