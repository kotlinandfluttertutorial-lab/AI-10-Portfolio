# docs/jira — Portfolio Jira Traceability Index

This directory contains the canonical Kiro prompts for all 200 tickets across 10 projects, organized in the `PROJECT-XX-NNN.md` naming convention.

Each project subdirectory has a `README.md` with the full ticket table and a `kiro-prompts/` folder with one `.md` file per ticket.

## Project Index

| ID | Project | Folder | Tickets | Prompts |
|---|---|---|---|---|
| P01 | Enterprise Knowledge Intelligence Platform | [project-01/](project-01/) | P01-01 → P01-20 | [kiro-prompts/](project-01/kiro-prompts/) |
| P02 | Autonomous Market Research Analyst | [project-02/](project-02/) | P02-01 → P02-20 | [kiro-prompts/](project-02/kiro-prompts/) |
| P03 | Smart Customer Service Assistant | [project-03/](project-03/) | P03-01 → P03-20 | [kiro-prompts/](project-03/kiro-prompts/) |
| P04 | Voice-Based Appointment and Task Assistant | [project-04/](project-04/) | P04-01 → P04-20 | [kiro-prompts/](project-04/kiro-prompts/) |
| P05 | AI Agent Monitoring and Reliability Platform | [project-05/](project-05/) | P05-01 → P05-20 | [kiro-prompts/](project-05/kiro-prompts/) |
| P06 | Intelligent Invoice and Contract Processing | [project-06/](project-06/) | P06-01 → P06-20 | [kiro-prompts/](project-06/kiro-prompts/) |
| P07 | AI Software Project Delivery Orchestrator | [project-07/](project-07/) | P07-01 → P07-20 | [kiro-prompts/](project-07/kiro-prompts/) |
| P08 | Context-Aware Enterprise Search Engine | [project-08/](project-08/) | P08-01 → P08-20 | [kiro-prompts/](project-08/kiro-prompts/) |
| P09 | AI Pull Request Review and Quality Assistant | [project-09/](project-09/) | P09-01 → P09-20 | [kiro-prompts/](project-09/kiro-prompts/) |
| P10 | LLM Guard and Prompt Injection Defense | [project-10/](project-10/) | P10-01 → P10-20 | [kiro-prompts/](project-10/kiro-prompts/) |

## Naming Convention

Files in each `kiro-prompts/` folder are named: `PROJECT-XX-NNN.md`
- `XX` = zero-padded project number (01–10)
- `NNN` = zero-padded ticket number (001–020)

Example: `docs/jira/project-01/kiro-prompts/PROJECT-01-008.md`

## Traceability Chain

```
Jira Ticket (PXX-NN)
    ↓
Kiro Prompt (docs/jira/project-XX/kiro-prompts/PROJECT-XX-NNN.md)
    ↓
Requirement (.kiro/specs/project-XX/ or <project-folder>/specs/requirements.md)
    ↓
Design (<project-folder>/specs/design.md)
    ↓
Implementation (<project-folder>/src/ or domain/)
    ↓
Tests (<project-folder>/tests/)
    ↓
Evaluation (<project-folder>/evaluation/)
    ↓
Security (docs/security/)
    ↓
Release (docs/operations/)
```
