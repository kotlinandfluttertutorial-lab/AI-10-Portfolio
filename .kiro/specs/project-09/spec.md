# Project Specification — P09: AI Pull Request Review and Quality Assistant

**Project ID:** P09  
**Folder:** `github-code-review-ai/`  
**Status:** Specified  
**AI-SDLC Phase:** SPECIFY → DESIGN  
**Version:** 1.0

---

## 1. Executive Summary

Code review is a bottleneck in software delivery. Reviewers miss security vulnerabilities, style violations, and logical errors — especially under time pressure. This GitHub App automates the first pass of code review: it analyzes PR diffs, runs static analysis, generates AI review comments with severity labels, and posts findings as GitHub review comments and Check runs — while requiring human approval before any auto-merge action.

---

## 2. Problem Statement

Engineering teams merge code with unreviewed security vulnerabilities, inconsistent patterns, and undocumented changes. Human reviewers are overwhelmed and cannot review every PR thoroughly. There is no systematic way to detect security anti-patterns across all PRs.

---

## 3. Target Users

- Developers receiving automated review feedback before human review
- Tech leads who configure review rules and security policies
- Engineering managers monitoring PR quality metrics

---

## 4. Personas

**Casey — Developer:** Opens a PR with 300-line diff. Wants AI to catch obvious issues (hardcoded secrets, missing error handling, SQL injection risk) before the human reviewer gets to it.

**Jordan — Tech Lead:** Configures which rules are enforced per repository. Wants finding precision ≥ 80% — no noise. Reviews the AI summary before approving the PR.

---

## 5. User Journeys

**Primary (Casey):**
1. Pushes branch, opens PR on GitHub
2. GitHub webhook fires → AI Review App receives event
3. App fetches diff, runs static analysis + AI review
4. Posts inline comments on specific diff lines with severity (info, warning, error)
5. Creates a GitHub Check with pass/fail based on critical findings
6. Casey fixes critical findings, re-runs review

**Jordan:**
1. Opens repository settings in the review app
2. Configures: "block PRs with critical security findings"
3. Views PR quality metrics: findings per PR, false positive rate

---

## 6. Business Goals

- Finding precision ≥ 80% (reported findings that are real issues)
- Finding recall ≥ 60% (real issues that are detected)
- Zero auto-merge without explicit human approval
- Human PR review time reduced by 30%

---

## 7. Functional Requirements

- FR-01: GitHub App installation and webhook handling (PR opened, synchronize, reopened)
- FR-02: Fetch PR diff via GitHub API
- FR-03: Run static analysis (AST-based or tool-based) on changed files
- FR-04: AI code review: generate inline findings with severity, line reference, explanation
- FR-05: Security finding detection: hardcoded secrets, SQL injection patterns, unsafe deserialization
- FR-06: Post review comments via GitHub API
- FR-07: Create GitHub Check run with pass/fail verdict
- FR-08: Human approval workflow: block merge on critical findings until developer resolves or tech lead overrides
- FR-09: Review history and analytics dashboard
- FR-10: Per-repo configuration (rules, severity thresholds, enabled checks)

---

## 8. Non-Functional Requirements

- NFR-01: PR review completes in < 3 minutes for a 500-line diff
- NFR-02: No auto-merge without human approval (hard requirement)
- NFR-03: GitHub webhook verified via HMAC signature before processing
- NFR-04: PR code content not stored longer than the review session (ephemeral)
- NFR-05: False positive rate < 20% (measured in evaluation)

---

## 9. System Architecture

```
[GitHub Webhook] → [Webhook Handler API] → [Review Job Queue]
                                                    ↓
                                          [Diff Fetcher (GitHub API)]
                                                    ↓
                                          [Static Analyzer]
                                                    ↓
                                          [AI Review Generator (LLM)]
                                                    ↓
                                          [Finding Aggregator]
                                                    ↓
                              [GitHub Comment Poster + Check Run Creator]
                                                    ↓
                              [Human Approval Gate (for blocking decisions)]
```

---

## 10. Component Architecture

- `api/` — webhooks, reviews, configurations, analytics, health
- `domain/` — PR, DiffFile, Finding, ReviewComment, CheckRun, ReviewConfiguration
- `adapters/` — GitHub API adapter, LLM adapter, static analysis adapter
- `workers/` — review worker

---

## 11. Data Architecture

Core entities: Installation, Repository, PRReview, DiffFile, Finding, ReviewComment, CheckRun, ReviewConfiguration

---

## 12. Database Schema (Key Tables)

