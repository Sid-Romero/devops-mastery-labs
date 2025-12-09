# Lab 01: Multi-stage Node.js Build

## 🎯 Objectives

Learn how to create efficient Docker images using multi-stage builds. Reduce image size and improve security by separating build and runtime environments.

## 📚 Concepts Covered

- Multi-stage Docker builds
- Layer optimization
- Build vs runtime dependencies
- Image size reduction techniques

## 📋 Prerequisites

- Docker installed and running
- Basic knowledge of Node.js
- Understanding of Dockerfile syntax

## 🔨 Task Description

Create a multi-stage Dockerfile for a Node.js application that:

1. Uses a build stage to install dependencies and build the application
2. Uses a minimal runtime stage for the final image
3. Reduces the final image size by at least 50% compared to a single-stage build
4. Excludes development dependencies from the production image

## 🎓 Learning Goals

- Understand the benefits of multi-stage builds
- Learn how to optimize Docker layer caching
- Practice separating build-time and runtime dependencies
- Minimize attack surface by reducing image size

## 📁 Project Structure

```
lab-01-multistage-node/
├── README.md (this file)
├── app/ (your work goes here)
└── solution/ (reference solution - try not to peek!)
```

## 🚀 Getting Started

1. Navigate to the `app/` directory
2. Create a simple Node.js application (or use the provided starter)
3. Create a multi-stage Dockerfile
4. Build and run your container
5. Compare image sizes using `docker images`

## ✅ Validation Criteria

Your solution should:

- [ ] Use at least 2 stages in the Dockerfile
- [ ] Build stage uses `node:alpine` or similar for installation
- [ ] Runtime stage uses a minimal base image
- [ ] Production image does NOT contain devDependencies
- [ ] Final image size is < 200MB (for a basic app)
- [ ] Application runs successfully in the container
- [ ] Container exposes the correct port
- [ ] Health check endpoint responds correctly

## 🔍 Verification Commands

```bash
# Build the image
docker build -t lab01-node-app .

# Check image size
docker images lab01-node-app

# Run the container
docker run -p 3000:3000 lab01-node-app

# Test the application
curl http://localhost:3000
```

## 💡 Hints

- Consider using `node:alpine` for smaller base images
- Use `.dockerignore` to exclude unnecessary files
- Copy only necessary files between stages
- Consider using `npm ci` instead of `npm install` for production
- Order Dockerfile instructions from least to most frequently changing

## 🎁 Bonus Challenges

1. Implement a health check in the Dockerfile
2. Add labels for better image management
3. Use build arguments for flexibility
4. Implement a development-specific build stage

## 📖 Resources

- [Docker Multi-stage Builds](https://docs.docker.com/develop/develop-images/multistage-build/)
- [Node.js Docker Best Practices](https://github.com/nodejs/docker-node/blob/main/docs/BestPractices.md)
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

## 🔗 Next Steps

Once you've completed this lab, move on to:
- **Lab 02**: Python Environment & Secrets Management

## 📝 Notes

- The solution directory contains a reference implementation
- Try to solve the lab independently before checking the solution
- Compare your approach with the solution to learn different techniques
