# Project Specification — P07: AI Software Project Delivery Orchestrator

**Project ID:** P07  
**Folder:** `multi-agent-delivery-orchestrator/`  
**Status:** Specified  
**AI-SDLC Phase:** SPECIFY → DESIGN  
**Version:** 1.0

---

## 1. Executive Summary

Software projects fail when requirements are vague, architecture is undocumented, and planning is disconnected from delivery. This platform orchestrates a multi-agent workflow that transforms a high-level project description into requirements, architecture, a dependency-aware plan, Jira tickets, and code scaffolding — with human approval gates at each major phase.

---

## 2. Problem Statement

Engineering teams spend 20–30% of project time on planning and requirements work that is repetitive and could be AI-assisted. Existing tools generate artifacts in isolation without connecting requirements to architecture to tasks. Human oversight is required but tedious when every step is manual.

---

## 3. Target Users

- Engineering managers needing rapid project kickoffs
- Tech leads generating architecture and planning artifacts
- Developers who want a structured plan before writing code

---

## 4. Personas

**Jordan — Engineering Manager:** Needs to start a new project from a one-paragraph description. Wants requirements, architecture, and a 2-sprint Jira backlog in under an hour, with full control to revise before approving.

**Sam — Tech Lead:** Reviews the AI-generated architecture and approves or rejects it. Wants clear ADRs and a defensible rationale for each decision.

---

## 5. User Journeys

**Primary (Jordan):**
1. Submits: "Build a multi-tenant document storage API with access control"
2. Requirements Agent generates functional and non-functional requirements
3. Jordan reviews and approves
4. Architecture Agent generates component design and database schema
5. Sam (tech lead) reviews and approves architecture
6. Planning Agent generates dependency-ordered Jira tickets
7. Jordan imports tickets to Jira
8. Coding Agent scaffolds project structure

---

## 6. Business Goals

- Reduce project kickoff time from days to hours
- Generate 0 circular dependencies in task plans (hard requirement)
- All generated architecture decisions include rationale
- Human approval required before any external action (Jira write, code generation)

---

## 7. Functional Requirements

- FR-01: Accept project description and constraints as input
- FR-02: Requirements Agent: generate functional/non-functional requirements
- FR-03: Architecture Agent: generate component diagram, data model, ADRs
- FR-04: Planning Agent: generate dependency-ordered task list with estimates
- FR-05: Coding Agent: scaffold project structure from approved plan
- FR-06: Testing Agent: generate test strategy and test stubs
- FR-07: Review Agent: validate each phase output before advancing
- FR-08: Human approval gate: each phase requires approval before continuing
- FR-09: Jira integration: create tickets from approved plan
- FR-10: Shared state: all agents read/write to a shared project context

---

## 8. Non-Functional Requirements

- NFR-01: No Jira writes or code generation without human approval
- NFR-02: Requirements phase completes in < 2 minutes
- NFR-03: Task dependency graph must be a DAG (no cycles, enforced algorithmically)
- NFR-04: Each agent operates on its assigned phase only (no agent can skip to a later phase)
- NFR-05: Maximum agent iterations: 3 revision cycles per phase

---

## 9. System Architecture

```
[Project Request] → [Shared State Store]
                          ↓
                  [Requirements Agent]
                          ↓ (human approval)
                  [Architecture Agent]
                          ↓ (human approval)
                  [Planning Agent]
                          ↓ (human approval)
              [Coding + Testing Agents]
                          ↓ (human approval)
              [Review Agent]
                          ↓
              [Jira Integration (on approval)]
```

---

## 10. Component Architecture

- `api/` — projects, phases, approvals, jira-export, health
- `domain/` — Project, Phase, Artifact, ApprovalGate, Dependency, JiraTicket
- `adapters/` — LLM adapter, Jira API adapter
- `workers/` — phase execution workers (one per agent role)
- `evaluation/` — plan validity, dependency correctness, artifact completeness

---

## 11. Data Architecture

Core entities: Project, Phase, PhaseArtifact, ApprovalGate, Task, Dependency, JiraExport

Key relationships:
- Project 1:N Phases (ordered)
- Phase 1:N Artifacts
- Phase 1:1 ApprovalGate
- Planning Phase → N Tasks with Dependency edges (DAG)

---

## 12. Database Schema (Key Tables)

```sql
projects(id, name, description, status, created_by, created_at)
phases(id, project_id, phase_type, status, created_at)
artifacts(id, phase_id, artifact_type, content, version, created_at)
approval_gates(id, phase_id, approver_id, decision, notes, created_at)
tasks(id, project_id, title, estimate_points, phase_id, created_at)
task_dependencies(task_id, depends_on_task_id)
jira_exports(id, project_id, export_status, jira_project_key, created_at)
```

---

## 13. API Specification

