# Project Specification — P06: Intelligent Invoice and Contract Processing System

**Project ID:** P06  
**Folder:** `document-extraction-pipeline/`  
**Status:** Specified  
**AI-SDLC Phase:** SPECIFY → DESIGN  
**Version:** 1.0

---

## 1. Executive Summary

Finance and operations teams process hundreds of invoices and contracts manually, introducing errors and delays. This platform automates document ingestion, OCR, layout detection, and structured field extraction, then routes low-confidence extractions to a human review queue — combining AI speed with human accuracy for high-stakes financial documents.

---

## 2. Problem Statement

Manual invoice processing takes 5–10 minutes per document and has a 2–5% error rate. Errors in extracted amounts or contract terms cause payment disputes and compliance issues. Existing OCR tools extract text but do not understand document structure or field semantics.

---

## 3. Target Users

- Finance teams processing invoices and purchase orders
- Legal/operations teams processing contracts
- Platform administrators managing extraction schemas and review queues

---

## 4. Personas

**Alex — Finance Analyst:** Processes 50+ invoices per day. Needs accurate amount, date, and vendor extraction. Reviews and corrects AI extractions before approving payment.

**Sam — Legal Ops:** Processes contracts for key term extraction (payment terms, termination clauses, SLA). Needs high recall — missing a term is worse than flagging one for review.

**Jordan — Platform Admin:** Creates and manages extraction schemas for different document types. Monitors extraction accuracy and queue depth.

---

## 5. User Journeys

**Primary (Alex):**
1. Uploads a PDF invoice
2. AI extracts fields: vendor name, invoice number, date, line items, total
3. High-confidence extractions are auto-accepted; low-confidence go to review queue
4. Alex reviews flagged items, corrects if needed, approves
5. Approved extraction is exported to accounting system

---

## 6. Business Goals

- Achieve field extraction accuracy ≥ 90% on standard invoices
- Reduce manual review time by 70% vs. fully manual processing
- Human review queue only for items with confidence < configurable threshold
- Full audit trail: who reviewed what, when, with what correction

---

## 7. Functional Requirements

- FR-01: Ingest PDF, TIFF, and image documents
- FR-02: Run OCR on document images (Tesseract or cloud OCR)
- FR-03: Detect document layout (header, table, footer, signature block)
- FR-04: Extract fields per schema (configurable per document type)
- FR-05: Score extraction confidence per field
- FR-06: Auto-accept high-confidence extractions; queue low-confidence for review
- FR-07: Human review UI: show document + extraction side-by-side, allow corrections
- FR-08: Export approved extractions (JSON, CSV, webhook)
- FR-09: Full audit trail: ingestion, extraction, review decision, correction, export
- FR-10: Batch processing: upload a folder of documents, track job progress

---

## 8. Non-Functional Requirements

- NFR-01: Single document processing < 30s (OCR + extraction + confidence scoring)
- NFR-02: Batch of 100 documents processed within 30 minutes
- NFR-03: Document content not logged in structured logs (only document ID and metadata)
- NFR-04: Audit log immutable and append-only
- NFR-05: Extraction schemas versioned (schema change does not break existing documents)

---

## 9. System Architecture

```
[Upload API] → [Ingestion Queue]
                    ↓
              [OCR Worker (Tesseract/cloud)]
                    ↓
              [Layout Detector (LLM vision or rule-based)]
                    ↓
              [Field Extractor (LLM + schema)]
                    ↓
              [Confidence Scorer]
                    ↓
         [Auto-accept OR Review Queue]
                    ↓
           [Human Review Interface]
                    ↓
              [Export API]
```

---

## 10. Component Architecture

- `api/` — documents, jobs, schemas, review-queue, exports, health
- `domain/` — Document, ExtractionJob, ExtractionSchema, ExtractedField, ReviewItem, AuditEvent
- `adapters/` — OCR adapter (Tesseract, AWS Textract), LLM extraction adapter, export adapter
- `workers/` — OCR worker, extraction worker
- `evaluation/` — field accuracy runner

---

## 11. Data Architecture

Core entities: Document, ExtractionJob, ExtractionSchema, ExtractedField, ReviewItem, ReviewDecision, AuditEvent, ExportRecord

---

## 12. Database Schema (Key Tables)