```sql
installations(id, github_installation_id, account_login, created_at)
repositories(id, installation_id, full_name, config jsonb, created_at)
pr_reviews(id, repo_id, pr_number, sha, status, finding_count, created_at)
diff_files(id, review_id, filename, additions, deletions)
findings(id, review_id, file_id, line_number, severity, category, description, created_at)
review_comments(id, review_id, github_comment_id, created_at)
check_runs(id, review_id, github_check_run_id, conclusion, created_at)
```

---

## 13. API Specification

```
POST   /v1/webhooks/github              — receive GitHub webhook events
GET    /v1/reviews/{id}                 — get review results
GET    /v1/repositories/{id}/reviews    — list PR reviews for a repo
CRUD   /v1/repositories/{id}/config     — manage review configuration
GET    /v1/analytics/findings           — finding frequency by category and severity
GET    /v1/health
```

---

## 14. AI Architecture

- LLM prompt: system defines review standards, security patterns, and output schema; user provides diff file content
- Output: array of `{ "file": string, "line": int, "severity": "info|warning|error|critical", "category": string, "description": string }`
- Static analysis: runs AST-based checks (bandit for Python, semgrep patterns) before LLM to catch deterministic issues cheaply
- LLM review focuses on: logic errors, design issues, documentation gaps, and patterns static analysis misses

---

## 15. Prompt Architecture

- Review prompt: system defines finding schema and standards; user provides diff content per file
- File content truncated to max 4000 tokens; long files reviewed in chunks
- Prompt templates versioned in `domain/prompts/`

---

## 16. Agent Architecture

Not applicable — pipeline, not agent loop. Each PR review is a single-pass workflow.

---

## 17. Tool Architecture

Read-only GitHub tools:
- `github.get_pull_request_diff(repo, pr_number)`
- `github.get_file_content(repo, sha, path)`

Write tools (used only after review completes):
- `github.create_review_comments(repo, pr_number, comments)` — called once per review
- `github.create_check_run(repo, sha, conclusion)` — called once per review

No human approval required for comment posting (read-only to users; comments are advisory). Human approval required only for blocking merge (critical finding enforcement).

---

## 18. Security Architecture

- GitHub webhook: HMAC-SHA256 signature verification on every event
- GitHub App private key: stored as environment variable, never in logs or code
- PR code content: ephemeral — fetched for review, processed in memory, not persisted in database
- Finding privacy: PR content not sent to third-party services other than the LLM provider
- RBAC: repository owners can configure rules; other users can only view their own PRs

---

## 19. Evaluation Architecture

Metrics: finding precision, finding recall, false positive rate, false negative rate, review latency

Ground truth dataset: curated PRs with known bugs, security vulnerabilities, and clean diffs.

---

## 20. Observability Architecture

- Metrics: `pr_reviews_total`, `findings_total{severity}`, `review_latency_seconds`, `false_positive_rate`
- Logs: review job events (PR number, repo, finding count, no code content)

---

## 21. Deployment Architecture

```
docker-compose: postgres, redis, api, review-worker, frontend (React analytics dashboard)
GitHub App: registered at github.com/settings/apps
```

---

## 22. Testing Strategy

- Unit: finding aggregator, severity classifier, diff parser
- Integration: full review pipeline with mocked GitHub API and LLM
- API: webhook HMAC validation, review CRUD, config management
- Security: webhook spoofing, unauthorized repository access, code content persistence check
- E2E: PR opened → review completed → comments posted → check run created

---

## 23. Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| High false positive rate | Medium | High | Evaluation gate: FPR < 20% required |
| GitHub API rate limit | Medium | Medium | Request queuing; respect X-RateLimit headers |
| LLM review misses critical vulnerability | Medium | Medium | Complement with static analysis (bandit, semgrep) |
| Webhook spoofing | Low | High | HMAC verification on all events |
| Code content stored in logs | Low | High | No code content in structured logs |

---

## 24. Threat Model

Webhook spoofing, GitHub App private key exposure, code content leakage, unauthorized repository access. Full threat model: `docs/security/threat-model-P09.md`

---

## 25. Performance Requirements

- PR review < 3 minutes for 500-line diff
- Static analysis < 30s for 500-line diff
- GitHub comment posting < 5s after review completes

---

## 26. Cost Considerations

- LLM review: ~$0.05–0.20 per PR (varies by diff size)
- Static analysis: free (local tools)
- Per-PR budget cap: $0.50 (configurable)

---

## 27. Definition of Done

- Finding precision ≥ 80%, recall ≥ 60% on evaluation dataset
- Zero auto-merges without human approval in security tests
- Webhook HMAC verification tested
- E2E demo passes

---

## 28. Release Criteria

- CI green, GitHub App installable, Docker Compose runs, human approval obtained

---

## 29. Future Roadmap

- GitLab MR support
- Test coverage analysis as part of review
- PR description quality scoring
- Review trend notifications (weekly digest)
