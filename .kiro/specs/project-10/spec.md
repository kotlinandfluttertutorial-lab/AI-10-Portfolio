# Project Specification — P10: LLM Guard and Prompt Injection Defense Platform

**Project ID:** P10  
**Folder:** `enterprise-prompt-security/`  
**Status:** Specified  
**AI-SDLC Phase:** SPECIFY → DESIGN  
**Version:** 1.0

---

## 1. Executive Summary

AI applications are vulnerable to prompt injection, PII leakage, credential exposure, and policy violations. This platform provides a security middleware layer that scans inputs and outputs for threats, enforces content policies, detects and redacts PII and secrets, and produces an audit dashboard — acting as a security gateway between users and LLMs.

---

## 2. Problem Statement

Organizations deploying LLMs face threats that traditional WAFs cannot detect: prompt injection, jailbreaks, PII leakage in model responses, and indirect injection via retrieved documents. There is no standard, deployable security layer for LLM applications.

---

## 3. Target Users

- Security engineers auditing LLM application deployments
- Platform teams integrating LLM security into their pipeline
- Compliance officers reviewing PII handling in AI systems
- Developers building applications on top of LLMs

---

## 4. Personas

**Alex — Security Engineer:** Reviews all AI applications before production deployment. Needs a tool that intercepts LLM inputs/outputs and flags violations before they reach users or external systems.

**Sam — Platform Engineer:** Integrates the guard as a middleware in their RAG pipeline. Needs a simple SDK call: `guard.scan_input(text)` → `{ "safe": bool, "findings": [] }`.

**River — Compliance Officer:** Needs a dashboard showing: how many PII instances were detected, what types, and whether they were redacted or blocked.

---

## 5. User Journeys

**Primary (Sam — SDK integration):**
1. Adds guard SDK to their RAG application
2. Before every LLM call: `result = guard.scan_input(user_query)`
3. If `result.safe == False` and `result.severity == "critical"`: block and return error to user
4. After every LLM response: `result = guard.scan_output(llm_response)`
5. PII in the response is redacted before being returned to the user

**Alex — Audit review:**
1. Opens the audit dashboard
2. Sees: 42 prompt injection attempts in the last 7 days, 3 critical
3. Drills into critical events: sees the raw (pre-redaction) flagged content
4. Exports a security report for compliance

---

## 6. Business Goals

- Prompt injection detection rate ≥ 85% on benchmark dataset
- PII recall ≥ 90% (% of PII instances detected and redacted)
- False positive rate < 10% (benign inputs incorrectly flagged)
- Latency overhead: guard adds < 100ms to each LLM request

---

## 7. Functional Requirements

- FR-01: Input scanner: detect prompt injection, jailbreak attempts, policy violations
- FR-02: Output scanner: detect PII, secrets, policy violations in LLM responses
- FR-03: PII detection and redaction (names, emails, phone numbers, SSN, credit cards)
- FR-04: Secret detection (API keys, tokens, passwords in prompts or responses)
- FR-05: Policy engine: configurable rules for what to block, redact, or flag
- FR-06: Tool authorization: validate AI tool call requests against an allowlist
- FR-07: Proxy mode: act as a transparent LLM proxy for drop-in integration
- FR-08: SDK: Python and JavaScript clients for direct integration
- FR-09: Audit dashboard: findings by type, severity, time; individual event drill-down
- FR-10: Alert management: configurable alerts on finding thresholds

---

## 8. Non-Functional Requirements

- NFR-01: Guard processing latency < 100ms per request
- NFR-02: False positive rate < 10% on standard enterprise chat inputs
- NFR-03: PII content is redacted before storage in audit logs
- NFR-04: Detection models are versioned and updatable without downtime
- NFR-05: Audit log is append-only and tamper-resistant

---

## 9. System Architecture

```
[Application] → [Guard SDK] → [Scan API (POST /v1/scan/input)]
                                        ↓
                            [Injection Detector (rule + LLM)]
                            [PII Detector (NER model)]
                            [Secret Detector (pattern matching)]
                            [Policy Engine]
                                        ↓
                            [Audit Logger (append-only)]
                                        ↓
                  Verdict: { safe: bool, findings: [], redacted_text: string }

[Application] → [Guard SDK] → [Scan API (POST /v1/scan/output)]
                                        ↓ (same pipeline, output-specific rules)
```

---

## 10. Component Architecture

- `api/` — scan/input, scan/output, policies, alerts, audit, health
- `domain/` — ScanRequest, Finding, Policy, PolicyRule, AuditEvent, Alert
- `adapters/` — NER model adapter (spaCy/HuggingFace), LLM injection detector adapter, regex pattern engine
- `sdk/` — Python and JS client packages
- `evaluation/` — detection rate, PII recall, false positive rate

---

## 11. Data Architecture

Core entities: Application, ScanRequest, Finding, Policy, PolicyRule, AuditEvent, AlertRule, AlertEvent

---

## 12. Database Schema (Key Tables)

