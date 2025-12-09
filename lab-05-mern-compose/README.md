# Lab 05: MERN Stack with Compose

## 🎯 Objectives

Orchestrate a complete MERN (MongoDB, Express, React, Node.js) stack using Docker Compose, demonstrating multi-container application deployment.

## 📚 Concepts Covered

- Docker Compose orchestration
- Multi-container applications
- Service dependencies
- Health checks
- Environment configuration
- Development vs production setups
- Full-stack application deployment

## 📋 Prerequisites

- Completed Labs 01-04 or equivalent Docker knowledge
- Basic understanding of MongoDB, Express, React, and Node.js
- Familiarity with Docker Compose

## 🔨 Task Description

Create a complete MERN stack application with Docker Compose that:

1. Runs MongoDB, Express backend, and React frontend as separate services
2. Implements proper service dependencies and startup order
3. Uses environment variables for configuration
4. Implements health checks for all services
5. Supports both development and production modes
6. Includes data persistence for MongoDB

## 🎓 Learning Goals

- Master Docker Compose for multi-container orchestration
- Understand service dependencies and startup sequencing
- Learn to configure full-stack applications with containers
- Practice building integrated development environments
- Implement production-ready container configurations

## 📁 Project Structure

```
lab-05-mern-compose/
├── README.md (this file)
└── stack/
    ├── docker-compose.yml
    ├── frontend/
    │   ├── Dockerfile
    │   └── src/
    ├── backend/
    │   ├── Dockerfile
    │   └── src/
    └── mongodb/
        └── init-scripts/
```

## 🚀 Getting Started

1. Set up the project structure in the `stack/` directory
2. Create Dockerfiles for frontend and backend
3. Create a docker-compose.yml orchestrating all services
4. Configure environment variables and networking
5. Implement health checks for service readiness
6. Test the complete stack

## ✅ Validation Criteria

Your solution should:

- [ ] All services defined in docker-compose.yml
- [ ] Frontend (React) builds and serves correctly
- [ ] Backend (Express) connects to MongoDB
- [ ] MongoDB uses a persistent volume
- [ ] Services start in correct order using depends_on
- [ ] Health checks implemented for all services
- [ ] Environment variables used for configuration
- [ ] Frontend can communicate with backend API
- [ ] Backend can read/write to MongoDB
- [ ] Development mode supports hot-reload
- [ ] Production mode uses optimized builds

## 🔍 Verification Commands

```bash
# Start the stack
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f

# Check specific service logs
docker-compose logs backend

# Test frontend
curl http://localhost:3000

# Test backend API
curl http://localhost:5000/api/health

# Access MongoDB
docker-compose exec mongodb mongosh

# Restart specific service
docker-compose restart backend

# Scale services (if stateless)
docker-compose up -d --scale backend=3

# Stop the stack
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## 💡 Hints

- Use `depends_on` to define service dependencies (note: this only controls startup order, not readiness)
- Implement health check endpoints in your backend API
- Use separate Dockerfiles for dev and production (Dockerfile.dev, Dockerfile.prod)
- Consider using `docker-compose.override.yml` for local development settings
- Use `.env` file for environment variable management
- Implement graceful shutdown handlers in your services
- Use MongoDB initialization scripts for schema setup

## 🎁 Bonus Challenges

1. Add nginx as a reverse proxy
2. Implement Redis for session management or caching
3. Add a worker service for background jobs
4. Create separate compose files for dev/staging/prod
5. Implement container-to-container logging aggregation
6. Add automated testing services to the stack
7. Implement a CI/CD pipeline using the compose setup
8. Add monitoring with Prometheus and Grafana

## 📖 Resources

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Compose File Reference](https://docs.docker.com/compose/compose-file/)
- [React with Docker](https://create-react-app.dev/docs/deployment/#docker)
- [Express Best Practices](https://expressjs.com/en/advanced/best-practice-production.html)
- [MongoDB Docker Image](https://hub.docker.com/_/mongo)

## 🔗 Next Steps

Congratulations on completing the beginner labs! Continue to:
- **Lab 06**: Advanced intermediate topics
- Review your solutions and optimize for production
- Explore Kubernetes for container orchestration at scale

## 📝 Notes

- This lab combines concepts from Labs 01-04
- Focus on service orchestration and dependencies
- Document your setup for team members
- Consider creating separate configurations for different environments
- Test failure scenarios (e.g., what happens if MongoDB crashes?)
