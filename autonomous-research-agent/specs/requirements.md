# Requirements — Autonomous Market Research Analyst

## Product outcome
Research work is fragmented across sources and requires repeatable planning, evidence collection, synthesis, and citation.

## Personas
Business analysts, product managers, researchers, strategy teams

## User stories and acceptance criteria

### US-01: Start the primary workflow
As a user, I want to submit a valid request so that the system can begin the main workflow.
- Given valid input, when I submit it, then the system returns a stable identifier and initial status.
- Invalid or unsupported input is rejected with field-level guidance.
- Duplicate submissions are handled according to documented idempotency rules.

### US-02: Inspect workflow progress
As a user, I want to see status and results so that I can understand what the system has done.
- Status transitions are persisted and visible.
- Failure states include a safe, actionable explanation.
- Long-running work can be refreshed without creating duplicate work.

### US-03: Review AI output
As a user, I want to inspect AI output and its supporting context so that I can correct errors before relying on it.
- Output conforms to a validated schema.
- Supporting evidence or decision reasons are shown where applicable.
- Uncertain or policy-sensitive outcomes are routed to review.

### US-04: Configure and operate the system
As an administrator, I want to manage settings and monitor operation.
- Access is role-checked.
- Configuration changes are validated and audited.
- Health and key operational metrics are available.

### US-05: Evaluate quality
As an engineer, I want to run repeatable tests against a fixed dataset.
- Evaluation inputs and versions are stored.
- Results include per-case details and aggregate metrics.
- A regression can be compared with a prior run.

## Project-specific capabilities
- Research workspace and job creation
- Goal decomposition and planning
- Search provider abstraction
- Safe web retrieval and content normalization
- Evidence ledger with source metadata
- Duplicate source detection
- Research graph orchestration
- Tool-call budgets and loop limits
- Finding extraction and claim tracking
- Citation verification
- Report generation
- Human approval and revision flow
- Job pause, resume, and cancellation
- Progress and trace viewer
- Export to Markdown and PDF
- Prompt and model configuration
- Authentication and role permissions
- Evaluation scenarios and scoring
- Observability and cost tracking
- Containerized deployment and demo

## Acceptance boundaries
- The MVP supports one documented deployment topology.
- External provider availability is not treated as an application success criterion; failures must be handled and surfaced.
- Quality thresholds must be set from a baseline dataset rather than invented in advance.
