# Data Dictionary

## Source Tables

### `data/support_issues.csv`

One row per open or recently closed application issue.

- `issue_id`: Stable issue key.
- `application`: Supported financial application area.
- `opened_date`: Date issue entered the queue.
- `status`: Current state.
- `severity`: Business severity from P1 to P4.
- `channel`: Intake source, including Service Center.
- `user_group`: Primary affected user population.
- `sla_hours`: Target resolution hours.
- `hours_open`: Current or final age of the issue.
- `recurrence_count`: Prior related issues in the lookback window.
- `affected_users`: Estimated affected user count.
- `customer_effort_score`: Synthetic 1-7 effort score.
- `vendor_blocked`: Whether a vendor action is required.
- `release_id`: Related release or upgrade.

### `data/product_requirements.csv`

One row per requirement derived from grouped issues.

- `requirement_id`: Requirement key.
- `application`: Related supported application.
- `source_issue_count`: Number of issues mapped into the requirement.
- `priority`: Product priority tier.
- `business_owner`: Owning department.
- `acceptance_criteria_count`: Count of acceptance criteria.
- `planned_increment`: Incremental rollout milestone.

### `data/test_requests.csv`

One row per release test request.

- `test_request_id`: Test request key.
- `release_id`: Release being validated.
- `application`: Application under test.
- `test_type`: UAT, regression, vendor validation, or data validation.
- `pass_rate`: Synthetic pass rate.
- `open_defects`: Remaining defects.
- `ready_for_release`: Boolean readiness flag.

### `data/user_groups.csv`

One row per recurring user group.

- `user_group`: User population.
- `meeting_frequency`: Expected forum cadence.
- `active_members`: Group size.
- `top_pain_point`: Most common issue theme.
- `sharepoint_updates_last_30d`: Communication updates in the last 30 days.

### `data/vendor_dependencies.csv`

One row per vendor dependency.

- `vendor_id`: Vendor key.
- `application`: Related application.
- `dependency_type`: Data feed, API, defect fix, access, or release signoff.
- `avg_turnaround_hours`: Vendor turnaround time.
- `open_items`: Open dependency count.
- `risk_level`: Dependency risk label.

## Generated Outputs

### `analysis/outputs/ranked_issue_queue.csv`

One row per support issue, including closed items for scoring auditability.

- `triage_score`: Illustrative review score combining severity, SLA pressure, recurrence, affected users, customer effort, and vendor blocker.
- `sla_breached`: Boolean field showing whether `hours_open` exceeds the issue's `sla_hours` target.

### `analysis/outputs/top_25_upgrade_blockers.csv`

One row per active issue selected for blocker review.

- `sla_breach_flag`: Boolean field showing whether `hours_open` exceeds the issue's `sla_hours` target.

### `analysis/outputs/release_readiness_summary.csv`

One row per release.

- `avg_pass_rate`: Average test pass rate for the release.
- `pass_rate_gap`: `1 - avg_pass_rate`; used so release-readiness color means higher risk when the value is higher.
- `open_defects`: Total open defects across release test requests.
- `not_ready_tests`: Count of test requests not ready for release.

### `analysis/outputs/kpi_snapshot.csv`

One row per KPI for Product Analyst status updates.

- `issue_count`: Total issue records.
- `open_issue_count`: Active issue records excluding `Closed`.
- `sla_breach_rate`: Active issues beyond SLA target divided by active issues.
- `avg_hours_open`: Average age of active issues.
- `vendor_blocked_share`: Active issues requiring vendor action divided by active issues.
- `avg_customer_effort_score`: Average active issue effort score.

### `analysis/outputs/data_quality_checks.csv`

One row per source table.

- `row_count`: Source table row count.
- `column_count`: Source table column count.
- `primary_key`: Expected unique key column.
- `duplicate_key_count`: Count of duplicate primary-key values.
- `missing_cell_count`: Total missing cells across the table.

### `analysis/outputs/eda_segment_summary.csv`

One row per application and user-group segment among active issues.

- `active_issue_count`: Number of active issues in the segment.
- `avg_triage_score`: Average active issue score.
- `sla_breach_rate`: Segment share of active issues beyond SLA.
- `vendor_blocked_share`: Segment share requiring vendor action.
- `avg_customer_effort`: Average effort score.
- `review_required_rate`: Share of active issues meeting the benchmark review-required proxy.

### `analysis/outputs/driver_correlations.csv`

Correlation matrix for numeric score drivers, release risk fields, and `triage_score`.

### `analysis/outputs/triage_score_outliers.csv`

Top active score outliers above the IQR threshold, with driver columns retained for review.

### `analysis/outputs/model_vs_rule_benchmark.csv`

Benchmark comparing the multi-signal score with a simpler severity/SLA baseline at top 100.

- `precision_at_100`: Share of selected top-100 items that meet the synthetic review-required proxy.
- `recall_at_100`: Share of all review-required items captured in the selected top 100.
- `vendor_blocked_share_at_100`: Vendor-blocked share among selected items.
- `avg_customer_effort_at_100`: Average customer effort among selected items.
- `avg_sla_breach_rate_at_100`: SLA breach rate among selected items.

### `analysis/outputs/sensitivity_scenarios.csv`

Scenario-level comparison of current, SLA-heavy, user-impact-heavy, and vendor-escalation-heavy weights.

- `top_25_overlap_with_current`: Count of issue IDs overlapping with the current top 25.
- `avg_score`: Average scenario score for the selected top 25.
- `sla_breach_rate`: SLA breach rate among selected top 25.
- `vendor_blocked_share`: Vendor-blocked share among selected top 25.
- `avg_customer_effort`: Average customer effort among selected top 25.
- `review_required_share`: Share meeting the synthetic review-required proxy.
