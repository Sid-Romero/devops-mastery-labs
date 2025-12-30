# Lab 23: Docker Multi-Agent Research Environment

![Difficulty: Medium](https://img.shields.io/badge/Difficulty-Medium-yellow) ![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

> **Auto-generated lab** - Created on 2025-12-30

## Description

This lab demonstrates how to containerize a simplified multi-agent research environment using Docker. It focuses on creating separate containers for different agent types and using Docker networking to enable communication between them.

## Learning Objectives

- Learn to define multiple services in a Docker Compose file.
- Understand how to create custom Dockerfiles for different agent types.
- Explore Docker networking to facilitate inter-container communication.
- Apply Docker volume mounts for persistent data storage and code sharing.

## Prerequisites

- Docker installed and running
- Docker Compose installed
- Basic understanding of Docker concepts (images, containers, networking)

## Lab Steps

### Step 1: Create Project Directory and Base Files

Create a new directory for your project and navigate into it.

```bash
mkdir multi-agent-research
cd multi-agent-research
```

Create the following files:

*   `docker-compose.yml` (for defining the services)
*   `agent1/Dockerfile` (for building the first agent's image)
*   `agent2/Dockerfile` (for building the second agent's image)
*   `agent1/app.py` (a simple Python script for agent 1)
*   `agent2/app.py` (a simple Python script for agent 2)
*   `data/` (an empty directory for volume mounting)

```bash
mkdir agent1 agent2 data
touch docker-compose.yml agent1/Dockerfile agent2/Dockerfile agent1/app.py agent2/app.py
```

### Step 2: Define Agent 1 Dockerfile

Create a `Dockerfile` for the first agent (`agent1/Dockerfile`). This file will define the steps to build the agent's container image.

```dockerfile
# agent1/Dockerfile
FROM python:3.9-slim-buster

WORKDIR /app

COPY agent1/app.py .

RUN pip install --no-cache-dir flask

CMD ["python", "app.py"]
```

### Step 3: Define Agent 2 Dockerfile

Create a `Dockerfile` for the second agent (`agent2/Dockerfile`). This file will define the steps to build the agent's container image. This agent will have a slightly different dependency.

```dockerfile
# agent2/Dockerfile
FROM python:3.9-slim-buster

WORKDIR /app

COPY agent2/app.py .

RUN pip install --no-cache-dir requests

CMD ["python", "app.py"]
```

### Step 4: Create Agent Python Scripts

Create simple Python scripts for each agent. These scripts will simulate the agents' behavior.

```python
# agent1/app.py
from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    return f'Hello from Agent 1! Data dir content: {os.listdir("/data")}'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
```

```python
# agent2/app.py
import requests
import os

def main():
    agent1_url = os.environ.get("AGENT1_URL", "http://agent1:5000")
    try:
        response = requests.get(agent1_url)
        print(f"Agent 2 calling Agent 1: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error calling Agent 1: {e}")

if __name__ == "__main__":
    main()
```

### Step 5: Define Docker Compose File

Create a `docker-compose.yml` file to define the services (agents) and their configurations.

```yaml
# docker-compose.yml
version: '3.8'

services:
  agent1:
    build:
      context: .
      dockerfile: agent1/Dockerfile
    ports:
      - "5000:5000"
    volumes:
      - ./data:/data
    networks:
      - research-network

  agent2:
    build:
      context: .
      dockerfile: agent2/Dockerfile
    depends_on:
      - agent1
    environment:
      AGENT1_URL: http://agent1:5000
    networks:
      - research-network
    command: python app.py

networks:
  research-network:
```

### Step 6: Run the Docker Compose Environment

Start the services using Docker Compose.

```bash
docker-compose up --build
```

This command will build the images and start the containers.  Monitor the logs to see the agents interacting.

### Step 7: Test the Application

Open your web browser and navigate to `http://localhost:5000`. You should see "Hello from Agent 1!".

Also, observe the logs of `agent2`. It should be printing the response it receives from `agent1`.

Try creating a file in the `data/` directory on your host machine.  Observe that it is visible within the `agent1` container by looking at the output of `http://localhost:5000`.

### Step 8: Clean Up

Stop and remove the containers and network.

```bash
docker-compose down
```


<details>
<summary> Hints (click to expand)</summary>

1. Ensure Docker Desktop (or similar) is running before starting the lab.
2. Check your Dockerfile syntax carefully; small errors can cause build failures.
3. Use `docker-compose logs` to debug any issues with the running containers.
4. If agent2 cannot connect to agent1, ensure that the `AGENT1_URL` environment variable is correctly set.
5. Make sure the Docker context is set correctly when building the images. In this lab, the context is the root directory of the project.

</details>


<details>
<summary>✅ Solution Notes (spoiler)</summary>

The lab creates two Docker containers, each representing a different agent. Agent 1 runs a simple Flask web server, and Agent 2 makes requests to Agent 1. Docker Compose is used to define and manage the services, and a custom Docker network facilitates communication between the containers. A volume mount is used to share data between the host machine and Agent 1.

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
