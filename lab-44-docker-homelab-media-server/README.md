# Lab 44: Docker Homelab: Media Server with Persistent Data

![Difficulty: Easy](https://img.shields.io/badge/Difficulty-Easy-brightgreen) ![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

> **Auto-generated lab** - Created on 2026-01-02

## Description

This lab simulates deploying a simple media server using Docker, focusing on persistent data storage and basic Docker Compose setup. You will learn how to create a Dockerfile, define a Docker Compose configuration, and manage persistent volumes for your media files.

## Learning Objectives

- Create a Dockerfile for a simple media server application.
- Define a Docker Compose configuration to orchestrate the media server and a persistent volume.
- Understand how to map host directories to container volumes for persistent data.
- Start, stop, and manage Docker containers using Docker Compose.

## Prerequisites

- Docker installed and running on your local machine (Docker Desktop, etc.)
- Basic understanding of Docker concepts (images, containers, volumes)
- Text editor for creating files

## Lab Steps

### Step 1: Step 1: Create a Project Directory

Create a new directory for your project. This will house all the files needed for the lab.

```bash
mkdir docker-media-server
cd docker-media-server
```

### Step 2: Step 2: Create a Simple Media Server Dockerfile

Create a file named `Dockerfile` in your project directory. This file will define how your media server image is built.

```dockerfile
# Use a lightweight base image
FROM nginx:alpine

# Copy a simple HTML file to serve as a placeholder
COPY index.html /usr/share/nginx/html/

# Expose port 80
EXPOSE 80

# Command to start nginx
CMD ["nginx", "-g", "daemon off;"]
```

Now, create a simple `index.html` file in the same directory:

```html
<!DOCTYPE html>
<html>
<head>
    <title>My Media Server</title>
</head>
<body>
    <h1>Welcome to my media server!</h1>
    <p>This is a placeholder. Add your media here.</p>
</body>
</html>
```

### Step 3: Step 3: Define a Docker Compose Configuration

Create a file named `docker-compose.yml` in your project directory. This file will define the services and volumes for your media server.

```yaml
version: '3.8'

services:
  media-server:
    build: .
    ports:
      - "8080:80"
    volumes:
      - media-volume:/usr/share/nginx/html/media

volumes:
  media-volume:
```

This configuration does the following:

*   Defines a service named `media-server`.
*   Specifies that the image should be built from the `Dockerfile` in the current directory (`.`).
*   Maps port 8080 on your host machine to port 80 on the container.
*   Creates a named volume `media-volume` and mounts it to `/usr/share/nginx/html/media` inside the container.  This is where you would store your media files.

Create a directory on your host machine that will be mapped to the volume. This will hold the media files.

```bash
mkdir media
```

Now modify the `docker-compose.yml` file to map the local `media` directory to the `media-volume`:

```yaml
version: '3.8'

services:
  media-server:
    build: .
    ports:
      - "8080:80"
    volumes:
      - ./media:/usr/share/nginx/html/media

```

Remove the named volume definition.


### Step 4: Step 4: Start the Media Server

Start the media server using Docker Compose.

```bash
docker-compose up -d
```

This command will build the image (if it doesn't exist) and start the container in detached mode (`-d`).

### Step 5: Step 5: Access the Media Server

Open your web browser and navigate to `http://localhost:8080`. You should see the placeholder HTML page.

Now, add some files (e.g., images, videos) to the `media` directory on your host machine.  These files will be accessible inside the container at `/usr/share/nginx/html/media`. You may need to adjust the nginx configuration to properly serve these files.

To see the files, you could modify the `index.html` to include links to the media files. For example:

```html
<!DOCTYPE html>
<html>
<head>
    <title>My Media Server</title>
</head>
<body>
    <h1>Welcome to my media server!</h1>
    <p>This is a placeholder. Add your media here.</p>
    <h2>Media Files:</h2>
    <ul>
        <li><a href="media/image.jpg">Image</a></li>
    </ul>
</body>
</html>
```

(Assuming you placed a file named `image.jpg` inside the `media` directory)

Restart the container to see the changes:

```bash
docker-compose restart
```

### Step 6: Step 6: Stop and Remove the Media Server

Stop and remove the media server using Docker Compose.

```bash
docker-compose down
```

This command will stop and remove the container and the network created by Docker Compose.  The volume (and the data within it) will persist.


<details>
<summary> Hints (click to expand)</summary>

1. Make sure your Dockerfile correctly copies the `index.html` file.
2. Ensure the ports in your `docker-compose.yml` file are mapped correctly.
3. Verify that the volume is mounted correctly by checking the container's file system.
4. If you're having trouble accessing the media server, check your firewall settings.

</details>


<details>
<summary>✅ Solution Notes (spoiler)</summary>

The solution involves creating a Dockerfile that uses nginx to serve static files. A docker-compose.yml file defines the service, maps ports, and mounts a volume to persist the media files. The key is understanding how the volume mapping allows the container to access files on the host machine, ensuring data persistence.

</details>


---

## Notes

- **Difficulty:** Easy
- **Estimated time:** 30-45 minutes
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
