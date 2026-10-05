# AI-10 Project Portfolio — AI-SDLC Engineering System

This repository contains 10 independent AI engineering projects managed through a production-grade AI-assisted Software Development Life Cycle (AI-SDLC). Each project is a deployable, tested, documented application that demonstrates real AI engineering — RAG, agents, evaluation, observability, and security — not toy demos.

---

## Portfolio Overview

| ID | Project | Core AI Capability | Folder | Spec | Status |
|---|---|---|---|---|---|
| P01 | Enterprise Knowledge Intelligence Platform | RAG, hybrid search, grounded answers | `rag-evaluation-platform/` | `.kiro/specs/project-01/spec.md` | Specified |
| P02 | Autonomous Market Research Analyst | Research agent, claim verification | `autonomous-research-agent/` | `.kiro/specs/project-02/spec.md` | Specified |
| P03 | Smart Customer Service Assistant | RAG, classification, escalation | `customer-support-copilot/` | `.kiro/specs/project-03/spec.md` | Specified |
| P04 | Voice-Based Appointment and Task Assistant | STT, intent, TTS, confirmation gate | `voice-task-assistant/` | `.kiro/specs/project-04/spec.md` | Specified |
| P05 | AI Agent Monitoring and Reliability Platform | Agent traces, cost tracking, dashboards | `agentops-observability/` | `.kiro/specs/project-05/spec.md` | Specified |
| P06 | Intelligent Invoice and Contract Processing | OCR, LLM extraction, human review | `document-extraction-pipeline/` | `.kiro/specs/project-06/spec.md` | Specified |
| P07 | AI Software Project Delivery Orchestrator | Multi-agent pipeline, DAG planning | `multi-agent-delivery-orchestrator/` | `.kiro/specs/project-07/spec.md` | Specified |
| P08 | Context-Aware Enterprise Search Engine | Hybrid search, ACL filtering, reranking | `enterprise-semantic-search/` | `.kiro/specs/project-08/spec.md` | Specified |
| P09 | AI Pull Request Review and Quality Assistant | GitHub App, diff analysis, AI review | `github-code-review-ai/` | `.kiro/specs/project-09/spec.md` | Specified |
| P10 | LLM Guard and Prompt Injection Defense | Injection detection, PII redaction, policy | `enterprise-prompt-security/` | `.kiro/specs/project-10/spec.md` | Specified |

---

## What Each Project Contains

Every project folder has a consistent structure ready for implementation:

```
<project-folder>/
├── .kiro/
│   ├── specs/core-workflow.md       — Kiro spec for the primary workflow
│   └── steering/
│       ├── product.md               — Project goals and scope
│       ├── tech.md                  — Technology stack and patterns
│       └── quality.md               — Quality and testing standards
├── jira/
│   └── PXX-tickets.csv             — 20 Jira starter tickets (Jira-importable)
├── kiro-prompts/                    — 20 implementation prompts (pXX-NN-slug.md)
├── specs/
│   ├── requirements.md             — Functional and non-functional requirements
│   └── design.md                   — Architecture and component design
├── PROJECT-SPEC.md                  — 29-section project specification
├── README.md                        — Project-specific setup and run instructions
└── TRACEABILITY.md                  — Jira → spec → prompt → implementation map
```

---

## AI-SDLC Framework

This portfolio uses a 10-phase AI-assisted SDLC. Every project follows the same lifecycle:

```
DISCOVER → PLAN → SPECIFY → DESIGN → BUILD → VERIFY → SECURE → RELEASE → OPERATE → IMPROVE
```

**AI assists every phase. Humans remain accountable for:**
- Product scope decisions
- Architecture approvals
- Security risk acceptance
- Code review (never self-approved)
- Production deployment authorization
- Release approval (Gate G5)

### Phase Gates

