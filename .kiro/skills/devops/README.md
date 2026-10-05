# Skill: DevOps

This skill covers containerization, CI/CD, and deployment patterns for all 10 projects.

## Topics
- Dockerfile best practices (multi-stage builds, non-root user, .dockerignore)
- docker-compose for local development (app + db + redis + workers)
- GitHub Actions CI pipeline (lint, type-check, test, security scan, build)
- Environment variable management across environments
- Alembic migration execution in CI and deployment
- Health check configuration in Docker and Kubernetes
- Prometheus metrics scraping configuration
- Grafana dashboard provisioning
- Log aggregation patterns (structured JSON to ELK/Loki)
- Deployment strategies (rolling, blue-green basics)
- Rollback procedures
- Secret injection patterns for CI and production
- Container image tagging and versioning
- Dependency caching in CI

## Reference
See `.kiro/steering/architecture.md` for technology defaults and `.kiro/steering/engineering.md` for configuration standards.
