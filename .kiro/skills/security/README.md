# Skill: Security Engineering

This skill covers security patterns and controls for all 10 projects.

## Topics
- JWT authentication implementation (FastAPI + python-jose)
- API key management (generation, hashing, storage, rotation)
- RBAC implementation (roles, permissions, middleware)
- Input validation with Pydantic
- Output validation for AI-generated content
- Prompt injection detection patterns
- Tool authorization allowlists for agentic systems
- Secret scanning (detect-secrets, trufflehog)
- Dependency vulnerability scanning (pip-audit, safety)
- Audit logging schema and implementation
- Rate limiting with Redis (slowapi or custom)
- PII detection and redaction
- Secure error handling (no stack traces in responses)
- TLS configuration
- Security test patterns (auth bypass, injection, tenant isolation)

## Reference
See `.kiro/steering/security.md` for the full security standards and gate checklist.
