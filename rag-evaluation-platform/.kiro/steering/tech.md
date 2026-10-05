# Technology Steering

Use this stack unless repository constraints require a documented change: Python 3.12, FastAPI, PostgreSQL + pgvector, object storage, React/TypeScript, Docker, pytest, OpenTelemetry

Maintain clear API/domain/adapter boundaries. Use typed schemas, migrations, dependency injection for external providers, structured logging, and automated tests. Never commit credentials. Keep provider-specific code behind interfaces.
