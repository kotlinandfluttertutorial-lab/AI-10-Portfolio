# Kiro Implementation Prompt

**Project:** P01 — Enterprise Knowledge Intelligence Platform  
**Jira:** P01-08  
**AI-SDLC Phase:** BUILD  
**Title:** PDF/DOCX/text parsing

---

## Objective

Implement document parsers for PDF, DOCX, and plain text files. Each parser accepts a file path or bytes, extracts text with position metadata, and returns a normalized list of `TextBlock` objects. Parser failures must be handled gracefully: mark the document as failed with a descriptive error message rather than crashing the ingestion worker.

---

## Context

**Project folder:** `rag-evaluation-platform/`  
**Project spec:** `.kiro/specs/project-01/spec.md` — section 10 (component architecture), section 12 (database schema)  
**Requirements:** `rag-evaluation-platform/specs/requirements.md`  
**Design:** `rag-evaluation-platform/specs/design.md`  
**Engineering steering:** `.kiro/steering/engineering.md`  
**Architecture steering:** `.kiro/steering/architecture.md`

**This ticket:** Parsing is the first step in the ingestion worker pipeline. The output feeds directly into the chunker (P01-09). Parsers live in `domain/parsers/`.

---

## Dependencies

- P01-07 completed (secure document upload and validation — files stored with document record)
- P01-03 completed (database schema with documents table)

---

## Implementation Requirements

1. **TextBlock dataclass** in `domain/models/text_block.py`:
   ```python
   @dataclass
   class TextBlock:
       content: str
       page_number: int | None
       section: str | None
       char_offset_start: int
       char_offset_end: int
       metadata: dict
   ```

2. **Parser interface** in `domain/parsers/base.py`:
   ```python
   class DocumentParser(Protocol):
       def parse(self, file_bytes: bytes, filename: str) -> list[TextBlock]: ...
   ```

3. **PDF parser** in `domain/parsers/pdf_parser.py`:
   - Use PyMuPDF (fitz) for text extraction
   - Extract text per page with page_number
   - Handle encrypted PDFs: raise `ParseError("PDF is encrypted or password-protected")`
   - Handle corrupt PDFs: raise `ParseError("PDF could not be opened: {reason}")`
   - Return empty list for pages with no extractable text (image-only pages — do not fail)

4. **DOCX parser** in `domain/parsers/docx_parser.py`:
   - Use python-docx
   - Extract paragraphs with heading detection (metadata["is_heading"] = True for styles starting with "Heading")
   - Extract table cells as separate TextBlocks with metadata["is_table_cell"] = True
   - Handle corrupt DOCX: raise `ParseError`

5. **Plain text parser** in `domain/parsers/text_parser.py`:
   - Split on double newlines for paragraph detection
   - No external dependencies

6. **Parser factory** in `domain/parsers/factory.py`:
   - `get_parser(mime_type: str) -> DocumentParser` — raises `UnsupportedFormatError` for unknown MIME types

7. **Ingestion worker integration:** In `workers/ingestion_worker.py`, call parser on the stored file bytes. On `ParseError`: update `documents.status = "parse_failed"`, log error with `document_id` and error message, continue to next job (do not crash worker).

8. **Fixture files** for testing in `tests/fixtures/`:
   - `sample.pdf` — a 3-page PDF with text content
   - `sample.docx` — a DOCX with headings, paragraphs, and a table
   - `sample.txt` — plain text with paragraphs

---

## Technical Constraints

- No document content in structured logs — log only `document_id`, `page_count`, `block_count`, `duration_ms`
- Parser errors must be `ParseError` subclass, not generic `Exception`
- PyMuPDF version pinned in requirements.txt
- python-docx version pinned in requirements.txt
- Parsers are pure functions — no database or I/O side effects
- Image-only PDF pages produce empty blocks (warn, do not fail)

---

## Files to Inspect

- `rag-evaluation-platform/domain/` — check existing structure
- `rag-evaluation-platform/workers/ingestion_worker.py` — existing worker code
- `rag-evaluation-platform/requirements.txt` — existing dependencies

---

## Expected Changes

**Backend:**
- `rag-evaluation-platform/domain/models/text_block.py` (new)
- `rag-evaluation-platform/domain/parsers/base.py` (new)
- `rag-evaluation-platform/domain/parsers/pdf_parser.py` (new)
- `rag-evaluation-platform/domain/parsers/docx_parser.py` (new)
- `rag-evaluation-platform/domain/parsers/text_parser.py` (new)
- `rag-evaluation-platform/domain/parsers/factory.py` (new)
- `rag-evaluation-platform/workers/ingestion_worker.py` (modified — add parse step)
- `rag-evaluation-platform/requirements.txt` (modified — add PyMuPDF, python-docx)

**Tests:**
- `rag-evaluation-platform/tests/unit/test_pdf_parser.py`
- `rag-evaluation-platform/tests/unit/test_docx_parser.py`
- `rag-evaluation-platform/tests/unit/test_text_parser.py`
- `rag-evaluation-platform/tests/fixtures/sample.pdf`
- `rag-evaluation-platform/tests/fixtures/sample.docx`
- `rag-evaluation-platform/tests/fixtures/sample.txt`

---

## Acceptance Criteria

1. PDF parser extracts text from a 3-page test PDF, returning ≥ 1 TextBlock per page
2. DOCX parser correctly identifies headings (`metadata["is_heading"] == True`) in test DOCX
3. Plain text parser splits a multi-paragraph test file into ≥ 2 TextBlocks
4. Corrupt PDF raises `ParseError` (tested with a truncated file)
5. Encrypted PDF raises `ParseError` with "encrypted" in the message
6. Parser factory raises `UnsupportedFormatError` for `application/zip`
7. Ingestion worker sets `documents.status = "parse_failed"` on `ParseError` and continues
8. All unit tests pass: `pytest tests/unit/test_*_parser.py -v`
9. No document content appears in structured log output

---

## Testing

- **Unit:** `test_pdf_parser.py` — parse fixture PDF, assert TextBlock count and page numbers
- **Unit:** `test_docx_parser.py` — parse fixture DOCX, assert heading detection, table cell detection
- **Unit:** `test_text_parser.py` — parse multi-paragraph text, assert block count
- **Unit:** `test_pdf_parser.py` — corrupt PDF raises ParseError
- **Integration:** ingestion worker with parse failure — document status set to parse_failed

---

## AI-SDLC Verification

Before completing:
1. Run `pytest tests/unit/test_*_parser.py -v` and report exact output
2. Verify no `content=` or similar fields appear in log output (scan structlog calls)
3. Verify PyMuPDF and python-docx are pinned in requirements.txt
4. Verify parsers have no database imports
5. Verify `ParseError` is defined and used (not `Exception`)

---

## Human Approval Required

- Choice of PyMuPDF vs. pdfplumber (if deviation from spec)
- Any parser behavior decisions for edge cases (password-protected PDFs, malformed XML in DOCX)

---

## Definition of Done

- [ ] All 3 parsers implemented and tested with fixture files
- [ ] Corrupt/encrypted PDF handled gracefully
- [ ] Integration with ingestion worker: parse failure → document status updated
- [ ] No document content in logs (verified by reviewing log output)
- [ ] All unit tests passing (exact output reported)
- [ ] Human reviewer approved PR

---

## Output Report

Kiro must report:
- Files created and modified
- Test results: `pytest tests/unit/test_*_parser.py -v` → exact output
- TextBlock counts for each fixture file
- Log output sample (must show no content field)
- Known limitations (e.g., image-only PDFs return empty blocks)
- **Jira status recommendation:** Ready for Code Review