```sql
applications(id, name, api_key_hash, policy_id, created_at)
scan_requests(id, app_id, direction, content_hash, verdict, latency_ms, created_at)
findings(id, scan_id, finding_type, severity, description, position, created_at)
policies(id, app_id, name, version, rules jsonb, created_at)
audit_events(id, scan_id, finding_id, event_type, redacted, created_at)
alert_rules(id, app_id, finding_type, threshold, period_minutes, created_at)
```

---

## 13. API Specification

```
POST   /v1/scan/input          — scan user input before LLM call
POST   /v1/scan/output         — scan LLM response before delivery
GET    /v1/scan/{id}           — get scan result and findings
CRUD   /v1/policies            — manage security policies
GET    /v1/audit               — list audit events with filters
GET    /v1/audit/{id}          — get individual audit event
CRUD   /v1/alert-rules         — manage alert rules
GET    /v1/alerts              — list triggered alerts
GET    /v1/health
```

---

## 14. AI Architecture

- Injection detector: multi-layer
  1. Rule-based: regex patterns for known injection signatures
  2. LLM-based: classifier prompt that identifies injection intent in context
- PII detector: spaCy NER model + pattern rules (regex for SSN, credit cards, etc.)
- Secret detector: pattern-matching library (similar to detect-secrets)
- LLM injection detector prompt: classifies text as `{ "injection": bool, "confidence": float, "technique": string }`

---

## 15. Prompt Architecture

- Injection classification prompt: system defines injection techniques and instructs classification; user provides the text to evaluate; output is structured JSON
- Output scanning prompt: system defines PII and violation categories; user provides LLM response; output is `{ "violations": [{ "type", "value_hash", "position" }] }`
- Prompts are versioned; changes require evaluation before deployment

---

## 16. Agent Architecture

Not applicable — P10 is a security scanning service.

---

## 17. Tool Architecture

Not applicable.

---

## 18. Security Architecture

- API key authentication for SDK integrations
- PII in findings is stored as a hash + type, never the raw value (except in admin-restricted audit log with TTL)
- Audit log: append-only, write access restricted to the scan pipeline; read access restricted to admin
- Detection model updates: versioned, deployed without downtime via blue-green swap
- Guard itself is not a single point of failure: scan failures return a safe-by-default configurable verdict

---

## 19. Evaluation Architecture

Ground truth dataset: labeled injection attempts, benign inputs, PII-containing texts, clean texts.

Metrics: detection rate, false positive rate, PII recall, PII precision, secret detection rate, latency distribution

---

## 20. Observability Architecture

- Metrics: `scans_total{direction}`, `findings_total{type,severity}`, `scan_latency_ms`, `false_positive_rate`
- Alert: finding rate > threshold triggers alert; dashboard shows trend
- Audit dashboard: findings by type/severity/day, individual event drill-down

---

## 21. Deployment Architecture

```
docker-compose: postgres, redis, api, frontend (React audit dashboard)
SDK distributed as Python package (PyPI) and npm package
```

---

## 22. Testing Strategy

- Unit: injection detector rules, PII patterns, policy engine rule evaluation
- Integration: full scan pipeline with NER model
- API: scan endpoints, policy CRUD, audit log
- Security: PII storage (never raw), audit log immutability, API key isolation
- Evaluation: detection rate and FPR on labeled benchmark dataset
- E2E: SDK → scan → finding → audit log → dashboard visible

---

## 23. Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| High false positive rate | Medium | High | Evaluation gate: FPR < 10% required |
| Novel injection technique bypasses detection | Medium | Medium | Layered detection; LLM-based classifier catches semantic attacks |
| PII stored in audit log | Low | Critical | Content hashed before storage; raw only in time-limited admin view |
| Guard adds > 100ms overhead | Medium | Medium | Async scanning path for non-blocking mode; latency SLA monitored |
| Detection model update breaks scanning | Low | High | Blue-green deployment; evaluation required before swap |

---

## 24. Threat Model

Injection bypass via novel technique, PII leakage via audit log, API key leakage, false negative leaving application vulnerable. Full threat model: `docs/security/threat-model-P10.md`

---

## 25. Performance Requirements

- Guard scan latency < 100ms p99 per request
- PII detection: < 50ms for inputs under 2000 tokens
- LLM injection classifier: < 500ms (acceptable for async mode)

---

## 26. Cost Considerations

- LLM injection classifier: ~$0.001 per scan (used only for edge cases; rule-based is free)
- NER model: local, no cost
- Storage: ~500 bytes per scan record; 1M scans/month = 500MB

---

## 27. Definition of Done

- Detection rate ≥ 85% and FPR < 10% on evaluation benchmark
- PII recall ≥ 90%
- No raw PII in audit log (tested)
- E2E demo passes

---

## 28. Release Criteria

- CI green, Docker Compose runs, PyPI package installable, human approval obtained

---

## 29. Future Roadmap

- JavaScript/TypeScript SDK
- OpenAI API proxy mode (drop-in replacement)
- Custom injection detection model fine-tuning
- Real-time streaming scan for token-by-token output scanning
- Integration with SIEM systems (Splunk, Elastic)