| Gate | Phase | Who Approves | What Is Reviewed |
|---|---|---|---|
| G0 | DISCOVER | Product owner | Problem brief and scope |
| G1 | PLAN | Team | Backlog quality and Definition of Ready |
| G2 | SPECIFY | Tech lead | Requirements and design decisions |
| G3 | BUILD | Developer | Code, tests, and acceptance criteria |
| G4 | VERIFY | QA | Test evidence and AI evaluation results |
| G5 | RELEASE | Release owner | Release checklist, rollback plan, approval |
| G6 | IMPROVE | Team | Retrospective findings and backlog updates |

Full lifecycle definition: `.kiro/steering/ai-sdlc.md` and `AI-SDLC/AI-SDLC-MASTER.md`

---

## How to Use the Kiro Prompts

### Option A — Per-Project Workspace (Recommended)

Open a single project folder as your Kiro workspace. All per-project steering files and specs are pre-configured.

```
1. Open <project-folder>/ as the Kiro workspace
2. Review .kiro/steering/ and .kiro/specs/
3. Pick a Jira ticket from jira/PXX-tickets.csv
4. Open the linked Kiro prompt from kiro-prompts/pXX-NN-*.md
5. Ask Kiro: "Implement [ticket key]"
6. Review the diff, run tests, update Jira with evidence
```

### Option B — Portfolio Workspace (Cross-Project)

Open this root folder as the workspace for cross-project work (steering files, architecture decisions, Jira structure).

```
1. Open AI-10-Portfolio/ as the Kiro workspace
2. Navigate to docs/jira/project-XX/kiro-prompts/
3. Open PROJECT-XX-NNN.md for the ticket you want to implement
4. Open <project-folder>/ as a second workspace tab
5. Follow the prompt instructions
```

### Prompt Locations

| Location | Naming | Used For |
|---|---|---|
| `<project-folder>/kiro-prompts/pXX-NN-slug.md` | `p01-08-pdf-docx-text-parsing.md` | Per-project workspace (primary) |
| `docs/jira/project-XX/kiro-prompts/PROJECT-XX-NNN.md` | `PROJECT-01-008.md` | Portfolio workspace, canonical index |

Both sets of prompts exist. The per-project ones are the primary working prompts. The `docs/jira/` ones are the canonical portfolio-level index.

---

## Portfolio Structure

```
AI-10-Portfolio/
│
├── .kiro/
│   ├── steering/                    — Portfolio-level AI-SDLC rules (active in root workspace)
│   │   ├── ai-sdlc.md              — Full lifecycle with phase definitions and gates
│   │   ├── architecture.md         — Modular architecture, provider abstraction, observability
│   │   ├── engineering.md          — 21 non-negotiable engineering rules, code standards
│   │   ├── security.md             — Auth, RBAC, secrets, PII, prompt injection, audit
│   │   ├── testing.md              — Unit, integration, API, E2E, security, AI evaluation
│   │   ├── product.md              — Portfolio vision, product principles, scope rules
│   │   └── documentation.md        — Required docs, ADR format, traceability
│   │
│   ├── specs/
│   │   └── project-01/ … project-10/  — 29-section spec per project
│   │
│   └── skills/                      — AI-SDLC skill reference files
│       ├── ai-sdlc/, architecture/, backend/, frontend/
│       ├── ai-engineering/, rag/, agents/, evaluation/
│       ├── security/, testing/, devops/
│
├── docs/
│   ├── architecture/
│   │   └── overview.md             — Portfolio architecture, shared ADRs
│   ├── api/
│   │   └── api-style-guide.md      — API design contract all projects follow
│   ├── security/
│   │   └── portfolio-security-policy.md — Security gate checklist template
│   ├── evaluation/
│   │   └── evaluation-framework.md — Per-project evaluation metrics and methodology
│   ├── operations/
│   │   └── portfolio-operations.md — Shared runbook templates, CI/CD patterns
│   └── jira/
│       ├── README.md               — Traceability index
│       └── project-01/ … project-10/
│           ├── README.md           — Ticket table with Jira → Prompt links
│           ├── PXX-tickets-full.csv — 20 tickets × 16 fields (enhanced Jira format)
│           └── kiro-prompts/
│               └── PROJECT-XX-001.md … PROJECT-XX-020.md
│
├── projects/
│   └── README.md                   — Canonical project folder mapping
│
├── AI-SDLC/
│   ├── AI-SDLC-MASTER.md           — Master lifecycle reference
│   ├── agents/agent-roles.md       — Agent role definitions
│   ├── gates/release-checklist.md  — Release gate checklist
│   └── templates/ticket-prompt-template.md
│
├── rag-evaluation-platform/        — P01 source folder
├── autonomous-research-agent/      — P02 source folder
├── customer-support-copilot/       — P03 source folder
├── voice-task-assistant/           — P04 source folder
├── agentops-observability/         — P05 source folder
├── document-extraction-pipeline/   — P06 source folder
├── multi-agent-delivery-orchestrator/ — P07 source folder
├── enterprise-semantic-search/     — P08 source folder
├── github-code-review-ai/          — P09 source folder
├── enterprise-prompt-security/     — P10 source folder
│
├── ALL-PROJECTS-JIRA.csv           — All 200 tickets in one flat CSV (Jira import)
└── README.md                       — This file
```

