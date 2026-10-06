# Project Specification — P01: Enterprise Knowledge Intelligence Platform

**Project ID:** P01  
**Folder:** `rag-evaluation-platform/`  
**Status:** Specified  
**AI-SDLC Phase:** SPECIFY → DESIGN  
**Version:** 1.0

---

## 1. Executive Summary

Enterprise teams lose productivity searching for information scattered across documents, wikis, and shared drives. This platform ingests organizational documents, indexes them with hybrid search and vector embeddings, and delivers grounded answers with citations — so users get accurate, sourced answers rather than hunting through files.

---

## 2. Problem Statement

Knowledge workers spend 20–35% of their time searching for information. Existing search tools return documents, not answers. AI assistants hallucinate and cite sources that don't exist. There is no way to verify whether an AI-generated answer is actually supported by company documentation.

---

## 3. Target Users

- Knowledge workers who need accurate answers from internal documentation
- Engineering teams searching technical runbooks, architecture docs, and APIs
- Support agents needing product documentation answers
- Platform teams managing document ingestion and workspace configuration

---

## 4. Personas

**Alex — Senior Engineer:** Needs to find architecture decisions and API specs quickly. Frustrated by Confluence search returning irrelevant pages. Needs answers, not links.

**Maria — Support Lead:** Handles 50+ tickets/day. Needs accurate product answers with exact source references. Cannot afford hallucinated answers reaching customers.

**Dev — Platform Admin:** Manages document workspaces, controls access, monitors ingestion health, and tracks token costs.

---

## 5. User Journeys

**Primary (Alex):**
1. Uploads a PDF architecture doc to a workspace
2. Asks: "What database does the payments service use?"
3. Gets a grounded answer with citation to the exact page/section
4. Clicks the citation to verify the source

**Admin (Dev):**
1. Creates a workspace, sets access controls
2. Monitors ingestion queue for failures
3. Reviews token usage dashboard
4. Re-indexes after a document is updated

---

## 6. Business Goals

- Reduce time-to-answer for internal knowledge queries by 60%
- Eliminate citation hallucinations (faithfulness ≥ 0.90)
- Support multi-tenant document isolation for enterprise customers
- Demonstrate RAG evaluation methodology (Recall@k, MRR, faithfulness)

---

## 7. Functional Requirements

- FR-01: Upload PDF, DOCX, and plain text files to named workspaces
- FR-02: Parse and chunk documents with configurable strategies
- FR-03: Generate embeddings and store in pgvector
- FR-04: Support hybrid search (keyword BM25 + semantic vector)
- FR-05: Rerank retrieved passages with a cross-encoder
- FR-06: Generate grounded answers with inline citations
- FR-07: Return confidence score and source references with every answer
- FR-08: Workspace-level access control (RBAC)
- FR-09: Document versioning (re-ingest updated files)
- FR-10: Evaluation pipeline for Recall@k, MRR, faithfulness, citation precision

---

## 8. Non-Functional Requirements

- NFR-01: p99 query latency < 3s (excluding first-token streaming)
- NFR-02: Ingestion throughput ≥ 10 documents/minute on standard hardware
- NFR-03: Multi-tenant isolation: tenant A cannot retrieve tenant B's documents by design
- NFR-04: No secrets in logs or API responses
- NFR-05: Dependency scan passes on every CI build
- NFR-06: A new developer can run the full stack locally in under 15 minutes

---

## 9. System Architecture

```
[Upload API] → [Ingestion Queue (Redis)] → [Parser/Chunker Worker]
                                                    ↓
                                         [Embedding Service (OpenAI/local)]
                                                    ↓
                                         [pgvector Index]

[Query API] → [Hybrid Retriever] → [Reranker] → [LLM (grounded)] → [Answer + Citations]
                                                        ↓
                                              [Evaluation Pipeline]
```

---

## 10. Component Architecture

- `api/` — FastAPI routers: documents, search, answers, evaluations, health
- `domain/` — Workspace, Document, Chunk, Query, Answer entities and use cases
- `adapters/` — OpenAI embedding adapter, LLM adapter, pgvector adapter
- `workers/` — Ingestion worker (parse → chunk → embed → index)
- `evaluation/` — RAGAS-based evaluation runner

---

## 11. Data Architecture

Core entities: Workspace, Document, DocumentVersion, Chunk, Embedding, Query, RetrievedPassage, Answer, Citation, EvaluationRun, Feedback

Key relationships:
- Workspace 1:N Documents
- Document 1:N Chunks
- Chunk 1:1 Embedding
- Query 1:N RetrievedPassages → 1 Answer → N Citations

---

## 12. Database Schema (Key Tables)

```sql
workspaces(id, name, owner_id, created_at, updated_at)
documents(id, workspace_id, title, file_hash, status, version, created_at)
chunks(id, document_id, content, chunk_index, metadata jsonb, created_at)
embeddings(id, chunk_id, model_version, vector vector(1536), created_at)
queries(id, workspace_id, user_id, text, created_at)
answers(id, query_id, text, model, tokens_used, latency_ms, created_at)
citations(id, answer_id, chunk_id, relevance_score, created_at)
evaluation_runs(id, workspace_id, dataset_version, metrics jsonb, created_at)
```

---

## 13. API Specification

```
POST   /v1/workspaces
POST   /v1/workspaces/{id}/documents
GET    /v1/workspaces/{id}/documents
GET    /v1/documents/{id}
POST   /v1/search          — hybrid retrieval, returns ranked passages
POST   /v1/answers         — grounded answer generation with citations
POST   /v1/evaluations     — run evaluation against a dataset
POST   /v1/feedback        — user feedback on an answer
GET    /v1/health
GET    /v1/ready
```

