# Skill: AI Evaluation

This skill covers building and running AI evaluation systems for all 10 projects.

## Topics
- Evaluation dataset creation and versioning
- Metric design: precision, recall, F1, NDCG, MRR, faithfulness, relevance
- Metric implementation in code (never just as prose)
- RAGAS for RAG evaluation
- LLM-as-judge patterns for subjective quality
- Human spot-check integration
- Baseline establishment before threshold-setting
- Regression detection and comparison
- Per-case failure inspection
- Evaluation runners and report generation
- Evaluation directory structure: datasets/, cases/, runners/, metrics/, reports/, regression/
- Evaluation as a CI gate
- Cost and latency tracking per evaluation run

## Project-specific metrics
- P01: Recall@k, MRR, faithfulness, citation precision, answer relevance
- P02: Source coverage, claim accuracy, report completeness, hallucination rate
- P03: Resolution rate, escalation accuracy, response relevance
- P04: Intent accuracy, slot fill accuracy, task completion rate
- P05: Metric correctness, alert precision, ingestion accuracy
- P06: Field extraction accuracy, schema compliance, confidence calibration
- P07: Plan validity, dependency correctness, task completion rate
- P08: NDCG, MRR, recall, query rewrite quality
- P09: Finding precision/recall, false positive rate
- P10: Detection rate, false positive rate, PII recall

## Reference
See `.kiro/steering/testing.md` section 8 (AI Evaluation Tests).
