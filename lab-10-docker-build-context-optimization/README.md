# Lab 10: Docker Build Context Optimization

![Difficulty: Medium](https://img.shields.io/badge/Difficulty-Medium-yellow) ![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

> **Auto-generated lab** - Created on 2025-12-27

## Description

This lab explores how to optimize Docker build contexts to reduce image build times and improve security. We'll focus on using `.dockerignore` effectively and understanding the implications of build context size.

## Learning Objectives

- Understand the Docker build context and its impact on build performance.
- Learn how to use `.dockerignore` to exclude unnecessary files and directories from the build context.
- Optimize a Dockerfile to reduce image size and build time.
- Analyze the security implications of a large build context.

## Prerequisites

- Docker installed and running
- Basic understanding of Dockerfiles

## Lab Steps

### Step 1: Set up the Project Directory

Create a new directory for the project and navigate into it.

```bash
mkdir docker-build-context-demo
cd docker-build-context-demo
```

Inside this directory, create the following files:

*   `app.py` (a simple Python application)
*   `requirements.txt` (Python dependencies)
*   `Dockerfile` (the Dockerfile for building the image)
*   `.dockerignore` (to exclude files from the build context)
*   `large_file.txt` (a large dummy file to simulate unnecessary data)


### Step 2: Create the Python Application (app.py)

Create a simple Python "Hello, World!" application.

```python
# app.py
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
```

### Step 3: Define Python Dependencies (requirements.txt)

Specify the Flask dependency.

```
# requirements.txt
Flask==2.3.3
```

### Step 4: Create a Large Dummy File (large_file.txt)

Create a large file to simulate unnecessary data in the build context. This file will be used to demonstrate the impact of a large build context.

```bash
dd if=/dev/urandom of=large_file.txt bs=1M count=100
```

This command creates a 100MB file named `large_file.txt`.

### Step 5: Initial Dockerfile (Dockerfile)

Create a basic Dockerfile to build the application image.

```dockerfile
# Dockerfile
FROM python:3.9-slim-buster

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]
```

### Step 6: Build the Initial Image

Build the Docker image using the initial Dockerfile.

```bash
docker build -t initial-image .
```

Note the build time and image size. Check the files included in the build context.

### Step 7: Create a .dockerignore File

Create a `.dockerignore` file to exclude the large dummy file and other unnecessary files from the build context.

```
# .dockerignore
large_file.txt
*.pyc
__pycache__/
```

### Step 8: Optimize the Dockerfile (Dockerfile)

Modify the Dockerfile to only copy the necessary files after installing dependencies. This leverages Docker's layer caching.

```dockerfile
# Dockerfile
FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

CMD ["python", "app.py"]
```

### Step 9: Build the Optimized Image

Build the Docker image using the optimized Dockerfile and `.dockerignore` file.

```bash
docker build -t optimized-image .
```

Compare the build time and image size with the initial image. You should see a significant improvement.

### Step 10: Run and Test the Optimized Image

Run the optimized Docker image and test the application.

```bash
docker run -d -p 5000:5000 optimized-image
```

Open your browser and navigate to `http://localhost:5000` to see the "Hello, World!" message.

### Step 11: Analyze Build Context Security

Consider what sensitive data might unintentionally be included in the build context (e.g., `.env` files, SSH keys).  Ensure your `.dockerignore` file excludes these files to prevent them from being included in the final image.  Even if you don't COPY them into the image, they are still present in the build context during the build process, increasing the potential attack surface.

As an exercise, try adding a dummy `.env` file with a fake API key and observe if it's present in the image layers (using `docker history optimized-image`).  Then, add `.env` to `.dockerignore` and rebuild to confirm it's excluded.


<details>
<summary> Hints (click to expand)</summary>

1. Ensure your `.dockerignore` file is in the same directory as your Dockerfile.
2. Use `docker history <image_id>` to inspect the layers of your Docker image and identify large layers.
3. Consider using multi-stage builds for even more optimization.

</details>


<details>
<summary>✅ Solution Notes (spoiler)</summary>

The key to this lab is understanding that the entire directory where you run `docker build` is sent to the Docker daemon. Excluding unnecessary files with `.dockerignore` drastically reduces build time and image size. Optimizing the Dockerfile by copying only necessary files and leveraging layer caching further enhances performance. Finally, being mindful of sensitive data in the build context is crucial for security.

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
