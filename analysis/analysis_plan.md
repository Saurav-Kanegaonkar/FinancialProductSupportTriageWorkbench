# Analysis Plan

## Objective

Rank financial product support issues by business urgency and release risk so a Product Analyst can prioritize resolution procedures, Service Center updates, test requests, vendor follow-up, and scheduled incremental improvements.

## Inputs

- Support issue queue
- Product requirements mapped from recurring issues
- Test requests by release
- User-group communication records
- Vendor dependencies

## Data Quality Checks

Before scoring, the workbench checks each source table for:

- row counts;
- column counts;
- primary-key duplicate counts;
- missing-cell counts.

The generated quality output is `analysis/outputs/data_quality_checks.csv` and the rendered evidence image is `docs/images/data-quality-checks.png`.

## EDA Questions

- What does the issue queue look like by severity and status?
- Which active issues are score outliers?
- Which application and user-group segments concentrate the highest average score?
- Which score drivers are most associated with issue priority?
- Which release groups combine pass-rate gap, open defects, and not-ready tests?

## Scoring Logic

The triage score uses illustrative review weights, not an automated production rule. It combines:

- severity weighting;
- SLA breach risk from issue age versus target resolution window;
- defect recurrence;
- affected user count;
- customer effort score;
- vendor blocker flag.

The score intentionally gives the largest fixed baseline to severity, caps SLA aging so stale lower-severity tickets do not overwhelm true P1 incidents, and then adds recurrence, affected-user, customer-effort, and vendor-blocker pressure to surface issues that need cross-team coordination.

## Model-Vs-Rule Benchmark

A black-box predictive model is not the best fit for this JD because the Product Analyst must defend prioritization logic to operations, vendors, and user groups. Instead, the workbench compares:

- `Severity + SLA baseline`: severity weighting plus SLA breach and vendor-blocker flags;
- `Multi-signal triage score`: severity, SLA pressure, recurrence, affected users, customer effort, and vendor blocker.

The benchmark uses a synthetic `review_required` proxy for same-week review need and reports precision, recall, vendor-blocked share, average effort, and SLA breach rate at top 100.

## Sensitivity Analysis

The workbench tests whether the top 25 active blocker queue changes under:

- current balanced review weights;
- SLA-heavy escalation;
- user-impact-heavy prioritization;
- vendor-escalation-heavy prioritization.

The output `analysis/outputs/sensitivity_scenarios.csv` shows overlap with the current top 25 and how each scenario changes vendor share, SLA breach rate, customer effort, and review-required share.

## Review Questions

- Which issues should be escalated before the next user group?
- Which releases have the weakest test readiness?
- Which vendors are slowing application support?
- Which requirements represent recurring issues rather than one-off tickets?
- Which score weights should be calibrated against historical outcomes before production use?
