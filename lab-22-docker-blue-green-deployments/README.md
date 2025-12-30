# Lab 22: Docker: Implementing Blue/Green Deployments

![Difficulty: Medium](https://img.shields.io/badge/Difficulty-Medium-yellow) ![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

> **Auto-generated lab** - Created on 2025-12-30

## Description

Learn how to implement a blue/green deployment strategy using Docker. This lab guides you through building two identical application environments (blue and green) and switching traffic between them for seamless updates.

## Learning Objectives

- Understand the blue/green deployment strategy.
- Create Docker images for application versions.
- Deploy and manage multiple application containers.
- Switch traffic between different application versions using Docker networking.

## Prerequisites

- Docker installed and running
- Basic understanding of Docker commands
- Text editor (e.g., VS Code, Sublime Text)

## Lab Steps

### Step 1: Step 1: Create a Simple Application

Let's start by creating a basic application. For simplicity, we'll use a simple Python Flask app that displays a version number. Create a file named `app.py` with the following content:

```python
from flask import Flask
import os

app = Flask(__name__)

VERSION = os.getenv('VERSION', '1.0')

@app.route('/')
def hello_world():
    return f'Hello, World! Version: {VERSION}'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

Next, create a `requirements.txt` file to specify the application's dependencies:

```
Flask
```

Finally, create a `Dockerfile` to package the application into a Docker image.  This Dockerfile should install python, copy the requirements and source, and then execute the flask application.

### Step 2: Step 2: Build Docker Images for Blue and Green Versions

Now, let's build Docker images for two versions of our application. First, build the 'blue' version (v1):

```bash
docker build -t myapp:blue .
```

Next, modify the `app.py` file to represent the 'green' version (v2). Change the `VERSION` variable:

```python
VERSION = os.getenv('VERSION', '2.0')
```

Now, build the 'green' version:

```bash
docker build -t myapp:green .
```

Verify that both images have been created:

```bash
docker images
```

You should see `myapp:blue` and `myapp:green` in the list.

### Step 3: Step 3: Create a Docker Network

Create a Docker network that will allow us to easily switch traffic between the blue and green containers. This network will allow for easy communication and isolation.

```bash
docker network create mynetwork
```

Verify that the network has been created:

```bash
docker network ls
```

### Step 4: Step 4: Run the Blue and Green Containers

Run both the 'blue' and 'green' containers, connecting them to the `mynetwork` network. Expose port 5000 for both. Ensure to set the `VERSION` environment variable.

```bash
docker run -d --name myapp-blue --network mynetwork -p 5000:5000 -e VERSION=1.0 myapp:blue
docker run -d --name myapp-green --network mynetwork -p 5001:5000 -e VERSION=2.0 myapp:green
```

Verify that both containers are running:

```bash
docker ps
```

You should see `myapp-blue` and `myapp-green` running.

### Step 5: Step 5: Create a Load Balancer (Simple Nginx)

To switch traffic between the blue and green containers, we'll use a simple Nginx load balancer. Create an `nginx.conf` file with the following content:

```nginx
events {}

http {
    upstream myapp {
        server myapp-blue:5000;
    }

    server {
        listen 80;

        location / {
            proxy_pass http://myapp;
        }
    }
}
```

Create a `Dockerfile` for the Nginx load balancer:

```dockerfile
FROM nginx:latest
COPY nginx.conf /etc/nginx/nginx.conf
```

Build the Nginx image:

```bash
docker build -t mynginx .
```

Run the Nginx container, connecting it to the `mynetwork` network:

```bash
docker run -d --name mynginx -p 80:80 --network mynetwork mynginx
```

Verify that the Nginx container is running:

```bash
docker ps
```

Access the application in your browser at `http://localhost`. You should see 'Hello, World! Version: 1.0' (the blue version).

### Step 6: Step 6: Switch Traffic to the Green Version

To switch traffic to the 'green' version, modify the `nginx.conf` file to point to `myapp-green:5000`:

```nginx
events {}

http {
    upstream myapp {
        server myapp-green:5000;
    }

    server {
        listen 80;

        location / {
            proxy_pass http://myapp;
        }
    }
}
```

Rebuild the Nginx image:

```bash
docker build -t mynginx .
```

Stop and remove the existing Nginx container:

```bash
docker stop mynginx
docker rm mynginx
```

Run the new Nginx container:

```bash
docker run -d --name mynginx -p 80:80 --network mynetwork mynginx
```

Access the application in your browser at `http://localhost`. You should now see 'Hello, World! Version: 2.0' (the green version). You have successfully switched traffic between the blue and green deployments.


<details>
<summary> Hints (click to expand)</summary>

1. Ensure that the Docker network is created before running the containers.
2. Double-check the port mappings and network connections in the `docker run` commands.
3. Verify the Nginx configuration file for correct upstream server definitions.
4. Use `docker logs <container_id>` to troubleshoot any issues with the containers.

</details>


<details>
<summary>✅ Solution Notes (spoiler)</summary>

The solution involves creating two identical application environments (blue and green) using Docker, deploying them with different versions, and switching traffic between them using a simple Nginx load balancer. This approach minimizes downtime during application updates and allows for easy rollback if necessary.

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
