# Kiro Implementation Prompt

**Project:** P01 — Enterprise Knowledge Intelligence Platform  
**Jira:** P01-02  
**AI-SDLC Phase:** DESIGN  
**Title:** Document system architecture and key technical decisions

---

## Objective

Write the `ARCHITECTURE.md` document and at least two Architecture Decision Records (ADRs) for the Enterprise Knowledge Intelligence Platform. This is a documentation-only ticket — no application code is written. The output is the technical design record that guides all implementation tickets.

---

## Context

**Project folder:** `rag-evaluation-platform/`  
**Project spec:** `.kiro/specs/project-01/spec.md` — sections 9–15 cover system, component, data, API, AI, prompt, and agent architecture  
**Architecture steering:** `.kiro/steering/architecture.md`  
**Documentation steering:** `.kiro/steering/documentation.md`  
**Prerequisite:** P01-01 (repo initialized)

The architecture to document:
- Upload API → Ingestion Queue (Redis) → Parser/Chunker Worker → Embedding Service → pgvector Index
- Query API → Hybrid Retriever (BM25 + pgvector) → Reranker → Grounded LLM Response with Citations → Evaluation Pipeline

---

## Dependencies

- P01-01 completed (repo skeleton exists)

---

## Implementation Requirements

1. **ARCHITECTURE.md** at `rag-evaluation-platform/ARCHITECTURE.md` covering:
   - System overview and purpose
   - Ingestion flow (text-based component diagram)
   - Query flow (text-based component diagram)
   - Component responsibilities table (api, domain, adapters, workers, evaluation)
   - Database schema overview (entities and key relationships)
   - External dependencies (OpenAI, pgvector, Redis)
   - Failure modes and recovery behavior
   - Scalability notes (stateless workers, horizontal scaling)

2. **ADR-001:** `docs/architecture/ADR-001-postgresql-pgvector-for-vector-storage.md`
   - Why PostgreSQL + pgvector over Pinecone/Chroma
   - Trade-offs, alternatives considered

3. **ADR-002:** `docs/architecture/ADR-002-hybrid-search-rrf-fusion.md`
   - Why RRF over linear combination for hybrid search
   - Formula documented, alternatives considered

4. **ADR-003 (optional):** `docs/architecture/ADR-003-openai-embedding-provider.md`
   - Provider abstraction rationale
   - How to switch providers without domain code changes

---

## Technical Constraints

- Documentation must reflect the planned implementation, not an idealized future state
- All ADRs follow the format in `.kiro/steering/documentation.md` section 5
- No "TODO" sections in a committed architecture document
- Component diagrams use ASCII/text art (no external image tools required)

---

## Files to Inspect

- `.kiro/specs/project-01/spec.md` — full architecture sections
- `rag-evaluation-platform/` — current file structure from P01-01
- `.kiro/steering/documentation.md` — ADR format, required document sections
- `.kiro/steering/architecture.md` — technology defaults to reference

---

## Expected Changes

**Documentation:**
- `rag-evaluation-platform/ARCHITECTURE.md` (new)
- `docs/architecture/ADR-001-postgresql-pgvector-for-vector-storage.md` (new)
- `docs/architecture/ADR-002-hybrid-search-rrf-fusion.md` (new)

---

## Acceptance Criteria

1. `ARCHITECTURE.md` exists and covers both ingestion and query flows with diagrams
2. Each flow diagram is readable in a plain text editor
3. At least 2 ADRs exist in `docs/architecture/` following the standard format
4. Component responsibilities table is present
5. Failure modes section describes at least 3 failure scenarios with recovery behavior
6. No section contains "TODO" or placeholder text

---

## Testing

- Documentation review: verify all required sections from `.kiro/steering/documentation.md` are present
- Cross-reference: verify ARCHITECTURE.md component list matches the planned module structure from P01-01

---

## AI-SDLC Verification

Before completing:
1. Read every section of ARCHITECTURE.md and verify it is accurate to the spec
2. Verify ADRs follow the required format exactly
3. Verify no claimed functionality is not also in the spec
4. Verify component diagrams are correct ASCII and readable

---

## Human Approval Required

- Architecture decisions (tech lead must review and approve ADRs before implementation begins)
- Any deviations from the spec architecture

---

## Definition of Done

- [ ] ARCHITECTURE.md complete with all required sections
- [ ] At least 2 ADRs in correct format
- [ ] Tech lead has reviewed and approved architecture decisions
- [ ] No placeholder text in any document
- [ ] Human reviewer approved PR

---

## Output Report

Kiro must report:
- Files created (list)
- Sections covered in ARCHITECTURE.md
- ADRs written (titles)
- Any architecture gaps or ambiguities found
- Decisions requiring human review
- **Jira status recommendation:** Ready for Code Review (documentation review)
