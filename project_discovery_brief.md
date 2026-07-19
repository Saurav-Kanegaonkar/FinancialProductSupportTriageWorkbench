# Project Understanding Gate: Project Discovery Brief

## Actual Role Pain Point

Hilltop Securities' Product Analyst role is about keeping supported financial applications usable while requests arrive from Service Center tickets, user groups, vendors, test cycles, and business stakeholders. The pain point is prioritization under ambiguity: the analyst must research day-to-day issues, maintain status, communicate with users, support upgrades, define requirements, and decide which open items require escalation before release signoff.

## Stakeholder Workflow

The modeled workflow starts when support issues enter the Service Center queue. A Product Analyst reviews severity, SLA age, affected users, customer effort, recurrence, vendor dependency, user-group impact, and release-test context. The analyst then prepares an active blocker queue, updates status in the Service Center, coordinates vendor follow-up, discusses patterns in user groups, and converts repeat issues into requirements with acceptance criteria.

## Decision This Project Supports

The project supports a weekly or release-readiness decision: which active issues should be escalated, which should be discussed with user groups, which vendor dependencies need follow-up, and which recurring patterns should become scheduled incremental product improvements.

## Data-Generating Process

The project uses deterministic synthetic data because real financial application support queues and broker-dealer operational records are not public. The generator creates 1,100 support issues, 120 product requirements, 180 release test requests, 5 user groups, and 12 vendor dependencies. Distributions are intentionally operational: severity is skewed toward P3/P4, status includes open/in-progress/vendor/testing/closed, SLA targets vary by severity, and release tests include pass rates, open defects, and readiness flags.

## Key Metrics And Assumptions

- `triage_score`: illustrative review score based on severity, SLA aging, recurrence, affected users, customer effort, and vendor-blocked status.
- `sla_breach_rate`: share of active items beyond target resolution hours.
- `review_required`: synthetic same-week review label used only for benchmarking the score against a simpler severity/SLA baseline.
- `pass_rate_gap`: `1 - avg_pass_rate`, used so release-readiness color semantics align with risk.
- `vendor_blocked_share`: share of queue items requiring external vendor action.
- `review_required_capture`: count of benchmark-positive items captured in the top 100 ranked issues.

The main assumption is that historical support data would be available to calibrate the illustrative weights. The current weights are transparent placeholders for interview discussion, not a production decisioning model.

## Why A Non-Web Analysis Workbench Is Stronger Than A Dashboard

For this JD, the strongest signal is not visual dashboard fluency alone. The role asks for researching and resolving application issues, prioritizing resolution procedures, updating Service Center status, supporting tests, defining requirements, and communicating tradeoffs. A non-web workbench makes the logic inspectable: the interviewer can open the data, scoring code, EDA outputs, benchmark, sensitivity scenarios, and recommendations to see how the analyst thinks.

A dashboard would look polished, but it could hide the harder question: why should one issue move before another? This repo keeps the evidence close to the decision logic and produces rendered artifacts for quick review without making UI the center of gravity.

## Alternatives Considered And Rejected

- `shadcn/ui dashboard`: rejected because the role pain point is transparent prioritization and issue research, not building a production cockpit.
- `Power BI mock dashboard`: rejected because screenshots alone would be less inspectable than reproducible source data, scripts, and generated outputs.
- `black-box ML classifier`: rejected because same-week escalation should be explainable to operations, users, and vendors. The workbench uses a transparent score and a score-vs-rule benchmark instead.
- `written PRD only`: rejected because the JD asks for SQL, Power BI-style analysis, data-driven support, testing, and issue resolution, so a data-backed artifact is more credible.

## Known Weaknesses And Assumptions

- The data is synthetic, not Hilltop Securities operational data.
- The review-required benchmark label is a proxy for evaluation, not an observed production outcome.
- The workbench does not integrate directly with Salesforce Service Cloud, Power BI, Excel, PowerPoint, SharePoint, or Teams.
- Release readiness is represented through generated test-request data rather than actual UAT or vendor evidence.
- FINRA-related sensitivity is represented only through financial product support workflow context, not regulated customer records.
