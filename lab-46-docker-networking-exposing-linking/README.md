# Lab 46: Docker Networking: Exposing and Linking Containers

![Difficulty: Medium](https://img.shields.io/badge/Difficulty-Medium-yellow) ![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

> **Auto-generated lab** - Created on 2026-01-03

## Description

This lab explores Docker networking concepts, focusing on exposing container ports and linking containers together.  You'll build a simple web application with a database and learn how to connect them using Docker's networking features.

## Learning Objectives

- Understand Docker networking concepts
- Learn how to expose container ports to the host
- Learn how to link containers together for communication
- Build a multi-container application using Docker Compose

## Prerequisites

- Docker installed
- Docker Compose installed
- Basic understanding of Docker commands

## Lab Steps

### Step 1: Create a Simple Web Application

First, let's create a basic web application using Python and Flask. Create a directory named `webapp` and inside it, create a file named `app.py`:

```python
from flask import Flask
import os
import socket

app = Flask(__name__)

@app.route('/')
def hello():
    hostname = socket.gethostname()
    return f'Hello from {hostname}!\n'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
```

Next, create a `requirements.txt` file in the same directory to specify the dependencies:

```
Flask
```


### Step 2: Create a Dockerfile for the Web Application

Create a `Dockerfile` in the `webapp` directory:

```dockerfile
FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

This Dockerfile does the following:
1.  Uses a Python 3.9 base image.
2.  Sets the working directory to `/app`.
3.  Copies the `requirements.txt` file and installs the dependencies.
4.  Copies the application code.
5.  Exposes port 5000.
6.  Runs the application.


### Step 3: Build the Web Application Image

Navigate to the `webapp` directory and build the Docker image:

```bash
docker build -t webapp .
```

This command builds an image named `webapp` from the `Dockerfile` in the current directory.

### Step 4: Run the Web Application Container and Expose the Port

Run the `webapp` image and expose port 5000 to the host:

```bash
docker run -d -p 8000:5000 --name webapp-container webapp
```

This command does the following:
1.  `-d`: Runs the container in detached mode (in the background).
2.  `-p 8000:5000`: Maps port 8000 on the host to port 5000 on the container.
3.  `--name webapp-container`: Assigns the name `webapp-container` to the container.
4.  `webapp`: Specifies the image to use.

Now, open your web browser and go to `http://localhost:8000`. You should see the "Hello from ...!" message.

### Step 5: Create a Simple Database Service (using Docker Compose)

Create a `docker-compose.yml` file in the root directory (outside the `webapp` directory):

```yaml
version: '3.8'
services:
  db:
    image: postgres:13-alpine
    environment:
      POSTGRES_USER: example
      POSTGRES_PASSWORD: example
      POSTGRES_DB: example
    ports:
      - "5432:5432"

  web:
    build: ./webapp
    ports:
      - "8000:5000"
    depends_on:
      - db
    environment:
       DATABASE_URL: postgresql://example:example@db:5432/example
```

This `docker-compose.yml` file defines two services:
1.  `db`: A PostgreSQL database.
2.  `web`: The web application we created earlier.

Notice the `depends_on` directive, which ensures that the database container starts before the web application container.  Also, the `DATABASE_URL` environment variable is set so that the web app (if it were actually connecting to the database) could access the database service through the internal docker network. The `db` hostname resolves to the database container's IP address within the Docker network.

### Step 6: Run the Application using Docker Compose

Navigate to the directory containing the `docker-compose.yml` file and run the following command:

```bash
docker-compose up -d
```

This command builds and starts the services defined in the `docker-compose.yml` file.  Docker Compose automatically creates a network and links the containers together. Access the web application at `http://localhost:8000`.

To stop the application, run:

```bash
docker-compose down
```


<details>
<summary> Hints (click to expand)</summary>

1. Make sure Docker Desktop is running before starting
2. Check if the port 8000 is already in use by another application
3. If the web application cannot connect to the database, verify the database URL in the `docker-compose.yml` file.

</details>


<details>
<summary>✅ Solution Notes (spoiler)</summary>

This lab demonstrates how to expose ports from a Docker container to the host machine and how to link containers together using Docker Compose. The `docker-compose.yml` file simplifies the process of managing multi-container applications. The `depends_on` directive ensures that the database container starts before the web application container, and the Docker Compose creates a default network allowing containers to communicate using service names as hostnames.

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
