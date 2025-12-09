# Lab 04: Network Isolation

## 🎯 Objectives

Master Docker networking by creating isolated networks and understanding container communication patterns.

## 📚 Concepts Covered

- Docker networks
- Bridge networks
- Network isolation
- Container DNS
- Service discovery
- Port mapping vs network connectivity
- Network security

## 📋 Prerequisites

- Completed Labs 01-03 or equivalent Docker knowledge
- Understanding of basic networking concepts
- Familiarity with Docker Compose

## 🔨 Task Description

Create a multi-service application with proper network isolation that:

1. Uses multiple Docker networks for service isolation
2. Implements a frontend, backend, and database architecture
3. Restricts communication between services based on roles
4. Demonstrates container DNS and service discovery
5. Shows both internal and external network access patterns

## 🎓 Learning Goals

- Understand Docker's networking model
- Learn to design secure network architectures
- Practice service isolation and segmentation
- Master container-to-container communication
- Implement zero-trust networking principles

## 📁 Project Structure

```
lab-04-network-isolation/
├── README.md (this file)
└── services/ (your services go here)
    ├── frontend/
    ├── backend/
    └── database/
```

## 🚀 Getting Started

1. Design a network architecture with frontend, backend, and database networks
2. Create Docker Compose configuration with multiple networks
3. Implement services that communicate across networks
4. Test network isolation using connectivity tests
5. Document network security boundaries

## ✅ Validation Criteria

Your solution should:

- [ ] Uses at least 2 custom Docker networks
- [ ] Frontend can reach backend but NOT database directly
- [ ] Backend can reach both frontend and database
- [ ] Database is isolated from frontend
- [ ] Uses container names for service discovery
- [ ] No unnecessary ports exposed to host
- [ ] Implements proper network segmentation
- [ ] Documents network architecture diagram

## 🔍 Verification Commands

```bash
# Start services
docker-compose up -d

# List networks
docker network ls

# Inspect network
docker network inspect <network-name>

# Test connectivity from frontend
docker exec frontend-container ping backend-container

# Attempt connection from frontend to database (should fail)
docker exec frontend-container ping database-container

# Check network isolation
docker network inspect frontend-net | grep Containers
docker network inspect backend-net | grep Containers

# View network configuration
docker-compose config
```

## 💡 Hints

- Use `docker network create` or define networks in docker-compose.yml
- Services on the same network can communicate using container names
- Use `networks:` in docker-compose.yml to control service connectivity
- Bridge networks provide isolation by default
- Use `internal: true` for networks that don't need external access
- Consider using aliases for flexible service naming

## 🎁 Bonus Challenges

1. Implement a reverse proxy (nginx) on the frontend network
2. Add network policies for additional security
3. Create a monitoring service with access to all networks
4. Implement mTLS for service-to-service communication
5. Use overlay networks for multi-host networking
6. Add a jump host for debugging isolated services

## 📖 Resources

- [Docker Networking Overview](https://docs.docker.com/network/)
- [Docker Compose Networking](https://docs.docker.com/compose/networking/)
- [Bridge Networks](https://docs.docker.com/network/bridge/)
- [Network Security Best Practices](https://docs.docker.com/engine/security/security/#docker-daemon-attack-surface)

## 🔗 Next Steps

Once you've completed this lab, move on to:
- **Lab 05**: MERN Stack with Compose

## 📝 Notes

- Network isolation is a key security principle
- Minimize exposed ports to reduce attack surface
- Use internal networks for backend services
- Document your network architecture for team members
- Consider using network plugins for advanced scenarios
