# Executive Findings

The generated support queue creates 1,100 synthetic application issues across six financial product surfaces, with 939 active items after excluding recently closed records from the operating blocker queue. The highest-scoring issues concentrate where SLA breach risk, recurrence, vendor blockers, customer effort, affected users, and release readiness overlap.

## Key Readouts

- `analysis/outputs/data_quality_checks.csv` shows zero duplicate primary keys and zero missing cells across all five source tables.
- `analysis/outputs/eda_segment_summary.csv` identifies Public Finance CRM as the highest average active-score application at 60.6.
- `analysis/outputs/triage_score_outliers.csv` isolates high-score active outliers above the IQR-based threshold.
- `analysis/outputs/ranked_issue_queue.csv` preserves the full scored queue for auditability.
- `analysis/outputs/top_25_upgrade_blockers.csv` filters to active statuses before identifying the top 25 upgrade blockers for Product Analyst review.
- `analysis/outputs/release_readiness_summary.csv` flags releases with larger pass-rate gaps and remaining open defects.
- `analysis/outputs/model_vs_rule_benchmark.csv` shows the multi-signal triage score captures 83 review-required top-100 items versus 72 for a severity/SLA baseline.
- `analysis/outputs/sensitivity_scenarios.csv` shows top-25 overlap ranges from 16 to 22 issues when stakeholder priorities shift toward SLA, user impact, or vendor escalation.
- `docs/images/` contains rendered evidence images for EDA, data quality, segment cuts, release readiness risk, score benchmarking, and the top upgrade blocker queue.

## Recommended Operating Motion

1. Review the active top 25 issues before user-group meetings and release readiness signoff.
2. Treat Public Finance CRM and Client Reporting as the first application segments for analyst follow-up.
3. Convert recurring high-score issue clusters into requirements with acceptance criteria.
4. Escalate high-risk vendor dependencies before release signoff, especially when issues also breach SLA.
5. Calibrate the illustrative score against real historical support outcomes before using it as a production prioritization standard.
