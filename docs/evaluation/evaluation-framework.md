# AI Evaluation Framework

This document defines the evaluation methodology used across all 10 projects in the AI-10 Portfolio.

## Principles

1. **Baselines first, thresholds second.** Establish baseline results before setting pass/fail thresholds. An arbitrary score without a baseline is meaningless.
2. **Metric formulas are code.** Every metric is implemented in `evaluation/metrics/` — not just named in prose.
3. **Versioned datasets.** Evaluation datasets are version-controlled. Results are only comparable when the dataset is identical.
4. **Per-case inspection.** Aggregate scores alone are not sufficient. Per-case failures must be inspectable.
5. **Evaluation is a release gate.** Regressions against the established baseline block release.
6. **Human spot-checks.** Automated metrics are supplemented with human evaluation for quality-sensitive dimensions.
7. **Separate correctness from quality.** Software tests (unit/integration) verify correctness. AI evaluation measures quality.

## Evaluation Directory Structure

Every project with AI behavior has:
```
evaluation/
├── datasets/          — versioned input datasets (jsonl, csv)
├── cases/             — individual test cases with inputs and expected outputs
├── runners/           — scripts that execute evaluation runs
├── metrics/           — metric implementations (Python)
├── reports/           — output reports from each run (timestamped)
└── regression/        — baseline files for comparison
```

## Standard Evaluation Run

```bash
# Run evaluation against the current model/config
python evaluation/runners/run_eval.py \
  --dataset evaluation/datasets/v1.0/eval_set.jsonl \
  --config evaluation/runners/config.yaml \
  --output evaluation/reports/$(date +%Y%m%d_%H%M%S).json

# Compare against baseline
python evaluation/runners/compare_baseline.py \
  --baseline evaluation/regression/baseline.json \
  --current evaluation/reports/<latest>.json
```

## Metric Definitions by Project

### P01 — RAG Platform

| Metric | Formula | Threshold (TBD after baseline) |
|---|---|---|
| Recall@k | |{retrieved} ∩ {relevant}| / |{relevant}| | ≥ baseline |
| MRR | mean(1 / rank of first relevant result) | ≥ baseline |
| Faithfulness | % of answer claims supported by retrieved passages | ≥ baseline |
| Citation Precision | % of cited passages that are relevant | ≥ baseline |
| Answer Relevance | LLM-as-judge: is the answer relevant to the question? | ≥ baseline |
| Latency p95 | 95th percentile end-to-end query latency | ≤ baseline + 20% |

### P02 — Research Agent

| Metric | Formula |
|---|---|
| Source Coverage | % of known relevant sources found |
| Claim Accuracy | % of report claims verified against sources |
| Report Completeness | % of required report sections present and non-empty |
| Hallucination Rate | % of claims with no source support |

### P03 — Customer Support

| Metric | Formula |
|---|---|
| Resolution Rate | % of test cases resolved without escalation |
| Escalation Accuracy | % of escalation decisions that are correct |
| Response Relevance | LLM-as-judge: relevance score |

### P04 — Voice Agent

| Metric | Formula |
|---|---|
| Intent Accuracy | % of utterances with correct intent classification |
| Slot Fill Accuracy | % of required slots correctly extracted |
| Task Completion Rate | % of multi-turn conversations achieving the goal |

### P05 — AgentOps

| Metric | Formula |
|---|---|
| Metric Correctness | % of computed metrics matching ground truth |
| Alert Precision | % of alerts that are true positives |
| Ingestion Accuracy | % of events correctly parsed and stored |

### P06 — Data Extraction

| Metric | Formula |
|---|---|
| Field Extraction Accuracy | % of fields correctly extracted per document |
| Schema Compliance Rate | % of outputs that validate against target schema |
| Confidence Calibration | correlation between confidence score and actual accuracy |

### P07 — Multi-Agent Orchestrator

| Metric | Formula |
|---|---|
| Plan Validity | % of generated plans with no dependency cycles |
| Dependency Correctness | % of task dependencies correctly identified |
| Task Completion Rate | % of demo workflows completed end-to-end |

### P08 — Enterprise Search

| Metric | Formula |
|---|---|
| NDCG@k | Normalized Discounted Cumulative Gain at rank k |
| MRR | Mean Reciprocal Rank |
| Recall@k | % of relevant documents in top-k results |
| Query Rewrite Quality | % of rewritten queries improving retrieval vs. original |

### P09 — Code Review AI

| Metric | Formula |
|---|---|
| Finding Precision | % of reported findings that are real issues |
| Finding Recall | % of real issues that were reported |
| False Positive Rate | % of reported findings that are not real issues |

### P10 — Prompt Security

| Metric | Formula |
|---|---|
| Detection Rate | % of injection attempts correctly detected |
| False Positive Rate | % of benign inputs incorrectly flagged |
| PII Recall | % of PII instances correctly identified and redacted |

## Baseline Establishment Process

1. Implement the evaluation runner and metric code
2. Run evaluation against the initial dataset
3. Record results as the baseline: `evaluation/regression/baseline.json`
4. Set pass/fail thresholds at baseline - 10% (or agreed delta)
5. All future evaluation runs compare against this baseline
6. Update the baseline when a deliberate model or prompt change improves quality (require human approval to update baseline)

## Evaluation Report Format

```json
{
  "run_id": "eval_20261005_120000",
  "project": "P01",
  "dataset_version": "v1.0",
  "model": "gpt-4o-2024-08-06",
  "config_hash": "abc123",
  "timestamp": "2026-10-05T12:00:00Z",
  "duration_seconds": 342,
  "aggregate_metrics": {
    "recall_at_5": 0.82,
    "mrr": 0.74,
    "faithfulness": 0.91,
    "citation_precision": 0.88,
    "answer_relevance": 0.85
  },
  "per_case_results": [
    {
      "case_id": "case_001",
      "query": "What is the refund policy?",
      "recall_at_5": 1.0,
      "faithfulness": 0.95,
      "passed": true
    }
  ],
  "regression_comparison": {
    "baseline_run_id": "eval_20261001_090000",
    "regressions": [],
    "improvements": ["faithfulness: +0.03"]
  }
}
```
