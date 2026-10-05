# Testing Steering File

## Overview

This file defines the testing standards, requirements, and practices that apply to all 10 projects in the AI-10 Portfolio. Tests are not optional. Every meaningful feature requires automated tests. Tests must actually run and their results must be reported accurately — never claim tests passed without running them.

---

## 1. Testing Principles

- Tests are first-class artifacts: written alongside code, not after
- Test coverage is a means, not an end — prioritize meaningful coverage of behavior over line percentage
- Never delete or weaken tests to make a failing test pass
- Test results are reported honestly: commands run, output observed, and whether tests passed or failed
- Tests must be deterministic: the same test produces the same result on every run
- Flaky tests are treated as bugs and fixed immediately
- External dependencies (AI providers, databases, external APIs) are mocked or stubbed in unit and most integration tests

---

## 2. Unit Tests

**Scope:** Individual functions, classes, and modules in isolation.

**Requirements:**
- Cover the main success path for every public function/method
- Cover all significant edge cases (empty input, boundary values, type errors)
- Cover all error/exception paths
- Use mocks or stubs for all external dependencies (database, HTTP, AI providers)
- Tests must run in under 10 seconds total for a single module's suite
- Test file naming: `test_<module_name>.py` or `<module_name>.test.ts`

**Tools:**
- Python: `pytest` with `unittest.mock` or `pytest-mock`
- TypeScript/JavaScript: `jest` or `vitest`

**Minimum coverage targets (establish baseline first, then improve):**
- Domain logic: aim for 90%+ line coverage
- Adapters: aim for 80%+ with mocked externals
- API handlers: 100% of endpoints have at least one test

---

## 3. Integration Tests

**Scope:** Interactions between two or more modules, or between a module and a real (or containerized) dependency.

**Requirements:**
- Test the critical happy path for each major workflow end-to-end within the service boundary
- Use a real test database (containerized via Docker) — do not mock the database in integration tests
- Test database is seeded with fixtures before each test run
- Cover authorization checks: authenticated requests succeed; unauthenticated/unauthorized requests fail with the right status code
- Cover failure paths: what happens when a dependency returns an error

**Tools:**
- Python: `pytest` with `docker-compose` for test dependencies
- Database: test-specific schema isolated from development schema
- Use `testcontainers` or `pytest-docker` for ephemeral containers

---

## 4. API Tests

**Scope:** HTTP API endpoints tested as a black box against the running service.

**Requirements:**
- Every API endpoint has at least one test
- Test both valid and invalid input
- Test authentication and authorization: missing token, expired token, insufficient permissions
- Test rate limiting behavior
- Test pagination where applicable
- Test error envelope format matches the documented contract
- Tests use a test client (not a live deployment) to remain deterministic

**Tools:**
- Python: `pytest` + FastAPI `TestClient` or `httpx`
- OpenAPI contract testing: `schemathesis` or `dredd`

---

## 5. End-to-End Tests

**Scope:** Full workflows from the user's perspective, exercising all layers including the UI and background jobs.

**Requirements:**
- Cover the primary user journey for each project
- Cover at least one failure/recovery scenario
- Run against a fully assembled environment (Docker Compose stack)
- E2E tests are slower and are run on CI, not on every local commit
- UI e2e tests use `Playwright` or `Cypress`
- Avoid flakiness: use explicit waits, not sleep() calls

**When required:**
- Before every release candidate
- After any change to the end-to-end workflow

---

## 6. Security Tests

**Requirements:**
- Authentication boundary: test that every protected endpoint rejects unauthenticated requests
- Authorization boundary: test that users cannot access or modify resources belonging to other users/tenants
- Input validation: test that malformed, oversized, and injection-containing inputs are rejected
- Prompt injection: test that user-supplied adversarial prompts do not hijack system behavior (for AI projects)
- Secret leakage: CI scan using `detect-secrets` or `trufflehog` on every commit
- Dependency scan: `pip-audit` or `safety` on every build

