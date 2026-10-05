# Product Steering File

## Overview

This file defines the product vision, goals, principles, and constraints for the AI-10 Portfolio. These principles apply across all 10 projects and guide product decisions, prioritization, and scope management.

---

## 1. Portfolio Vision

The AI-10 Portfolio demonstrates production-oriented AI engineering across 10 independent domains. Each project is not a toy demo but a deployable, testable, documented application that shows:

- Real AI engineering (RAG, agents, evaluation, observability, security)
- Production patterns (auth, RBAC, error handling, observability, CI/CD)
- AI-SDLC discipline (traceability, evaluation, human-in-the-loop, security gates)
- Portfolio-quality presentation (documentation, architecture records, test evidence)

---

## 2. Product Goals

For each project:
1. A new developer can run the application locally from the README
2. The primary end-to-end workflow passes automated acceptance tests
3. AI behavior is evaluated against a versioned representative test set
4. Security-sensitive actions are permission-checked and auditable
5. API errors, latency, and key workflow outcomes are observable
6. The project has a repeatable demo that showcases its core capability

For the portfolio:
1. All 10 projects share a consistent AI-SDLC framework
2. Traceability is complete: Jira → spec → prompt → implementation → test → release
3. Any project can be opened independently and built/run without understanding the others
4. The portfolio demonstrates AI-SDLC discipline as a hiring/showcase artifact

---

## 3. Product Principles

**Build real, not fake:**
- Every claimed feature must actually work
- Do not create documentation that claims unsupported functionality
- Do not invent test results
- Do not claim an AI evaluation score without running the evaluation

**Demonstrate the hard parts:**
- The interesting engineering is in evaluation, reliability, safety, and human-in-the-loop — not just the happy path
- Error handling, recovery, and observability are features, not afterthoughts
- Security is a first-class product requirement

**One coherent workflow per project:**
- Each project has one primary end-to-end workflow that a demo can walk through
- Secondary features support the primary workflow; they do not replace it
- MVP first: implement the core workflow completely before adding breadth

**AI is a component, not the product:**
- The product solves a user problem; AI is a component that helps it do so
- Users care about outcomes, not model names or token counts
- Evaluation measures user-relevant quality, not technical metrics in isolation

---

## 4. The 10 Projects

| ID | Project | Core Capability | Primary User |
|---|---|---|---|
| P01 | Enterprise Knowledge Intelligence Platform | Document ingestion, RAG search, grounded answers with citations | Knowledge workers, developers |
| P02 | Autonomous Market Research Analyst | Multi-step research, source collection, claim verification, report generation | Analysts, strategists |
| P03 | Smart Customer Service Assistant | Conversation management, RAG, ticket classification, escalation | Support agents, customers |
| P04 | Voice-Based Appointment and Task Assistant | STT, intent recognition, calendar/task integration, TTS | Individuals, scheduling users |
| P05 | AI Agent Monitoring and Reliability Platform | Agent trace collection, token/cost tracking, latency metrics, dashboards | AI engineers, SREs |
| P06 | Intelligent Invoice and Contract Processing | OCR, layout detection, schema extraction, human review queue | Finance, operations teams |
| P07 | AI Software Project Delivery Orchestrator | Multi-agent planning, Jira integration, dependency management, human approval | Engineering managers, dev teams |
| P08 | Context-Aware Enterprise Search Engine | Hybrid search, ACL filtering, query rewriting, reranking | Enterprise employees |
| P09 | AI Pull Request Review and Quality Assistant | GitHub App, diff analysis, AI review comments, security findings | Developers, tech leads |
| P10 | LLM Guard and Prompt Injection Defense Platform | Prompt injection detection, PII redaction, policy engine, audit dashboard | Security engineers, platform teams |

---

## 5. Scope Management Rules

**In scope by default for every project:**
- Core workflow from the ticket backlog
- Authentication and authorization
- Input validation and error handling
- Observability (logs, metrics, health endpoints)
- Automated tests for each ticket
- AI evaluation for AI-powered features
- Basic documentation (README, API, architecture)
- Docker/docker-compose local run
- CI pipeline

**Out of scope for initial MVP (unless explicitly in the ticket backlog):**
- Multi-region high availability
- Formal enterprise certifications (SOC 2, ISO 27001)
- Training foundation models from scratch
- Integrations not listed in the project backlog
- Unbounded autonomous actions without approval gates

**Scope change process:**
1. Identify the scope change and its business justification
2. Create a new Jira ticket
3. Get human approval before implementing
4. Do not invent requirements or implement undiscussed features

---

## 6. Definition of Ready

A ticket is ready to implement when:
- The outcome and affected user are clear
- Acceptance criteria are specific and testable
- Dependencies and affected components are identified
- Spec and design links are present
- Security and data impact are assessed
- Test and evaluation approach is defined
- Human reviewer is assigned
- The Kiro prompt scope, constraints, and expected output are explicit

---

## 7. Definition of Done

A ticket is done when:
- All acceptance criteria are evidenced with actual test output
- Code has human review (never self-approved)
- Tests ran and actual results are recorded
- Security, privacy, and performance impacts were considered
- No unresolved critical issue without formal risk acceptance
- Observability and safe failure behavior are present
- Documentation and traceability are updated
- No secrets or sensitive data leaked

---

## 8. Human Approval Gates

Mandatory human approval for:
- Production deployment
- Security exceptions
- Data deletion operations
- External side effects with financial or business impact
- Architecture changes
- Permission escalation
- Risk acceptance decisions
- Release approval (Gate G5)

AI must not automatically approve its own work, transition tickets to Done, or deploy to production.

---

## 9. Prioritization Framework

When prioritizing within a project sprint:

1. **Foundation first:** Repository skeleton, database schema, API foundation, auth (tickets 01–05)
2. **Core workflow second:** The primary feature that makes the project demonstrable (tickets 06–15)
3. **Evaluation and quality third:** AI evaluation, observability, security hardening (tickets 16–18)
4. **Release readiness last:** CI/CD, deployment docs, integrated demo (tickets 19–20)

Do not start CI/CD before the core workflow is working. Do not ship a demo before evaluation is complete.
