# Kiro Implementation Prompt

**Project:** P01 — Enterprise Knowledge Intelligence Platform  
**Jira:** P01-16  
**AI-SDLC Phase:** VERIFY  
**Title:** Add project-specific evaluation and regression test harness

---

## Objective

Build a complete AI evaluation system for the Enterprise Knowledge Intelligence Platform. Create a versioned evaluation dataset, implement metric calculators for Recall@k, MRR, Faithfulness, Citation Precision, and Answer Relevance, write an evaluation runner script, store the baseline, and implement a regression comparison tool. This establishes the quality measurement foundation before release.

---

## Context

**Project folder:** `rag-evaluation-platform/`  
**Project spec:** `.kiro/specs/project-01/spec.md` — section 19 (evaluation architecture)  
**Evaluation framework:** `docs/evaluation/evaluation-framework.md` — P01 metrics table  
**Testing steering:** `.kiro/steering/testing.md` — section 8 (AI evaluation tests)  
**Prerequisites:** P01-15 (grounded answer generation implemented and working)

**Key principle:** Establish baselines BEFORE setting thresholds. Run evaluation first, record results, then decide on quality thresholds. Never invent evaluation scores — only report results from actual evaluation runs.

---

## Dependencies

- P01-15 completed (answer generation with citations working)
- P01-12 completed (hybrid retrieval working)
- P01-14 completed (reranker working)

---

## Implementation Requirements

1. **Evaluation dataset** at `rag-evaluation-platform/evaluation/datasets/v1.0/eval_set.jsonl`:
   - 20+ question-answer pairs
   - Each record: `{ "id", "question", "expected_chunk_ids": [...], "expected_answer_keywords": [...], "ground_truth_answer": string }`
   - Questions should cover a range of: factual lookup, multi-hop, definition, comparison
   - Use synthetic domain content (not real proprietary data)

2. **Metric implementations:**
   - `evaluation/metrics/recall.py` — `recall_at_k(retrieved_ids, relevant_ids, k) -> float`
   - `evaluation/metrics/mrr.py` — `mean_reciprocal_rank(ranked_ids, relevant_ids) -> float`
   - `evaluation/metrics/faithfulness.py` — RAGAS faithfulness using LLM-as-judge. If RAGAS unavailable, implement simple overlap metric with LLM judge prompt
   - `evaluation/metrics/citation_precision.py` — `citation_precision(cited_ids, relevant_ids) -> float`
   - `evaluation/metrics/answer_relevance.py` — LLM-as-judge: is the answer relevant to the question? Returns 0.0–1.0

3. **Evaluation runner** at `evaluation/runners/run_eval.py`:
   ```
   python evaluation/runners/run_eval.py \
     --dataset evaluation/datasets/v1.0/eval_set.jsonl \
     --output evaluation/reports/YYYYMMDD_HHMMSS.json
   ```
   - For each question: call the full RAG pipeline (retrieve → rerank → answer)
   - Compute all metrics per case
   - Aggregate results
   - Write timestamped JSON report

4. **Baseline storage:** After first run, copy output to `evaluation/regression/baseline.json`

5. **Regression comparison** at `evaluation/runners/compare_baseline.py`:
   ```
   python evaluation/runners/compare_baseline.py \
     --baseline evaluation/regression/baseline.json \
     --current evaluation/reports/latest.json
   ```
   - Print per-metric comparison: current vs baseline, delta, pass/fail (fail if delta < -0.05)

6. **Report format** (JSON):
   ```json
   {
     "run_id": "eval_YYYYMMDD_HHMMSS",
     "dataset_version": "v1.0",
     "model": "gpt-4o-...",
     "timestamp": "...",
     "aggregate_metrics": { "recall_at_5": 0.0, "mrr": 0.0, "faithfulness": 0.0, "citation_precision": 0.0, "answer_relevance": 0.0 },
     "per_case_results": [{ "case_id": "...", "question": "...", "recall_at_5": 0.0, "faithfulness": 0.0, "passed": true }]
   }
   ```

---

## Technical Constraints

