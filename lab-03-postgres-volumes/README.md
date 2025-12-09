# Lab 03: PostgreSQL & Volumes

## 🎯 Objectives

Learn data persistence in Docker using volumes with a PostgreSQL database. Understand the importance of separating data from containers.

## 📚 Concepts Covered

- Docker volumes
- Data persistence
- Named volumes vs bind mounts
- Database initialization
- Data backup and restore
- Volume management

## 📋 Prerequisites

- Completed Labs 01-02 or equivalent Docker knowledge
- Basic understanding of databases
- SQL basics

## 🔨 Task Description

Create a PostgreSQL setup with Docker that:

1. Uses a named volume for data persistence
2. Survives container recreation and restarts
3. Implements database initialization scripts
4. Provides backup and restore capabilities
5. Demonstrates volume inspection and management

## 🎓 Learning Goals

- Understand container data lifecycle
- Learn when to use volumes vs bind mounts
- Practice database initialization in containers
- Implement backup strategies for containerized databases
- Master volume management commands

## 📁 Project Structure

```
lab-03-postgres-volumes/
├── README.md (this file)
└── data/ (initialization scripts go here)
```

## 🚀 Getting Started

1. Create a `docker-compose.yml` for PostgreSQL
2. Define a named volume for data persistence
3. Add initialization scripts in the `data/` directory
4. Test data persistence by recreating containers
5. Implement backup and restore procedures

## ✅ Validation Criteria

Your solution should:

- [ ] PostgreSQL uses a named Docker volume
- [ ] Data persists after `docker-compose down && docker-compose up`
- [ ] Database is initialized with custom schema/data
- [ ] Volume can be backed up and restored
- [ ] Uses environment variables for credentials
- [ ] Implements healthcheck for database readiness
- [ ] Documentation includes backup/restore procedures
- [ ] Data directory permissions are correct

## 🔍 Verification Commands

```bash
# Start PostgreSQL with volume
docker-compose up -d

# Connect to database
docker exec -it postgres-container psql -U postgres

# Create test data
# Recreate container
docker-compose down
docker-compose up -d

# Verify data persists
docker exec -it postgres-container psql -U postgres -c "SELECT * FROM test_table;"

# List volumes
docker volume ls

# Inspect volume
docker volume inspect <volume-name>

# Backup volume
docker run --rm -v <volume-name>:/data -v $(pwd):/backup alpine tar czf /backup/backup.tar.gz -C /data .

# Restore volume
docker run --rm -v <volume-name>:/data -v $(pwd):/backup alpine tar xzf /backup/backup.tar.gz -C /data
```

## 💡 Hints

- Use official PostgreSQL image from Docker Hub
- Place `.sql` files in `/docker-entrypoint-initdb.d/` for auto-initialization
- Named volumes are preferred over bind mounts for databases
- Use `PGDATA` environment variable to customize data location
- Consider using Docker Compose for easier management
- Always backup before major operations

## 🎁 Bonus Challenges

1. Implement automated backups using cron in a sidecar container
2. Create multiple databases with different volumes
3. Set up a PostgreSQL replica using volumes
4. Implement point-in-time recovery
5. Create a script to migrate data between volumes
6. Add pgAdmin for database management

## 📖 Resources

- [Docker Volumes](https://docs.docker.com/storage/volumes/)
- [PostgreSQL Docker Image](https://hub.docker.com/_/postgres)
- [Dockerfile Best Practices: Volumes](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#volume)
- [PostgreSQL Backup and Restore](https://www.postgresql.org/docs/current/backup.html)

## 🔗 Next Steps

Once you've completed this lab, move on to:
- **Lab 04**: Network Isolation

## 📝 Notes

- Volumes are independent of container lifecycle
- Always use volumes for production databases
- Bind mounts are useful for development but not recommended for production data
- Test your backup and restore procedures regularly
