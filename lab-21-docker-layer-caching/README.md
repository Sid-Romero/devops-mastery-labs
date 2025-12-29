# Lab 21: Docker Layer Caching for Faster Builds

![Difficulty: Medium](https://img.shields.io/badge/Difficulty-Medium-yellow) ![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

> **Auto-generated lab** - Created on 2025-12-29

## Description

This lab explores Docker layer caching to significantly speed up build times. You'll learn how to structure your Dockerfile to leverage caching effectively and avoid invalidating layers unnecessarily.

## Learning Objectives

- Understand how Docker layer caching works
- Optimize Dockerfiles for efficient caching
- Identify common causes of cache invalidation
- Improve build times using layer caching best practices

## Prerequisites

- Docker installed and running
- Basic understanding of Dockerfiles
- A text editor

## Lab Steps

### Step 1: Create a Sample Application

Let's simulate a simple Node.js application. Create a directory named `caching-demo`, and inside it, create two files: `package.json` and `index.js`.

```bash
mkdir caching-demo
cd caching-demo
touch package.json index.js
```

Populate `package.json` with the following:

```json
{
  "name": "caching-demo",
  "version": "1.0.0",
  "description": "A simple Node.js app",
  "main": "index.js",
  "scripts": {
    "start": "node index.js"
  },
  "dependencies": {
    "express": "^4.17.1"
  }
}
```

And `index.js` with:

```javascript
const express = require('express')
const app = express()
const port = 3000

app.get('/', (req, res) => {
  res.send('Hello World!')
})

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})
```

### Step 2: Create a Basic Dockerfile

Now, create a `Dockerfile` in the same directory with the following content. This is a naive first attempt, and we will optimize it later.

```dockerfile
FROM node:16

WORKDIR /app

COPY package*.json .
RUN npm install

COPY . .

EXPOSE 3000
CMD ["npm", "start"]
```

### Step 3: Build and Run the Initial Docker Image

Build the image using the following command:

```bash
docker build -t caching-demo .
```

Run the container:

```bash
docker run -p 3000:3000 caching-demo
```

Access the application in your browser at `http://localhost:3000`.  Stop the container once you confirm it works.

Now, run the `docker build` command again. Observe the output.  Docker uses the cached layers from the previous build. Note the `Using cache` lines.

### Step 4: Modify the Application Code

Modify `index.js` by changing the greeting:

```javascript
const express = require('express')
const app = express()
const port = 3000

app.get('/', (req, res) => {
  res.send('Hello Docker Caching!')
})

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})
```

Run `docker build` again. Notice that the `COPY . .` step and subsequent steps are re-executed. This is because the `COPY` command copies *all* files, and a change to *any* file invalidates the cache for that layer and all subsequent layers.

### Step 5: Optimize the Dockerfile for Caching

Modify the `Dockerfile` to optimize for caching.  The key is to copy `package.json` and install dependencies *before* copying the rest of the application code. This allows Docker to cache the `npm install` layer unless `package.json` or `package-lock.json` changes.

```dockerfile
FROM node:16

WORKDIR /app

COPY package*.json .
RUN npm install --only=production

COPY . .

EXPOSE 3000
CMD ["npm", "start"]
```

Note the `--only=production` flag. This further speeds up caching by only installing production dependencies. Development dependencies will be installed during development (outside of the container). This also reduces the size of the final image.

Now, build the image again:

```bash
docker build -t caching-demo .
```

Notice that only the last `COPY` step is re-executed. The `npm install` layer is cached.

Modify `index.js` again and rebuild. The `npm install` layer remains cached, significantly reducing build time.

### Step 6: Further Optimization: .dockerignore

Create a `.dockerignore` file to exclude unnecessary files from being copied into the image. This can further improve build times and reduce image size.  For example, you might want to exclude `node_modules` (since they're installed inside the container) and any local development files.

```
touch .dockerignore
```

Add the following to `.dockerignore`:

```
node_modules
.git
.DS_Store
```

Rebuild the image. Although the visible impact might be small in this example, in larger projects, a well-configured `.dockerignore` file can significantly improve build performance by reducing the amount of data that needs to be copied and processed during the build.


<details>
<summary> Hints (click to expand)</summary>

1. Pay close attention to the order of commands in your Dockerfile.  Commands that change frequently should be placed later in the file.
2. Use the `--no-cache` flag with `docker build` to force a rebuild from scratch, bypassing the cache.
3. Make sure to include necessary files in your `.dockerignore` file to prevent them from being copied into the image.

</details>


<details>
<summary>✅ Solution Notes (spoiler)</summary>

The key to solving this lab is understanding that Docker builds images in layers, and each instruction in the Dockerfile creates a new layer.  If a layer's content changes, all subsequent layers must be rebuilt. By ordering the commands to copy frequently-changing files (like application code) *after* copying less-frequently-changing files (like `package.json`), you can maximize cache reuse and minimize build times. The `.dockerignore` file further optimizes the build by preventing unnecessary files from being copied into the image.

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
