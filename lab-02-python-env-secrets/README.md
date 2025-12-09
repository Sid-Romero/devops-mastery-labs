# Lab 02: Python Environment & Secrets

## 🎯 Objectives

Master the handling of environment variables, secrets, and configuration in Docker containers using Python applications.

## 📚 Concepts Covered

- Environment variable management
- Docker secrets
- Configuration best practices
- Secure credential handling
- Python environment isolation

## 📋 Prerequisites

- Completed Lab 01 or equivalent Docker knowledge
- Basic Python knowledge
- Understanding of environment variables

## 🔨 Task Description

Create a Python application and Docker setup that:

1. Reads configuration from environment variables
2. Handles sensitive data (API keys, passwords) securely
3. Uses Docker secrets for production scenarios
4. Implements proper fallback and default values
5. Demonstrates difference between build-time and runtime variables

## 🎓 Learning Goals

- Understand security implications of environment variables
- Learn proper secrets management in containers
- Practice using Docker secrets and config files
- Implement secure configuration patterns

## 📁 Project Structure

```
lab-02-python-env-secrets/
├── README.md (this file)
└── app/ (your work goes here)
```

## 🚀 Getting Started

1. Navigate to the `app/` directory
2. Create a Python application that uses environment variables
3. Create a Dockerfile with proper ENV and ARG usage
4. Implement secrets handling using Docker secrets
5. Test with different configuration scenarios

## ✅ Validation Criteria

Your solution should:

- [ ] Python app reads environment variables correctly
- [ ] Sensitive data is NOT hardcoded in the Dockerfile
- [ ] Uses ARG for build-time variables
- [ ] Uses ENV for runtime variables
- [ ] Implements Docker secrets for sensitive data
- [ ] Provides sensible defaults for optional configuration
- [ ] Logs do NOT expose sensitive information
- [ ] `.env` file is in `.dockerignore` and `.gitignore`

## 🔍 Verification Commands

```bash
# Build the image
docker build -t lab02-python-app .

# Run with environment variables
docker run -e DB_PASSWORD=secret123 lab02-python-app

# Run with env file
docker run --env-file .env lab02-python-app

# Use Docker secrets (requires Docker Swarm mode - run 'docker swarm init' first)
docker swarm init
echo "my-secret-password" | docker secret create db_password -
docker service create --secret db_password lab02-python-app
```

## 💡 Hints

- Use `os.environ.get()` in Python with default values
- Never commit `.env` files to version control
- Use `ARG` only for build-time variables
- Docker secrets are mounted at `/run/secrets/<secret_name>`
- Consider using python-decouple or similar libraries
- Validate required environment variables at startup

## 🎁 Bonus Challenges

1. Implement environment variable validation at startup
2. Create separate configurations for dev/staging/prod
3. Use Docker Compose to manage multiple services with shared secrets
4. Implement a configuration hierarchy (defaults < env < secrets)
5. Add encryption for sensitive environment variables

## 📖 Resources

- [Docker Environment Variables](https://docs.docker.com/engine/reference/commandline/run/#set-environment-variables--e---env---env-file)
- [Docker Secrets](https://docs.docker.com/engine/swarm/secrets/)
- [Python Environment Variables](https://docs.python.org/3/library/os.html#os.environ)
- [12-Factor App: Config](https://12factor.net/config)

## 🔗 Next Steps

Once you've completed this lab, move on to:
- **Lab 03**: PostgreSQL & Volumes

## 📝 Notes

- Never commit secrets to version control
- Use `.env.example` to document required environment variables
- Consider using a secrets management service in production
