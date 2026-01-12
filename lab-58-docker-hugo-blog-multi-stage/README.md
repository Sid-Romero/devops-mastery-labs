# Lab 58: Docker: Hugo Blog with Multi-Stage Build and Volume Mounts

![Difficulty: Medium](https://img.shields.io/badge/Difficulty-Medium-yellow) ![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

> **Auto-generated lab** - Created on 2026-01-12

## Description

This lab demonstrates building a Hugo blog using a multi-stage Dockerfile. It covers efficient image creation, volume mounting for development, and running the blog in a container.

## Learning Objectives

- Understand multi-stage Dockerfile builds.
- Learn to efficiently build a Hugo blog image.
- Practice volume mounting for local development.
- Run a Hugo blog inside a Docker container.

## Prerequisites

- Docker installed and running
- Basic understanding of Docker concepts
- Text editor for creating files

## Lab Steps

### Step 1: Create Project Directory

Create a new directory for your Hugo blog project:

```bash
mkdir hugo-blog
cd hugo-blog
```

Inside this directory, create three files: `Dockerfile`, `docker-compose.yml`, and `README.md`.  The content of these files will be defined in the subsequent steps.

### Step 2: Create a Hugo Site

Initialize a new Hugo site. This will create the basic structure for your blog.

```bash
docker run --rm -v $(pwd):/src klakegg/hugo new site /src
```

This command uses a temporary Docker container with the Hugo CLI to create a new site in the current directory (mounted as `/src`).

### Step 3: Design the Dockerfile

Create a `Dockerfile` with the following content. This Dockerfile uses a multi-stage build to efficiently build the Hugo blog.

```dockerfile
# Stage 1: Builder image
FROM klakegg/hugo:latest AS builder

WORKDIR /app

COPY . .

# Build the Hugo site
RUN hugo

# Stage 2: Final image (nginx)
FROM nginx:alpine

WORKDIR /usr/share/nginx/html

# Copy the built site from the builder stage
COPY --from=builder /app/public . 

# Optionally, customize the nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

**Explanation:**
*   **Stage 1 (builder):** Uses the `klakegg/hugo` image to build the Hugo site.
*   **Stage 2 (final):** Uses `nginx:alpine` to serve the static files. It copies the generated `public` directory from the builder stage.  A custom nginx configuration is optional, but allows for more control of the web server.

### Step 4: Create nginx Configuration (Optional)

Create an `nginx.conf` file in the root directory with the following content. This file customizes the Nginx configuration to serve the Hugo blog.  If you skip this step, the default nginx configuration will be used.

```nginx
server {
    listen 80;
    server_name localhost;

    root /usr/share/nginx/html;
    index index.html index.htm;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

### Step 5: Create docker-compose.yml

Create a `docker-compose.yml` file to define the services for the Hugo blog.

```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:80"
    volumes:
      - .:/app
    command: hugo server -D -b / -w --disableFastRender
```

**Explanation:**
*   **`build: .`:**  Tells Docker Compose to build an image from the `Dockerfile` in the current directory.
*   **`ports: - "8000:80"`:** Maps port 8000 on your host machine to port 80 inside the container (where Nginx is running).
*   **`volumes: - .:/app`:**  Mounts the current directory (your Hugo project) into the `/app` directory inside the container. This allows you to make changes to your Hugo content locally and see them reflected in the running container without rebuilding the image.
*   **`command: hugo server -D -b / -w --disableFastRender`:** Overrides the default command and runs the Hugo development server inside the container. The `-D` flag enables draft posts, `-b /` sets the base URL, `-w` enables the watcher, and `--disableFastRender` ensures accurate rendering during development.  This is only used during development.  When running for production, the static content built by the Dockerfile is served.

### Step 6: Run the Blog with Docker Compose

Start the Hugo blog using Docker Compose:

```bash
docker-compose up
```

This command will build the Docker image (if it doesn't exist) and start the container.  Open your web browser and navigate to `http://localhost:8000` to view your Hugo blog.  Any changes you make to your Hugo content locally will be automatically reflected in the browser due to the volume mount.

### Step 7: Stop the Container

To stop the container, run:

```bash
docker-compose down
```

This will stop and remove the container created by Docker Compose.


<details>
<summary> Hints (click to expand)</summary>

1. Make sure Docker Desktop is running before starting the lab.
2. Ensure the correct Hugo version is used in the builder image.
3. Double-check the volume mount path in `docker-compose.yml`.
4. If you are using a custom theme, ensure it is copied correctly in the Dockerfile.

</details>


<details>
<summary>✅ Solution Notes (spoiler)</summary>

The solution involves creating a multi-stage Dockerfile to build the Hugo blog efficiently and using Docker Compose to run the blog with volume mounts for local development. The first stage builds the Hugo site, and the second stage serves the static content with Nginx.

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
