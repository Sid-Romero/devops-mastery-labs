# Lab 52: Docker Android Emulator with noVNC

![Difficulty: Medium](https://img.shields.io/badge/Difficulty-Medium-yellow) ![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

> **Auto-generated lab** - Created on 2026-01-06

## Description

This lab guides you through creating a Docker container running an Android emulator with noVNC for remote access. You'll learn how to build a custom Docker image, configure the emulator, and access it through a web browser.

## Learning Objectives

- Build a Docker image with an Android emulator.
- Configure the Android emulator to be accessible via noVNC.
- Access the Android emulator remotely through a web browser.
- Understand Dockerfile instructions and Docker Compose.

## Prerequisites

- Docker installed and running
- Basic understanding of Docker concepts (images, containers)
- A text editor

## Lab Steps

### Step 1: Create Project Directory

Create a new directory for your project:

```bash
mkdir docker-android-emulator
cd docker-android-emulator
```

### Step 2: Create Dockerfile

Create a `Dockerfile` in your project directory. This file will define the steps to build your Docker image.

```bash
touch Dockerfile
```

Open the `Dockerfile` in your text editor and add the following content.  You might need to adjust the `ANDROID_SDK_ROOT` and emulator download URL based on the latest versions.

```dockerfile
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    openjdk-8-jdk \
    xvfb \
    x11vnc \
    websockify \
    curl \
    git \
    libxkbcommon-x11-0 \
    --no-install-recommends

# Download and install Android SDK Command Line Tools
ENV ANDROID_SDK_ROOT /opt/android-sdk
RUN mkdir -p ${ANDROID_SDK_ROOT}

RUN wget -q https://dl.google.com/android/repository/commandlinetools-linux-7302050_latest.zip -O /tmp/android-sdk.zip \
    && unzip /tmp/android-sdk.zip -d ${ANDROID_SDK_ROOT}

ENV PATH ${ANDROID_SDK_ROOT}/cmdline-tools/latest/bin:${ANDROID_SDK_ROOT}/platform-tools:${PATH}

# Install necessary SDK components
RUN yes | sdkmanager --sdk_root=${ANDROID_SDK_ROOT} "platforms;android-30" \
    && yes | sdkmanager --sdk_root=${ANDROID_SDK_ROOT} "platform-tools" \
    && yes | sdkmanager --sdk_root=${ANDROID_SDK_ROOT} "system-images;android-30;google_apis;x86_64"

# Create and configure AVD (Android Virtual Device)
RUN avdmanager --sdk_root=${ANDROID_SDK_ROOT} create avd -n Pixel_API_30 -k "system-images;android-30;google_apis;x86_64" -f

# Expose noVNC port
EXPOSE 6080

# Start script
COPY start.sh /

CMD ["/start.sh"]
```

### Step 3: Create start.sh

Create a `start.sh` file in your project directory. This script will start the Android emulator and noVNC.

```bash
touch start.sh
chmod +x start.sh
```

Open the `start.sh` file in your text editor and add the following content:

```bash
#!/bin/bash

export ANDROID_SDK_ROOT=/opt/android-sdk
export PATH=$ANDROID_SDK_ROOT/platform-tools:$PATH

# Start the Android emulator in the background
emulator -avd Pixel_API_30 -no-window -no-audio -camera-back none -gpu swiftshader &

# Wait for the emulator to start
sleep 30

# Start x11vnc
x11vnc -display :0 -nopw -listen 0.0.0.0 -forever &

# Start noVNC
websockify -v --web=/usr/share/novnc 6080 localhost:5900
```

**Important Note:** The `sleep 30` is a simple way to wait for the emulator to start.  A more robust solution would involve checking for the emulator's process or log output. Also, you might need to install `novnc` with `apt-get install novnc` in your Dockerfile if it's not available in `/usr/share/novnc`.

### Step 4: Create docker-compose.yml (Optional)

You can use `docker-compose.yml` to simplify running the container.

```bash
touch docker-compose.yml
```

Open the `docker-compose.yml` in your text editor and add the following content:

```yaml
version: '3.8'
services:
  android:
    build: .
    ports:
      - "6080:6080"
    volumes:
      - android_data:/root/.android

volumes:
  android_data:
```

### Step 5: Build and Run the Docker Image

Build the Docker image. If you're using Docker Compose, run `docker-compose up --build`. Otherwise, run the following commands:

```bash
docker build -t android-emulator .
```

Then, run the container:

```bash
docker run -d -p 6080:6080 android-emulator
```

If you are using docker compose, you can skip the docker build command and just use `docker-compose up --build`.

### Step 6: Access the Android Emulator

Open your web browser and navigate to `http://localhost:6080`. You should see the noVNC interface connected to the Android emulator.  It may take several minutes for the emulator to fully boot.

If you are using a remote server, replace `localhost` with the server's IP address or hostname.

### Step 7: Stopping the Container

To stop the container, you can use the following command. First find the container ID:

```bash
docker ps
```
Then stop the container:

```bash
docker stop <container_id>
```

If using Docker Compose, you can use `docker-compose down`.


<details>
<summary> Hints (click to expand)</summary>

1. Make sure your CPU supports virtualization.  You might need to enable it in your BIOS settings.
2. The emulator can take a long time to boot up. Be patient.
3. If you encounter issues with the emulator, check the container logs using `docker logs <container_id>`.
4. Ensure the port 6080 is not already in use on your host machine.
5. Double-check the Android SDK download URL in the Dockerfile. It might need updating.
6. If noVNC doesn't connect, ensure x11vnc is running correctly inside the container by inspecting the container logs.

</details>


<details>
<summary>✅ Solution Notes (spoiler)</summary>

The solution involves creating a Dockerfile that installs the necessary dependencies, including the Android SDK, emulator, and noVNC. The `start.sh` script launches the emulator and noVNC. Docker Compose provides a convenient way to build and run the container. The key is to ensure all dependencies are correctly installed and configured within the Docker image, and the emulator is given sufficient time to initialize before attempting to connect with noVNC.

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
