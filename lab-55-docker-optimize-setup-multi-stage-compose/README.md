# Lab 55: Optimize Docker Setup: Multi-Stage Build & Compose

![Difficulty: Medium](https://img.shields.io/badge/Difficulty-Medium-yellow) ![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

> **Auto-generated lab** - Created on 2026-01-09

## Description

This lab demonstrates how to significantly reduce Docker image size and setup time using multi-stage builds and Docker Compose. You'll build a simple web application and optimize its Dockerfile for efficient image creation and deployment.

## Learning Objectives

- Understand and implement multi-stage Docker builds.
- Optimize Dockerfiles for smaller image sizes.
- Use Docker Compose for defining and managing multi-container applications.
- Implement basic health checks within a Docker Compose setup.

## Prerequisites

- Docker installed and running (Docker Desktop, etc.)
- Basic understanding of Docker concepts (images, containers)
- Text editor or IDE
- Command-line interface (terminal)

## Lab Steps

### Step 1: 1. Create a Simple Web Application

First, let's create a simple web application. This will be a basic Python Flask application.

Create a directory for your project:

```bash
mkdir docker-optimization-lab
cd docker-optimization-lab
```

Create a file named `app.py` with the following content:

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Docker!'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
```

Create a `requirements.txt` file specifying the dependencies:

```
Flask
```

### Step 2: 2. Initial Dockerfile (Unoptimized)

Create a `Dockerfile` in the same directory with the following content. This is a basic, unoptimized Dockerfile:

```dockerfile
FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

Build the image:

```bash
docker build -t web-app-unoptimized .
```

Check the image size:

```bash
docker images web-app-unoptimized
```

Note the size of the image. We will reduce this significantly in the next steps.

### Step 3: 3. Optimize with Multi-Stage Build

Now, let's optimize the Dockerfile using a multi-stage build. This will separate the build environment from the runtime environment, resulting in a smaller image.

Update the `Dockerfile` with the following content:

```dockerfile
# Builder stage
FROM python:3.9-slim-buster AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Final stage
FROM python:3.9-slim-buster

WORKDIR /app

COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --from=builder /app/app.py .

EXPOSE 5000

CMD ["python", "app.py"]
```

Build the optimized image:

```bash
docker build -t web-app-optimized .
```

Check the image size again:

```bash
docker images web-app-optimized
```

Compare the size with the unoptimized image.  You should see a significant reduction.  Consider using a smaller base image such as `python:3.9-slim` or `python:3.9-alpine` for further size reductions.

### Step 4: 4. Docker Compose Setup

Create a `docker-compose.yml` file to define and manage the web application container.

```yaml
version: '3.8'
services:
  web:
    image: web-app-optimized
    ports:
      - "5000:5000"
    restart: always
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000"]
      interval: 30s
      timeout: 10s
      retries: 3
```

This `docker-compose.yml` file defines a service named `web` using the `web-app-optimized` image. It maps port 5000 on the host to port 5000 in the container and sets a restart policy to `always`. It also configures a basic health check that uses `curl` to check if the application is responding.

Start the application using Docker Compose:

```bash
docker-compose up -d
```

Check the status of the container:

```bash
docker-compose ps
```

Ensure the application is running and the health check is passing.

### Step 5: 5. Further Optimization (Optional)

Explore further optimizations:

*   **Use a smaller base image:**  Experiment with `python:3.9-alpine` as the base image, but be aware of potential compatibility issues with certain Python packages.
*   **Exclude unnecessary files:** Use a `.dockerignore` file to exclude files and directories that are not needed in the image, such as `.git` directories or temporary files.
*   **Optimize pip installation:**  Use `--no-cache-dir` to avoid caching pip packages in the image, reducing its size.
*   **Use a reverse proxy:** Implement a reverse proxy like Nginx in front of the application to handle static assets and improve performance.  Add another service definition to the `docker-compose.yml` file for the Nginx proxy.


<details>
<summary> Hints (click to expand)</summary>

1. Ensure the `requirements.txt` file is in the same directory as the `Dockerfile` when copying it.
2. Double-check the syntax in your `docker-compose.yml` file, especially indentation.
3. If the health check fails, verify that the application is running correctly within the container.
4. If the build fails, carefully check the logs for errors in the pip install or other build steps.

</details>


<details>
<summary>✅ Solution Notes (spoiler)</summary>

The solution involves creating a simple Flask application, then building a naive Docker image. The key is then refactoring the Dockerfile to use a multi-stage build. This significantly reduces the final image size by only including the necessary runtime components. Docker Compose is then used to orchestrate the container, including a health check to ensure the application's availability. The final optional step suggests further avenues for optimization.

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