---

## Implementation Roadmap

Follow this sequence. Do not implement multiple projects simultaneously. Complete Phase 1 before Phase 2.

### Phase 1 — Portfolio Foundation (Done ✓)

- [x] AI-SDLC steering files (7 files covering lifecycle, architecture, engineering, security, testing, product, documentation)
- [x] 10 project specifications (29 sections each)
- [x] 200 Jira ticket definitions (20 per project × 16 fields)
- [x] 200 Kiro prompts (20 per project in canonical naming)
- [x] Portfolio documentation (architecture overview, API style guide, security policy, evaluation framework, operations guide)
- [x] Skills library (11 domain skill files)

### Phase 2 — Select and Implement First Project

**Recommended starting order based on complexity and dependency:**

| Order | Project | Why Start Here |
|---|---|---|
| 1st | **P05 — AgentOps** | No LLM inference needed for core platform. Demonstrates observability engineering. SDK provides a reusable instrumentation pattern. |
| 2nd | **P01 — RAG Platform** | Core RAG skills reused in P03 and P08. Well-defined success criteria (Recall@k, faithfulness). |
| 3rd | **P10 — Prompt Security** | Security-first project. Creates reusable PII/injection patterns for all other projects. |
| 4th | **P03 — Support Copilot** | Reuses RAG from P01. Clear user workflow with measurable outcomes (resolution rate, CSAT). |
| 5th | **P08 — Enterprise Search** | Extends RAG and adds ACL, connectors, and analytics. |
| 6th | **P02 — Research Agent** | Agent patterns. ReAct loop with bounded iteration. |
| 7th | **P04 — Voice Agent** | Voice pipeline. Confirmation gate pattern. |
| 8th | **P06 — Data Extraction** | OCR + LLM + human review queue. |
| 9th | **P09 — Code Review AI** | GitHub App. Webhook integration. |
| 10th | **P07 — Multi-Agent** | Most complex. Requires understanding of all prior agent patterns. |

### Phase 3 — Per-Project Implementation Sequence

For every selected project, follow this ticket order:

```
Tickets 01–05:  Foundation (skeleton, architecture doc, schema, API, auth)
Tickets 06–15:  Core workflow (the features that make the project demonstrable)
Ticket 16:      AI evaluation (measure quality before release)
Ticket 17:      Observability (logs, metrics, dashboards)
Ticket 18:      Security hardening (threat model, security gate)
Ticket 19:      CI/CD and deployment documentation
Ticket 20:      Integrated demo and release acceptance report
```

**Do not skip ahead.** Evaluation (ticket 16) must be done before tickets 17–20. Security hardening (ticket 18) must be done before the release demo (ticket 20).