```
POST   /v1/projects              — create project with description
GET    /v1/projects/{id}         — get project status and phase tree
GET    /v1/projects/{id}/phases  — get all phases and their artifacts
POST   /v1/phases/{id}/approve   — human approves phase output
POST   /v1/phases/{id}/reject    — human rejects and provides feedback
POST   /v1/projects/{id}/export/jira — export approved tasks to Jira
GET    /v1/health
```

---

## 14. AI Architecture

- Requirements Agent: LLM that transforms description into structured FR/NFR list
- Architecture Agent: LLM that produces component diagram (text), data model, ADRs
- Planning Agent: LLM that produces task list with estimates and dependencies; DAG validated after generation
- Coding Agent: LLM that generates project scaffolding (file structure, boilerplate)
- Testing Agent: LLM that produces test strategy and pytest/jest stubs
- Review Agent: LLM that reviews each phase artifact for completeness and consistency
- Shared context: each agent receives the accumulated project context from all prior phases

---

## 15. Prompt Architecture

- Requirements prompt: system defines FR/NFR structure; user provides description + constraints; output is structured JSON
- Architecture prompt: system defines component and ADR format; user provides requirements; output is structured JSON
- Planning prompt: system defines task schema with dependencies; DAG constraint stated explicitly
- Each prompt includes relevant prior phase artifacts as context
- All prompts versioned in `domain/prompts/`

---

## 16. Agent Architecture

Multi-agent pipeline with strict phase ordering:
1. Each phase is a separate agent with its own prompt, model config, and output schema
2. Agents are stateless — they receive full context from shared state and produce one artifact
3. Human approval gates between phases — no phase starts until prior phase is approved
4. Maximum revisions: if human rejects a phase 3 times with the same feedback, escalate and pause

---

## 17. Tool Architecture

Tools available (allowlisted, all require approval before execution):
- `jira.create_project(key, name)` — requires human approval
- `jira.create_issue(project_key, summary, type, description)` — requires human approval
- `code.scaffold_project(structure)` — generates files, requires human approval

Read-only tools (no approval needed):
- `jira.get_projects()` — read Jira project list
- `jira.get_issue_types(project_key)` — read issue types

---

## 18. Security Architecture

- JWT authentication; project creator owns the project
- No Jira or code writes without a confirmed ApprovalGate record
- Jira credentials: OAuth2 or API token stored encrypted, not in logs
- Agent prompts contain no credentials; credentials injected at the adapter boundary
- Task dependency graph is validated for cycles before accepting the planning output

---

## 19. Evaluation Architecture

Metrics: plan validity (% plans with no dependency cycles), requirement completeness, architecture coverage (all FRs addressed), task completion rate in demo

---

## 20. Observability Architecture

- Metrics: `phases_completed_total`, `approval_decisions_total{decision}`, `agent_latency_seconds{agent}`, `jira_exports_total`
- Logs: phase start/complete/reject with `project_id`, `phase_type`, no artifact content

---

## 21. Deployment Architecture

```
docker-compose: postgres, redis, api, phase-workers (one per agent type), frontend (React)
```

---

## 22. Testing Strategy

- Unit: DAG cycle detection, artifact schema validation, approval gate enforcement
- Integration: full multi-phase workflow with mocked LLM and Jira
- API: project CRUD, approval flow, Jira export
- Security: phase sequencing enforcement, approval bypass attempts, Jira credential isolation
- E2E: description → approved requirements → approved architecture → approved plan → Jira export

---

## 23. Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Circular task dependencies | Medium | High | DAG validation after planning phase; reject if cycles found |
| Jira write without approval | Low | Critical | Hard requirement: no export without ApprovalGate status=approved |
| LLM-generated architecture misses key concerns | Medium | Medium | Review Agent validates; human reviews before approval |
| Jira API credential leakage | Low | High | Credentials stored encrypted; not in logs |

---

## 24. Threat Model

Approval bypass (write without gate), Jira credential exposure, prompt injection via project description. Full threat model: `docs/security/threat-model-P07.md`

---

## 25. Performance Requirements

- Requirements phase: < 2 minutes
- Architecture phase: < 3 minutes
- Planning phase (20-task plan): < 2 minutes
- Jira export (20 tickets): < 30 seconds

---

## 26. Cost Considerations

- ~$0.10–0.50 per phase (varies by project complexity and model)
- Per-project budget cap: $5.00 (configurable)
- Jira API: free for most tiers

---

## 27. Definition of Done

- All 20 tickets accepted
- E2E demo: description → approved plan → Jira export with no circular dependencies
- Plan validity = 100% on evaluation dataset
- Security gate signed off (approval bypass tests pass)

---

## 28. Release Criteria

- CI green, Docker Compose runs, human approval obtained

---

## 29. Future Roadmap

- Streaming phase progress
- GitHub integration for code scaffold commit
- Sprint estimation and velocity modeling
- Plan revision without restarting from scratch
