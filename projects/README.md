# Projects Directory

This folder provides a canonical reference to all 10 project source folders.

The actual project source code lives in named folders at the repository root. This directory exists to satisfy the portfolio structure spec and provide a single-place index.

## Project Mapping

| Spec ID | Source Folder | Description |
|---|---|---|
| project-01-rag | `../rag-evaluation-platform/` | Enterprise Knowledge Intelligence Platform |
| project-02-research-agent | `../autonomous-research-agent/` | Autonomous Market Research Analyst |
| project-03-support-copilot | `../customer-support-copilot/` | Smart Customer Service Assistant |
| project-04-voice-agent | `../voice-task-assistant/` | Voice-Based Appointment and Task Assistant |
| project-05-agentops | `../agentops-observability/` | AI Agent Monitoring and Reliability Platform |
| project-06-data-extraction | `../document-extraction-pipeline/` | Intelligent Invoice and Contract Processing |
| project-07-multi-agent | `../multi-agent-delivery-orchestrator/` | AI Software Project Delivery Orchestrator |
| project-08-search | `../enterprise-semantic-search/` | Context-Aware Enterprise Search Engine |
| project-09-code-review | `../github-code-review-ai/` | AI Pull Request Review and Quality Assistant |
| project-10-prompt-security | `../enterprise-prompt-security/` | LLM Guard and Prompt Injection Defense |

## Usage

Open the project's source folder directly as a Kiro workspace to get per-project steering and specs. The portfolio root is for cross-project governance, architecture decisions, and Kiro prompts in the canonical `docs/jira/` layout.

## Structure Each Project Will Have (When Implemented)

```
<project-folder>/
├── api/
├── domain/
├── adapters/
├── workers/
├── evaluation/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── security/
├── migrations/
├── .env.example
├── docker-compose.yml
├── README.md
├── ARCHITECTURE.md
├── API.md
├── SECURITY.md
├── EVALUATION.md
├── DEPLOYMENT.md
├── OPERATIONS.md
└── CONTRIBUTING.md
```
