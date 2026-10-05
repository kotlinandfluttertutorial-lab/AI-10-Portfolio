# Portfolio Security Policy

This document defines the security policy for the AI-10 Portfolio. All 10 projects must comply with these standards before release.

## Scope

This policy applies to all source code, infrastructure, AI integrations, data handling, and deployment artifacts in the AI-10 Portfolio.

## Security Gate Checklist Template

Use this checklist for every project before any release. Complete and store in `docs/security/` with a timestamp and sign-off.

```
Project: [P0X — Project Name]
Version: [x.y.z]
Date: [YYYY-MM-DD]
Security Reviewer: [Name]

AUTHENTICATION
[ ] Authentication implemented and tested
[ ] JWT tokens are short-lived with refresh rotation
[ ] API key hashing is implemented (never stored in plain text)
[ ] Brute-force protection in place on auth endpoints
[ ] Local development auth documented; no real credentials in repository

AUTHORIZATION
[ ] Authorization enforced at domain layer (not just routing layer)
[ ] Default-deny implemented (missing permission check = denied)
[ ] Cross-tenant data access impossible by design
[ ] AI-generated side-effect actions require explicit authorization
[ ] Authorization decisions logged for audit

RBAC
[ ] All roles defined: admin, member/operator, viewer, service
[ ] Role assignments stored in database and auditable
[ ] Role escalation requires human approval

INPUT VALIDATION
[ ] All HTTP endpoints validate request bodies with Pydantic
[ ] File uploads validated for MIME type, extension, size, content
[ ] Null bytes, path traversal, injection patterns rejected

OUTPUT VALIDATION
[ ] AI-generated structured outputs validated against schema
[ ] AI output used in SQL/HTML/shell is sanitized
[ ] Validation failures logged; operations fail closed

PROMPT INJECTION (AI projects only)
[ ] User input separated from system instructions via templates
[ ] Prompt injection test cases executed
[ ] Tool calls from AI validated against allowlist

SECRETS MANAGEMENT
[ ] No secrets in source code (scan passed)
[ ] .env not committed; .env.example present
[ ] CI secrets stored in CI secret store
[ ] Secret scanning CI step configured

PII HANDLING
[ ] PII fields identified in schema documentation
[ ] PII not logged in plain text
[ ] PII minimized before sending to AI providers

AUDIT LOGGING
[ ] All authentication events logged (success and failure)
[ ] All authorization failures logged
[ ] Admin and configuration changes logged
[ ] AI-triggered external side effects logged
[ ] Audit logs separate from application logs

RATE LIMITING
[ ] Rate limits on all public endpoints
[ ] Rate limit headers in responses
[ ] AI endpoint token-budget limits configured

DEPENDENCY SECURITY
[ ] pip-audit / safety scan passed (no high/critical CVEs)
[ ] All dependencies pinned to exact versions
[ ] License compatibility checked for new dependencies

DATA PROTECTION
[ ] TLS enforced for all external communication
[ ] Database backups encrypted
[ ] Data retention periods defined and implemented

KNOWN RISKS
[ ] All known risks documented and accepted by security owner
[ ] No unmitigated critical vulnerabilities
[ ] Security findings stored in docs/security/

SIGN-OFF
Security owner: ________________
Date: ________________
Notes: ________________
```

## Threat Model Template

Store project threat models at `docs/security/threat-model-P0X.md`.

### Template Structure

```
# Threat Model — [Project Name]

## Scope
What is in scope for this threat model.

## Assets
What is being protected.

## Threat Actors
Who might attack this system and why.

## Threats (STRIDE)

| Threat | Category | Asset | Likelihood | Impact | Mitigation |
|---|---|---|---|---|---|
| User submits prompt injection | Tampering | LLM interaction | High | High | Structural separation + injection test suite |

STRIDE categories: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege

## Residual Risks

| Risk | Likelihood | Impact | Owner | Acceptance Date |
|---|---|---|---|---|
```

## Responsible Disclosure

Security issues in this portfolio should be reported to the repository maintainer. For production systems derived from this portfolio, define a responsible disclosure process before launch.
