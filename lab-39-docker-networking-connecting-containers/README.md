# Lab 39: Docker Networking: Connecting Containers

![Difficulty: Medium](https://img.shields.io/badge/Difficulty-Medium-yellow) ![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

> **Auto-generated lab** - Created on 2026-01-01

## Description

This lab explores Docker's networking capabilities by creating a custom network and connecting multiple containers. You'll learn how to expose ports, link containers, and use Docker Compose for multi-container applications.

## Learning Objectives

- Understand Docker networking concepts.
- Create and manage Docker networks.
- Connect containers within a Docker network.
- Expose ports to access containerized applications.
- Use Docker Compose to define and run multi-container applications.

## Prerequisites

- Docker installed and running
- Basic understanding of Docker concepts (images, containers)

## Lab Steps

### Step 1: Step 1: Create a Custom Docker Network

First, create a custom Docker network to isolate our containers. This allows them to communicate with each other by name.

```bash
docker network create my-network
```

Verify the network was created:

```bash
docker network ls
```

You should see `my-network` listed.

### Step 2: Step 2: Create a Simple Web Application (Node.js)

Let's create a basic Node.js web application. Create a directory named `web-app` and create two files inside: `app.js` and `package.json`.

**app.js:**

```javascript
const http = require('http');

const hostname = '0.0.0.0';
const port = 3000;

const server = http.createServer((req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  res.end('Hello, World! from the web-app container\n');
});

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});
```

**package.json:**

```json
{
  "name": "web-app",
  "version": "1.0.0",
  "description": "Simple Node.js web app",
  "main": "app.js",
  "scripts": {
    "start": "node app.js"
  },
  "author": "",
  "license": "ISC"
}
```

### Step 3: Step 3: Dockerize the Web Application

Create a `Dockerfile` in the `web-app` directory:

```dockerfile
FROM node:16-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
```

Build the Docker image:

```bash
cd web-app
docker build -t web-app .
```

### Step 4: Step 4: Run the Web Application Container

Run the web application container and connect it to the `my-network` network.  We'll name the container `web-app-container`.

```bash
docker run -d --name web-app-container --network my-network -p 8080:3000 web-app
```

Test the application by accessing `http://localhost:8080` in your browser. You should see 'Hello, World! from the web-app container'.

**Note:** We are mapping port 8080 on the host to port 3000 inside the container.

### Step 5: Step 5: Create a Second Container (Alpine Linux)

Now, let's create a second container based on Alpine Linux. This container will be used to test network connectivity to the web application container.

```bash
docker run -it --name alpine-container --network my-network alpine sh
```

Inside the `alpine-container`, use `wget` to access the web application container by its container name (`web-app-container`):

```bash
apk update
apk add wget
wget http://web-app-container:3000
```

You should see the HTML content of the web application in the output.

### Step 6: Step 6: Clean Up

Stop and remove the containers and network:

```bash
docker stop web-app-container alpine-container
docker rm web-app-container alpine-container
docker network rm my-network
```

### Step 7: Step 7: Using Docker Compose (Optional)

For more complex applications, Docker Compose simplifies the process of defining and running multi-container applications. Create a file named `docker-compose.yml` in the root directory (outside the `web-app` directory):

```yaml
version: '3.8'
services:
  web-app:
    build: ./web-app
    ports:
      - "8080:3000"
    networks:
      - my-network

  alpine:
    image: alpine
    networks:
      - my-network
    stdin_open: true # Equivalent to -i
    tty: true        # Equivalent to -t
    depends_on:
      - web-app

networks:
  my-network:
```

Run the application using Docker Compose:

```bash
docker-compose up -d
```

Access the web application at `http://localhost:8080`.  To access the alpine container:

```bash
docker exec -it <alpine_container_id> sh
```

Then execute the `wget` command as described in step 5.

To stop and remove the containers:

```bash
docker-compose down
```


<details>
<summary> Hints (click to expand)</summary>

1. Make sure your Node.js application is listening on 0.0.0.0, not 127.0.0.1.
2. Double-check the port mappings in your `docker run` command.
3. If `wget` is not found in the Alpine container, you need to install it using `apk add wget`.
4. Ensure that the Docker network is created before running the containers.
5. Use `docker logs <container_name>` to troubleshoot container startup issues.

</details>


<details>
<summary>✅ Solution Notes (spoiler)</summary>

The solution involves creating a custom Docker network, building and running a Node.js web application container, and then running an Alpine Linux container to test network connectivity. The containers communicate using the container name as the hostname within the custom network. Docker Compose simplifies the process of defining and managing multi-container applications.

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
