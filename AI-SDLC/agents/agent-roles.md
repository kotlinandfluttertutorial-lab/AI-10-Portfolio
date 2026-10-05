# AI-SDLC Agent Roles

| Role | Work | Boundaries |
|---|---|---|
| Product analyst | Draft outcomes, stories, criteria | Human approves scope and priority |
| Architect | Propose architecture, contracts, ADRs | Human approves material decisions |
| Developer | Implement ticket-scoped code/tests | No self-approval, merge, or production deploy |
| Test engineer | Generate/run tests and report evidence | Human approves waivers and release readiness |
| Security reviewer | Threat model and inspect findings | Human accepts residual risk |
| Release engineer | Prepare artifacts, notes, rollback plan | Human approves production release |
| Operations analyst | Summarize telemetry and suggest fixes | Human approves production changes |

Use narrow, logged, revocable tool permissions. Separate authoring from approval for high-risk changes.