```sql
documents(id, user_id, filename, file_hash, status, created_at)
extraction_jobs(id, document_id, schema_id, status, created_at, completed_at)
extraction_schemas(id, name, version, field_definitions jsonb, created_at)
extracted_fields(id, job_id, field_name, value, confidence, auto_accepted, created_at)
review_items(id, job_id, field_id, status, reviewer_id, correction, created_at)
audit_events(id, document_id, event_type, actor_id, payload_hash, created_at)
```

---

## 13. API Specification

```
POST   /v1/documents              — upload document
GET    /v1/documents/{id}         — get document and extraction status
GET    /v1/jobs/{id}              — get extraction job progress
GET    /v1/review-queue           — list items awaiting review
POST   /v1/review-queue/{id}/decide — submit review decision (accept/correct)
CRUD   /v1/schemas                — manage extraction schemas
GET    /v1/documents/{id}/export  — export approved extraction
GET    /v1/health
```

---

## 14. AI Architecture

- OCR: Tesseract for local processing; AWS Textract or Google Document AI via adapter for higher accuracy
- Layout detection: LLM vision (GPT-4o vision) or rule-based heuristics
- Field extraction: LLM with schema prompt; output is structured JSON per schema definition
- Confidence scoring: LLM returns confidence per field; calibrated against human labels

---

## 15. Prompt Architecture

- Extraction prompt: system provides schema definition (field names, types, extraction rules); user provides OCR text + layout; output is `{ "field_name": { "value": any, "confidence": float } }`
- Schema prompt is versioned alongside the schema definition

---

## 16. Agent Architecture

Not applicable — pipeline, not an agent loop.

---

## 17. Tool Architecture

Not applicable for extraction pipeline.

---

## 18. Security Architecture

- JWT auth; users can only access their own documents and jobs
- Document content: not stored in structured logs; only file hash and metadata
- Audit log: append-only, restricted to admin read
- PII: financial documents contain PII — access restricted to uploading user and assigned reviewers
- Export: webhook URLs validated to prevent SSRF

---

## 19. Evaluation Architecture

Metrics: field extraction accuracy per field type, schema compliance rate, confidence calibration (correlation between confidence score and actual accuracy), review queue precision (% of queued items that actually needed correction)

---

## 20. Observability Architecture

- Metrics: `documents_processed_total`, `extraction_latency_seconds`, `review_queue_depth`, `auto_accept_rate`
- Logs: document lifecycle events (no document content)

---

## 21. Deployment Architecture

```
docker-compose: postgres, redis, api, ocr-worker, extraction-worker, frontend (React review UI)
```

---

## 22. Testing Strategy

- Unit: schema validation, confidence scorer, field extractor logic
- Integration: full ingestion → extraction → review pipeline
- API: document CRUD, review decision, export
- Security: document access isolation, export webhook SSRF, audit log immutability
- E2E: upload invoice → extraction → human review → approved export

---

## 23. Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| OCR failure on low-quality scans | High | Medium | Confidence scoring routes to review; OCR failure is a known state |
| Hallucinated field values | Medium | High | Confidence threshold + mandatory review for low-confidence |
| PII exposure in logs | Low | High | Document content excluded from structured logs |
| Schema version mismatch | Medium | Medium | Schema version stored with each extraction job |

---

## 24. Threat Model

Unauthorized document access, PII in logs, export webhook SSRF, audit log tampering. Full threat model: `docs/security/threat-model-P06.md`

---

## 25. Performance Requirements

- Single document: < 30s end-to-end
- Batch of 100: < 30 minutes
- Review UI load: < 500ms per item

---

## 26. Cost Considerations

- Tesseract: free, local
- AWS Textract: ~$1.50/1000 pages
- LLM extraction: ~$0.02–0.10 per document depending on length
- Budget per document cap: $0.50 (configurable)

---

## 27. Definition of Done

- Field accuracy ≥ 90% on test invoice dataset
- E2E demo passes
- Audit trail immutability tested
- Security gate signed off

---

## 28. Release Criteria

- CI green, Docker Compose runs, human approval obtained

---

## 29. Future Roadmap

- Real-time OCR progress streaming
- Multi-language document support
- Active learning: human corrections feed back into extraction model
- Integration with accounting systems (QuickBooks, SAP)