### Phase 4 — Evaluate, Harden, Release

For each project:
1. Run the evaluation suite (ticket 16) — record actual results
2. Review security gate checklist (ticket 18) — get human sign-off
3. Build and test the Docker Compose stack (ticket 19)
4. Run the end-to-end demo (ticket 20) — record evidence
5. Obtain human release approval (Gate G5)
6. Document known limitations honestly

### Phase 5 — Cross-Project Learning

After the first project is released:
- Update the AI-SDLC framework with lessons learned
- Update shared skill files with new patterns discovered
- Carry evaluation datasets and security test patterns forward

---

## Jira Import Instructions

### Using ALL-PROJECTS-JIRA.csv (simple import)

Contains all 200 tickets with: Project ID, Project, Issue Type, Issue Key, Summary, Description, Priority, Labels, Epic Link, Acceptance Criteria, Story Points.

1. Create epics manually (one per project) before importing
2. Import via Jira → Projects → Import Issues → CSV
3. Map fields: Summary, Issue Type, Description, Priority, Labels, Acceptance Criteria
4. Epic Link field mapping varies by Jira instance — use Labels as fallback

### Using docs/jira/project-XX/PXX-tickets-full.csv (enhanced import)

Contains all 16 fields including Business Value, Dependencies, Skills, Technical Notes, AI-SDLC Phase, Security Requirements, Definition of Done. These additional fields do not have standard Jira equivalents — import them as custom fields or paste into the Description.

---

## Technology Defaults

All projects use the same technology stack unless an ADR documents a deviation:

| Concern | Default |
|---|---|
| Backend | Python 3.11+, FastAPI |
| Database | PostgreSQL 15 + pgvector |
| Cache / Queue | Redis |
| Migrations | Alembic |
| Testing | pytest |
| Lint / Format | ruff, black |
| Type checking | mypy |
| Frontend | React + TypeScript + Vite |
| CI | GitHub Actions |
| Containerization | Docker + docker-compose |
| Metrics | Prometheus-compatible |
| Tracing | OpenTelemetry |
| Secret management | Environment variables → Vault for production |

---

## Cross-Reference System

Every artifact traces back to its parent:

```
Jira Ticket (PXX-NN)
    ↓
Kiro Prompt (docs/jira/project-XX/kiro-prompts/PROJECT-XX-NNN.md)
    ↓
Requirement (<project-folder>/specs/requirements.md)
    ↓
Design (<project-folder>/specs/design.md)
    ↓
Implementation (<project-folder>/domain/, api/, adapters/)
    ↓
Tests (<project-folder>/tests/)
    ↓
Evaluation (<project-folder>/evaluation/)
    ↓
Security Review (docs/security/threat-model-PXX.md)
    ↓
Pull Request (branch: feature/PXX-NN-slug)
    ↓
Release (docs/operations/release-PXX-v1.0.md)
```

Maintain this traceability. Update `TRACEABILITY.md` in each project folder when completing a ticket.

---

## Non-Negotiable Rules

Before implementing any ticket:

1. Inspect the existing repository — never overwrite working functionality without understanding it
2. Never invent requirements — only implement what the Jira ticket specifies
3. Never claim tests passed without running them — report actual commands and results
4. Never self-approve code — every PR requires human review
5. Never deploy to production without Gate G5 human approval
6. No secrets, API keys, or credentials in source code
7. Treat LLM output as untrusted — validate all structured AI output
8. Stop and ask when requirements conflict or a security decision is ambiguous

---

## Contributing

See `AI-SDLC/AI-SDLC-MASTER.md` for the full workflow.

**Branch naming:** `feature/P01-08-pdf-docx-text-parsing`  
**Commit format:** `[P01-08] Add PDF/DOCX parser — N tests passing`  
**PR requirement:** Human reviewer required. CI must pass. No self-merges.

---

## License

This portfolio is a demonstration of AI-SDLC engineering practices. Replace with your chosen license before any production deployment.