All responses follow the portfolio error envelope. See `docs/api/api-style-guide.md`.

---

## 14. AI Architecture

- Embedding model: text-embedding-3-small (configurable via adapter)
- Retrieval: pgvector cosine similarity + PostgreSQL full-text search, fused with RRF
- Reranker: cross-encoder (ms-marco or Cohere Rerank via adapter)
- LLM: GPT-4o (configurable) — system prompt enforces grounding, cites chunk IDs
- All AI calls are budget-limited, logged (metadata only), and retried with backoff

---

## 15. Prompt Architecture

- System prompt: instructs model to answer only from provided context, cite chunk IDs, acknowledge uncertainty
- User turn: question + retrieved context passages
- Output format: structured JSON `{ "answer": string, "citations": [chunk_id], "confidence": float }`
- Prompt templates versioned in `domain/prompts/`

---

## 16. Agent Architecture

Not applicable — P01 is a pipeline, not an agent loop.

---

## 17. Tool Architecture

Not applicable — LLM is used for generation only, not tool calling.

---

## 18. Security Architecture

- JWT authentication for user-facing APIs; API key for service ingestion
- Workspace isolation: all database queries include `workspace_id` from authenticated context
- File upload validation: MIME type, extension allowlist, max size 50MB
- Prompt injection: user queries are inserted into a parameterized slot, never into system instructions
- PII: user query text is not logged in plain text; anonymized `user_id` hash only

---

## 19. Evaluation Architecture

```
evaluation/datasets/v1.0/eval_set.jsonl   — question, expected_chunks, expected_answer
evaluation/metrics/recall.py              — Recall@k implementation
evaluation/metrics/mrr.py                 — MRR implementation
evaluation/metrics/faithfulness.py        — RAGAS faithfulness
evaluation/runners/run_eval.py            — full evaluation run script
evaluation/reports/                       — timestamped JSON reports
evaluation/regression/baseline.json       — baseline to compare against
```

Key metrics: Recall@5, MRR, Faithfulness, Citation Precision, Answer Relevance, Latency p95

---

## 20. Observability Architecture

- Structured logs: every request logs `request_id`, `workspace_id`, `event`, `duration_ms`, `status`
- Metrics: `http_requests_total`, `ingestion_jobs_total`, `ai_tokens_used_total`, `retrieval_latency_seconds`
- Health: `GET /health`, `GET /ready` (checks db + redis + embedding service)
- AI cost estimate: logged per query from token count × model price

---

## 21. Deployment Architecture

```
docker-compose:
  - postgres (with pgvector extension)
  - redis
  - api (FastAPI, uvicorn)
  - worker (ingestion worker)
  - frontend (React, nginx)
```

Production: Kubernetes or ECS with separate scaling for API and worker.

---

## 22. Testing Strategy

- Unit: domain logic, chunking strategies, prompt construction, metric calculations
- Integration: ingestion pipeline end-to-end with real PostgreSQL
- API: every endpoint, auth/authz, validation, error envelope
- Security: workspace isolation, file upload abuse, prompt injection
- E2E: upload → chunk → embed → query → answer with citation
- AI evaluation: RAGAS metrics against versioned dataset

---

## 23. Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Hallucinated citations | Medium | High | Grounding enforcement in prompt + citation precision metric |
| Stale index after re-upload | Medium | Medium | Document versioning + re-index job |
| Embedding model deprecation | Low | High | Model version stored with each embedding; migration path documented |
| Tenant data leakage | Low | Critical | Workspace ID in every query + integration test for isolation |
| Token cost overrun | Medium | Medium | Per-request budget cap + cost dashboard |

---

## 24. Threat Model

Key threats: tenant data leakage via missing workspace filter, prompt injection via user query, file upload abuse (malicious content, oversized files), API key leakage, denial of service via large file uploads.

Mitigations: see Security Architecture above. Full threat model: `docs/security/threat-model-P01.md`

---

## 25. Performance Requirements

- Query end-to-end p99 < 3s (retrieval + reranking + LLM generation)
- Ingestion: 10 docs/min on 2-core/4GB worker
- Embedding batch size: 100 chunks per API call
- Database: queries with workspace_id filter must use indexes (EXPLAIN ANALYZE verified)

---

## 26. Cost Considerations

- text-embedding-3-small: ~$0.02/1M tokens — batch ingestion cost manageable
- GPT-4o: ~$15/1M input tokens — enforce max 3k context tokens per query
- Budget cap: $0.05 per query, $5/day per workspace by default (configurable)
- Cost tracked in evaluation reports per run

---

## 27. Definition of Done

- All 20 Jira tickets accepted by human reviewer
- End-to-end demo: upload → query → answer with citation passes
- Evaluation: Recall@5 ≥ baseline, Faithfulness ≥ 0.90 on eval dataset
- Security gate checklist completed and signed off
- All tests passing (unit, integration, API, security)
- Documentation complete: README, ARCHITECTURE.md, API.md, SECURITY.md, EVALUATION.md

---

## 28. Release Criteria

- CI pipeline green (lint, type-check, security scan, all tests)
- Docker Compose `up` runs cleanly from README
- Human approval (Gate G5) obtained
- Known limitations documented

---

## 29. Future Roadmap

- Streaming answer generation (server-sent events)
- Multi-modal ingestion (images, tables)
- Feedback-driven re-ranking fine-tuning
- Multi-workspace federated search
- Self-hosted embedding model option
