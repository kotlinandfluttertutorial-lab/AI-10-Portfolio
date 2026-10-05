# AI-10 Project Portfolio Engineering Pack

This pack contains 10 independent AI project workspaces. Each has a project specification, requirements and design specs, 20 Jira starter tickets, 20 linked Kiro prompts, and initial Kiro steering/spec files.

| ID | Project | Folder |
|---|---|---|
| P01 | Enterprise Knowledge Intelligence Platform | `rag-evaluation-platform/` |
| P02 | Autonomous Market Research Analyst | `autonomous-research-agent/` |
| P03 | Smart Customer Service Assistant | `customer-support-copilot/` |
| P04 | Voice-Based Appointment and Task Assistant | `voice-task-assistant/` |
| P05 | AI Agent Monitoring and Reliability Platform | `agentops-observability/` |
| P06 | Intelligent Invoice and Contract Processing System | `document-extraction-pipeline/` |
| P07 | AI Software Project Delivery Orchestrator | `multi-agent-delivery-orchestrator/` |
| P08 | Context-Aware Enterprise Search Engine | `enterprise-semantic-search/` |
| P09 | AI Pull Request Review and Quality Assistant | `github-code-review-ai/` |
| P10 | LLM Guard and Prompt Injection Defense Platform | `enterprise-prompt-security/` |

## Suggested execution order

Start with the project that best matches the role you are targeting. Within each project, implement foundation and architecture first, then the core workflow, evaluation/security, and release readiness. Treat ticket estimates and priorities as initial planning data, not commitments.

## Jira import notes

- Each project's CSV uses common Jira fields plus an Acceptance Criteria column. Jira import field names vary by instance; map Summary, Issue Type, Description, Priority, Labels, and Epic Link as supported.
- Create the epic referenced in each project's CSV before importing stories, or remove/map the Epic Link field during import.
- The 20 tickets are a starter backlog, not a promise that every feature fits one sprint. Split stories further where needed.
- Replace provider-specific choices, compliance requirements, SLOs, and cost thresholds with decisions appropriate to your environment.

## Kiro workflow

1. Open one project folder as the Kiro workspace.
2. Review `.kiro/steering/` and `.kiro/specs/`.
3. Pick a Jira ticket and open its linked prompt.
4. Ask Kiro to inspect the repository and implement only that ticket.
5. Review the diff, run tests, and update Jira with evidence.
6. Keep requirements, design, tickets, prompts, and code aligned.

## AI-SDLC framework

Shared lifecycle, agent roles, prompt template, and release checklist are in `AI-SDLC/`.
