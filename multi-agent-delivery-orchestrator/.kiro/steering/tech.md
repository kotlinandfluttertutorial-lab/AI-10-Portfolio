# Technology Steering

Use this stack unless repository constraints require a documented change: Python, LangGraph, FastAPI, PostgreSQL, Jira REST API adapter, Git provider adapter, React/TypeScript, Docker

Maintain clear API/domain/adapter boundaries. Use typed schemas, migrations, dependency injection for external providers, structured logging, and automated tests. Never commit credentials. Keep provider-specific code behind interfaces.
