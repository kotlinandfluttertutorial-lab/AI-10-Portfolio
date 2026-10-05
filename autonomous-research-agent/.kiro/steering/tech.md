# Technology Steering

Use this stack unless repository constraints require a documented change: Python, FastAPI, LangGraph, PostgreSQL, Redis, search provider adapter, React/TypeScript, Docker

Maintain clear API/domain/adapter boundaries. Use typed schemas, migrations, dependency injection for external providers, structured logging, and automated tests. Never commit credentials. Keep provider-specific code behind interfaces.