**Format:**
- Security test cases are tagged with `@security` or in a `tests/security/` directory
- Every security test documents the threat it is testing

---

## 7. Regression Tests

**Requirements:**
- Regression tests are added for every bug fix — the test must fail before the fix and pass after
- Regression tests are never deleted
- Regression test suite runs on every PR
- Regression failures block merge

**Process:**
1. Bug reported
2. Write a failing test that reproduces the bug
3. Fix the bug
4. Confirm the test passes
5. Add to regression suite

---

## 8. AI Evaluation Tests

Applies to all projects with AI components (all 10 projects have at least some AI behavior).

**Requirements:**
- A versioned evaluation dataset is created before measuring quality
- Evaluation runs are reproducible: same dataset + same model + same config = comparable results
- Baselines are established and stored before setting thresholds
- Regressions against the baseline fail the evaluation gate
- Per-case failures are inspectable (not just aggregate scores)
- Evaluation is run before every release

**Evaluation directory structure:**
```
evaluation/
├── datasets/      — versioned input datasets
├── cases/         — individual test cases with expected outputs
├── runners/       — scripts that execute evaluation runs
├── metrics/       — metric definitions and calculation code
├── reports/       — output reports from each run
└── regression/    — baseline comparisons
```

**Project-specific dimensions (examples):**

| Project | Key Metrics |
|---|---|
| P01 RAG | Recall@k, MRR, faithfulness, citation precision, answer relevance |
| P02 Research Agent | Source coverage, claim accuracy, report completeness, hallucination rate |
| P03 Support | Resolution rate, escalation accuracy, response relevance, tone |
| P04 Voice | Intent accuracy, slot fill accuracy, task completion rate |
| P05 AgentOps | Metric correctness, alert precision, ingestion accuracy |
| P06 Extraction | Field extraction accuracy, schema compliance rate, confidence calibration |
| P07 Multi-Agent | Plan validity, dependency correctness, task completion rate |
| P08 Search | NDCG, MRR, recall, query rewrite quality |
| P09 Code Review | Finding precision, finding recall, false positive rate |
| P10 Prompt Security | Detection rate, false positive rate, PII recall |

**Scoring rules:**
- Never use an arbitrary score without documenting how it is calculated
- Metric formulas are code, not prose — implement them in `evaluation/metrics/`
- Human spot-checks supplement automated metrics for quality-sensitive dimensions

---

## 9. Performance Tests

**Requirements:**
- Baseline performance is measured before optimization
- Latency is measured at p50, p95, and p99 percentiles
- Throughput is measured under realistic concurrent load
- Performance tests document: test conditions, hardware/environment, dataset size, concurrency level
- Performance regressions of >20% on p99 latency require investigation before release

**Tools:**
- `locust` or `k6` for HTTP load testing
- `pytest-benchmark` for unit-level performance tests

---

## 10. Failure and Recovery Tests

**Requirements:**
- Test that the system recovers gracefully when a dependency is unavailable (database down, AI provider down, queue full)
- Test that async jobs are retried correctly after transient failures
- Test that idempotency is preserved: replaying a job does not cause double-processing
- Test that the dead-letter queue captures permanently failed jobs
- Test that circuit breakers open and close as expected

---

## 11. Test Reporting

Every test run must produce a report containing:
- Test command executed (exact command, not a description)
- Number of tests passed, failed, and skipped
- Duration
- Names of failed tests with their error messages
- For AI evaluations: per-case results, aggregate scores, baseline comparison

**Rules:**
- Never summarize test results without running the tests
- Never report "tests passed" based on reading the code
- If tests cannot run (missing environment, missing keys), report that explicitly and explain why

---

## 12. Test Environment Requirements

- Tests requiring external services use containerized equivalents (Docker Compose)
- Environment variables for test environments are documented in `.env.test.example`
- Test databases are isolated from development databases
- CI pipelines configure test environments via their secret store; no manual setup required
- Each project's `README.md` includes a "Running tests" section with exact commands
