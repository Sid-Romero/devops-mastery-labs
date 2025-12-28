# Lab 17: Docker: Multi-Stage Builds & Image Optimization

![Difficulty: Medium](https://img.shields.io/badge/Difficulty-Medium-yellow) ![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

> **Auto-generated lab** - Created on 2025-12-28

## Description

This lab explores Docker multi-stage builds for creating smaller, more efficient container images. It focuses on separating build-time dependencies from runtime dependencies, leading to leaner and more secure images.

## Learning Objectives

- Understand the benefits of Docker multi-stage builds
- Create a Dockerfile using multi-stage build patterns
- Optimize image size by removing unnecessary dependencies
- Learn how to leverage build arguments for customization

## Prerequisites

- Docker installed and running
- Basic understanding of Dockerfiles and Docker commands

## Lab Steps

### Step 1: Project Setup: Create a Simple Python Application

First, create a directory for your project and a simple Python application.

```bash
mkdir docker-multistage-lab
cd docker-multistage-lab
```

Create a file named `app.py` with the following content:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World from Docker!\'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
```

Next, create a `requirements.txt` file to specify the Python dependencies:

```bash
echo 'Flask==2.3.2' > requirements.txt
```

### Step 2: Create a Single-Stage Dockerfile (Initial)

Create a Dockerfile named `Dockerfile` with the following content. This is a basic, single-stage Dockerfile:

```dockerfile
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

Note the size of the image. We will reduce this size in the next steps.

### Step 3: Convert to a Multi-Stage Dockerfile

Now, modify the Dockerfile to use multi-stage builds. This will separate the build environment (where dependencies are installed) from the runtime environment (where the application runs).

```dockerfile
# Builder stage
FROM python:3.9-slim-buster AS builder

WORKDIR /tmp/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.9-slim-buster

WORKDIR /app

COPY --from=builder /tmp/app/ ./
COPY app.py .

EXPOSE 5000
CMD ["python", "app.py"]
```

Build the image:

```bash
docker build -t multi-stage-app .
```

Check the image size:

```bash
docker images multi-stage-app
```

Compare the size of `multi-stage-app` with `single-stage-app`.  You should see a reduction in size.

### Step 4: Further Optimization: Using a Smaller Base Image

Let's optimize the runtime stage further by using an even smaller base image.  Instead of `python:3.9-slim-buster`, we can use `python:3.9-slim-buster-slim` (or even `python:3.9-alpine` but that requires more code changes due to musl vs glibc).

Modify the Dockerfile:

```dockerfile
# Builder stage
FROM python:3.9-slim-buster AS builder

WORKDIR /tmp/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.9-slim-buster-slim

WORKDIR /app

COPY --from=builder /tmp/app/ ./
COPY app.py .

EXPOSE 5000
CMD ["python", "app.py"]
```

Build the image:

```bash
docker build -t optimized-app .
```

Check the image size:

```bash
docker images optimized-app
```

Compare the size with the previous images. You should observe a further reduction.

### Step 5: Cleanup (Optional)

Remove the images to free up space:

```bash
docker rmi single-stage-app multi-stage-app optimized-app
```


<details>
<summary> Hints (click to expand)</summary>

1. Make sure your `requirements.txt` file is in the same directory as your `Dockerfile` when building the image.
2. The `--no-cache-dir` option in `pip install` helps reduce the image size by preventing the caching of downloaded packages.
3. Double-check that the paths in the `COPY` commands are correct.
4. Consider using `.dockerignore` to exclude unnecessary files from the build context.

</details>


<details>
<summary>✅ Solution Notes (spoiler)</summary>

The key to this lab is understanding how multi-stage builds allow you to use a larger image with build tools for compiling or installing dependencies, and then copy only the necessary artifacts to a smaller runtime image. Choosing the right base image for each stage is critical. The final optimized image should be significantly smaller than the initial single-stage image.

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
