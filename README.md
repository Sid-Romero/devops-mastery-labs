# Docker Mastery Labs

A comprehensive collection of hands-on labs designed to master Docker, Kubernetes, and related DevOps technologies. Each lab is a self-contained mini-project with clear objectives, specific constraints, and validation criteria. Progress from beginner to production expert through practical, real-world scenarios.

## Documentation

- **[Learning Path](docs/learning-path.md)** - Recommended progression through the labs
- **[Resources](docs/resources.md)** - Curated learning materials, tools, and references

## Quick Start

1. Clone this repository
2. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
3. Read the [Learning Path](docs/learning-path.md) to understand the recommended order
4. Start with Lab 01 and progress sequentially
5. Complete each lab's validation criteria before moving to the next

## Labs Overview

### Beginner Level (Labs 1-5)

Build foundational Docker knowledge with practical, hands-on projects.

| Lab | Title | Concepts | Status |
|-----|-------|----------|--------|
| [01](lab-01-multistage-node/) | Multi-stage Node.js Build | Multi-stage builds, optimization, layer caching | Not Started |
| [02](lab-02-python-env-secrets/) | Python Environment & Secrets | Environment variables, secrets management, configuration | Not Started |
| [03](lab-03-postgres-volumes/) | PostgreSQL & Volumes | Data persistence, volumes, backup/restore | Not Started |
| [04](lab-04-network-isolation/) | Network Isolation | Docker networking, service isolation, DNS | Not Started |
| [05](lab-05-mern-compose/) | MERN Stack with Compose | Multi-container orchestration, full-stack apps | Not Started |

### Intermediate Level (Labs 6-15)

Advanced Docker Compose, networking, and container orchestration topics.

### Advanced Level (Labs 16-25)

Production deployments, CI/CD, and DevOps integration.

### Expert Level (Labs 26-35)

Enterprise orchestration and cloud-native architectures.

## Progress Tracking

Track your progress by updating the status column in your fork:
- Not Started
- In Progress
- Completed
- Completed + Bonus Challenges

## Repository Structure

```
docker-mastery-labs/
├── README.md (this file - index of all labs)
├── docs/
│   ├── learning-path.md (recommended learning progression)
│   └── resources.md (curated learning resources)
├── lab-01-multistage-node/
│   ├── README.md (lab instructions)
│   ├── app/ (your work directory)
│   └── solution/ (reference solution)
├── lab-02-python-env-secrets/
│   ├── README.md
│   └── app/
├── lab-03-postgres-volumes/
│   ├── README.md
│   └── data/
├── lab-04-network-isolation/
│   ├── README.md
│   └── services/
└── lab-05-mern-compose/
    ├── README.md
    └── stack/
```

## Learning Approach

Each lab follows a consistent structure:

1. **Objectives** - Clear learning goals
2. **Concepts Covered** - Key topics you'll learn
3. **Prerequisites** - What you should know beforehand
4. **Task Description** - What you need to build
5. **Validation Criteria** - How to verify your solution
6. **Verification Commands** - Commands to test your work
7. **Hints** - Guidance without giving away the solution
8. **Bonus Challenges** - Extra practice for deeper learning
9. **Resources** - Links to relevant documentation

## Automated Lab Generation Pipeline

This repository utilizes an automated pipeline to continuously generate new hands-on labs using AI technology and web scraping.

### How Labs Are Created

The lab generation process follows a multi-stage pipeline:

#### 1. Content Discovery
The system scrapes trending DevOps content from multiple authoritative sources:
- Dev.to RSS feeds
- GitHub Trending repositories
- CNCF Blog
- Reddit communities (r/devops, r/kubernetes, r/docker, r/ansible)
- Hacker News (filtered for DevOps topics)
- Medium DevOps tags

#### 2. Topic Selection
From the scraped content, the system:
- Extracts relevant topics and technologies
- Identifies key concepts and learning opportunities
- Selects topics that align with the repository's learning progression
- Ensures diversity across Docker, Kubernetes, Helm, ArgoCD, and Ansible

#### 3. AI-Powered Generation
Using Google Gemini AI, the system generates complete lab structures including:
- Comprehensive objectives and learning goals
- Step-by-step task descriptions
- Validation criteria and verification commands
- Hints and bonus challenges
- Relevant documentation links
- Difficulty assessment (beginner, intermediate, advanced, expert)

#### 4. Lab Creation
The file creator component:
- Generates the lab directory structure
- Creates README.md with complete instructions
- Sets up starter files and solution directories
- Assigns sequential lab numbers
- Organizes labs by difficulty level

### GitHub Actions Workflow

The lab generation is automated through GitHub Actions:

**Schedule:**
- Runs automatically at intervals of 3 or 5 hours (runs at 00:00, 03:00, 08:00, 11:00, 16:00, 19:00 UTC)
- Switches to daily generation once 50 labs are reached
- Can be manually triggered with technology specification

**Process:**
1. Checks existing lab count
2. Determines if generation should proceed
3. Scrapes current DevOps content
4. Selects topic and technology
5. Generates lab using AI
6. Creates lab files in repository
7. Commits and pushes new lab

**Technologies Supported:**
- Docker
- Kubernetes
- Helm
- ArgoCD
- Ansible

### Manual Lab Generation

Developers can manually generate labs using the Python scripts:

```bash
cd scripts
pip install -r requirements.txt
python lab_generator.py --technology docker
```

Available options:
- `--technology <tech>` - Force specific technology
- `--skip-scrape` - Use fallback topics
- `--dry-run` - Test without creating files
- `--test` - Run local tests

See [scripts/README.md](scripts/README.md) for detailed documentation.

## Tips for Success

- **Work Sequentially**: Labs build on each other's concepts
- **Read Carefully**: Each lab README contains important details
- **Validate Your Work**: Use the provided validation criteria
- **Try Before Peeking**: Attempt to solve independently before checking solutions
- **Experiment**: Don't be afraid to try different approaches
- **Document**: Take notes on what you learn

## Contributing

Contributions are welcome. If you find issues or have improvements:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

Inspired by real-world Docker use cases and community best practices. Lab content is dynamically generated using Google Gemini AI and curated from trending DevOps topics across the web.

## Feedback

If you have questions, suggestions, or feedback:
- Open an issue on GitHub
- Share your learning journey
- Help improve the labs for others
