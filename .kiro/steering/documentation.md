# Documentation Steering File

## Overview

This file defines the documentation standards, required documents, quality rules, and maintenance practices for all 10 projects in the AI-10 Portfolio. Documentation is a deliverable, not an afterthought. Every project must maintain accurate, up-to-date documentation that reflects the actual implementation.

---

## 1. Documentation Principles

- **Documentation reflects reality:** Never document features that are not yet implemented. Never claim test results that were not produced.
- **Docs are code:** Documentation lives in the repository, is reviewed in PRs, and follows the same quality standards as code.
- **Minimal but complete:** Each document covers its topic completely but does not repeat content from other documents. Cross-reference rather than duplicate.
- **Discoverable:** A developer unfamiliar with the project can find what they need within 5 minutes of opening the repository.
- **Maintained, not archived:** Outdated documentation is a bug. File a ticket when you find wrong documentation.

---

## 2. Required Documents Per Project

### README.md
The project entry point. Must contain:
- Project name and one-line description
- What problem it solves and who it is for
- Prerequisites (language runtime, Docker, required accounts)
- Getting started: clone → configure → run (exact commands)
- Running tests (exact commands, expected output)
- Environment variables (list of all variables with types, defaults, and descriptions)
- Project structure overview
- Link to ARCHITECTURE.md, API.md, SECURITY.md
- Known limitations
- License

### ARCHITECTURE.md
Technical overview for developers and architects. Must contain:
- System overview and purpose
- Component diagram (text-based or image)
- Data flow description for the primary workflow
- Key architectural decisions (link to ADRs)
- External dependencies and integrations
- Database schema overview
- Async/event flow description if applicable
- Failure modes and recovery behavior
- Scalability notes

### API.md (or openapi.yaml)
Complete API reference. Must contain:
- Base URL and versioning strategy
- Authentication method
- All endpoints: method, path, description, request schema, response schema, example
- Error code reference
- Rate limiting documentation
- Webhook or event payloads (where applicable)
- Changelog (version history)

Prefer `openapi.yaml` as the source of truth; `API.md` may summarize it for readability.

### SECURITY.md
Security posture document. Must contain:
- Authentication and authorization model
- Role definitions and permissions
- Secrets management approach
- Data classification (what data is stored, its sensitivity)
- Known risks and mitigations
- Prompt injection controls (for AI projects)
- Dependency scanning process
- Security contact / responsible disclosure

### EVALUATION.md
AI quality measurement document. Must contain:
- Evaluation dimensions and their definitions
- Dataset description (size, sources, versioning)
- Metric formulas (not just names)
- How to run an evaluation (exact commands)
- Baseline results with date and model version
- Regression thresholds
- Known quality limitations

### DEPLOYMENT.md
Deployment guide. Must contain:
- Architecture diagram (production topology)
- Required infrastructure (databases, queues, services)
- Environment variables for production (without values — reference the secret store)
- Deployment steps (step-by-step)
- Database migration steps
- Health check verification
- Rollback procedure
- First-time setup vs. upgrade paths

### OPERATIONS.md
Day-2 operations guide. Must contain:
- Dashboard links or descriptions
- Key metrics and their normal ranges
- Alert definitions and response runbooks
- Common error patterns and their causes
- Log query examples for common debugging scenarios
- Backup and restore procedures
- Incident response process

### CONTRIBUTING.md
Developer onboarding guide. Must contain:
- Development setup (prerequisites, install, run)
- Branch naming and commit message conventions
- PR process and review checklist
- Ticket workflow (Ready → In Progress → Review → Done)
- How to add a new Jira ticket and Kiro prompt
- How to run the full test suite
- How to run AI evaluations
- Code style guide reference
- Contact and escalation

---

## 3. Portfolio-Level Documentation

At the repository root:

### README.md (portfolio)
- Portfolio overview: what this is and who it is for
- Table of all 10 projects with folder links
- AI-SDLC framework overview and reference to `AI-SDLC/`
- How to use the Kiro prompts
- Implementation roadmap
- Jira import instructions

### docs/architecture/
- Portfolio-level architecture overview
- ADRs (Architecture Decision Records) for cross-project decisions
- Shared infrastructure decisions

### docs/api/
- API style guide that all projects follow
- Cross-project API conventions

### docs/security/
- Portfolio security policy
- Security gate checklists (one per project, per release)
- Threat model templates

### docs/evaluation/
- Evaluation framework overview
- Per-project evaluation reports (stored after each evaluation run)
- Baseline comparison history

### docs/operations/
- Portfolio operations overview
- Shared runbook templates
- CI/CD pipeline documentation

---

## 4. Traceability Documentation

Every project must maintain a `TRACEABILITY.md` that maps:

```
Jira Ticket → Kiro Prompt → Requirement → Design → Implementation → Test → Evaluation
```

Format:
```markdown
| Ticket | Kiro Prompt | Requirement | Design | Implementation | Test | Status |
|--------|-------------|-------------|--------|----------------|------|--------|
| P01-08 | kiro-prompts/p01-08-*.md | specs/requirements.md#parsing | specs/design.md#parser | src/parsers/ | tests/test_parsers.py | Done |
```

Update `TRACEABILITY.md` as part of each ticket's Definition of Done.

---

## 5. ADR (Architecture Decision Record) Format

Store ADRs in `docs/architecture/` with naming `ADR-XXX-title.md`.

```markdown
# ADR-001: Use PostgreSQL with pgvector for vector storage

**Status:** Accepted
**Date:** 2026-10-05
**Deciders:** [List of people who made the decision]

## Context
[What is the problem we are solving? What constraints exist?]

## Decision
[What did we decide?]

## Consequences
**Positive:**
- [Benefit 1]

**Negative / Trade-offs:**
- [Risk or cost 1]

## Alternatives Considered
| Alternative | Why rejected |
|---|---|
| Pinecone | Vendor lock-in; additional cost |
| Chroma | Limited production readiness |

## References
- [Link to relevant spec or ticket]
```

---

## 6. Documentation Quality Rules

- **Accuracy:** Every claimed feature must exist. Test commands must actually work. Result numbers must come from actual runs.
- **Completeness:** Every required document section is present. No section left with "TODO" in a released version.
- **Currency:** Documentation is updated in the same PR that changes the code. Docs drift is a bug.
- **Clarity:** Write for a developer who is intelligent but unfamiliar with this specific project. Avoid jargon without definition.
- **Examples:** All API documentation includes at least one real request/response example.
- **Commands:** All commands are copy-pasteable and tested. Include expected output or mention what success looks like.

---

## 7. Documentation Review Checklist

Include in every PR that changes code:

```
[ ] README.md updated if setup or run steps changed
[ ] API.md / openapi.yaml updated if endpoints changed
[ ] ARCHITECTURE.md updated if component structure changed
[ ] SECURITY.md updated if security controls changed
[ ] EVALUATION.md updated if evaluation dimensions or results changed
[ ] TRACEABILITY.md updated for this ticket
[ ] No documentation claims unimplemented functionality
[ ] All code examples in docs are tested or marked as illustrative
```

---

## 8. Living Documentation

Documentation is never "done" — it evolves with the project. Practices:

- Review all documentation at the start of each sprint and file tickets for outdated sections
- Documentation improvements are valid Jira tickets
- Every new feature ticket includes documentation as part of its Definition of Done
- Documentation is reviewed in code review with the same rigour as code