- Evaluation dataset must not contain real proprietary or personal data
- Metric formulas must be implemented as code — not described only in prose
- LLM calls in metrics use the same provider adapter as the application
- Evaluation runner must work with `OPENAI_API_KEY` set in the environment
- Never invent or estimate metric scores — only report values from actual evaluation runs
- If evaluation cannot run (missing API key), report that clearly and explain why

---

## Files to Inspect

- `rag-evaluation-platform/domain/` — existing RAG pipeline components
- `rag-evaluation-platform/api/` — search and answer endpoints to call
- `docs/evaluation/evaluation-framework.md` — metric definitions
- `.kiro/steering/testing.md` section 8 — evaluation requirements

---

## Expected Changes

**Evaluation:**
- `rag-evaluation-platform/evaluation/__init__.py`
- `rag-evaluation-platform/evaluation/datasets/v1.0/eval_set.jsonl` (20+ records)
- `rag-evaluation-platform/evaluation/metrics/recall.py`
- `rag-evaluation-platform/evaluation/metrics/mrr.py`
- `rag-evaluation-platform/evaluation/metrics/faithfulness.py`
- `rag-evaluation-platform/evaluation/metrics/citation_precision.py`
- `rag-evaluation-platform/evaluation/metrics/answer_relevance.py`
- `rag-evaluation-platform/evaluation/runners/run_eval.py`
- `rag-evaluation-platform/evaluation/runners/compare_baseline.py`
- `rag-evaluation-platform/evaluation/regression/baseline.json` (after first run)
- `rag-evaluation-platform/evaluation/reports/` (directory, first report after run)

**Tests:**
- `rag-evaluation-platform/tests/unit/test_metrics.py` — unit tests for metric formulas
- `rag-evaluation-platform/EVALUATION.md` — updated with runner commands and baseline results

---

## Acceptance Criteria

1. `pytest tests/unit/test_metrics.py -v` passes — metric formulas return correct values for known inputs
2. `python evaluation/runners/run_eval.py --dataset ... --output ...` runs without error and produces a valid JSON report
3. Report contains per-case results (not just aggregate)
4. `evaluation/regression/baseline.json` stored with actual results from the first run
5. `python evaluation/runners/compare_baseline.py --baseline ... --current ...` runs and prints metric deltas
6. `EVALUATION.md` updated with: metric definitions, dataset description, runner commands, actual baseline results with date and model version

---

## Testing

- **Unit:** `test_metrics.py` — test Recall@5 with known inputs (e.g., retrieved=[1,2,3,4,5], relevant=[3], expected=1.0)
- **Unit:** test MRR with known inputs
- **Unit:** test citation_precision with known inputs
- **Integration:** run evaluation runner on 3 questions (subset) and verify report structure

---

## AI-SDLC Verification

Before completing:
1. Run `pytest tests/unit/test_metrics.py -v` — report exact output
2. Run the evaluation runner on at least 3 test cases — report the actual metric values produced
3. Verify baseline.json exists and contains non-zero metric values
4. Verify EVALUATION.md documents actual (not invented) baseline numbers
5. Verify metric formulas match the definitions in `docs/evaluation/evaluation-framework.md`

---

## Human Approval Required

- Baseline quality thresholds (human decides what is "good enough" before release)
- Choice of faithfulness evaluation approach (RAGAS vs. custom LLM judge)
- Evaluation dataset content review (ensure no proprietary data)

---

## Definition of Done

- [ ] 20+ evaluation cases in versioned dataset
- [ ] All 5 metrics implemented as code and unit-tested
- [ ] Evaluation runner executes successfully (actual results reported)
- [ ] Baseline stored with real results
- [ ] Regression comparison script works
- [ ] EVALUATION.md updated with actual (not placeholder) results
- [ ] Human reviewer approved PR

---

## Output Report

Kiro must report:
- Files created
- Test results: `pytest tests/unit/test_metrics.py -v` → exact output
- Evaluation run output: actual metric values (e.g., Recall@5: 0.72, MRR: 0.68)
- Number of evaluation cases run
- Whether baseline was stored
- Known limitations (e.g., faithfulness metric requires OpenAI API key)
- **Jira status recommendation:** Ready for Code Review
