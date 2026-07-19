from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "analysis" / "outputs"
IMAGES = ROOT / "docs" / "images"
RNG = random.Random(42)

APPLICATIONS = [
    "Advisor Portal",
    "Trade Support",
    "Public Finance CRM",
    "Client Reporting",
    "Compliance Workflow",
    "Data Entitlements",
]
USER_GROUPS = [
    "Operations",
    "Financial Advisors",
    "Public Finance",
    "Compliance",
    "Sales Support",
]
SEVERITY_WEIGHT = {"P1": 40, "P2": 28, "P3": 14, "P4": 6}
ACTIVE_STATUSES = {"Open", "In Progress", "Vendor Pending", "Testing"}
SEVERITY_ORDER = ["P1", "P2", "P3", "P4"]
STATUS_ORDER = ["Open", "In Progress", "Vendor Pending", "Testing", "Closed"]


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def generate_support_issues() -> list[dict]:
    rows = []
    today = date(2026, 7, 18)
    for i in range(1, 1101):
        severity = RNG.choices(["P1", "P2", "P3", "P4"], weights=[5, 20, 50, 25])[0]
        sla_hours = {"P1": 8, "P2": 24, "P3": 72, "P4": 168}[severity]
        hours_open = max(2, int(RNG.gammavariate(2.2, 28)))
        opened = today - timedelta(hours=hours_open)
        rows.append(
            {
                "issue_id": f"HTS-{i:04d}",
                "application": RNG.choice(APPLICATIONS),
                "opened_date": opened.isoformat(),
                "status": RNG.choices(["Open", "In Progress", "Vendor Pending", "Testing", "Closed"], weights=[25, 30, 12, 18, 15])[0],
                "severity": severity,
                "channel": RNG.choices(["Service Center", "User Group", "Email", "Vendor", "Release Testing"], weights=[55, 15, 10, 8, 12])[0],
                "user_group": RNG.choice(USER_GROUPS),
                "sla_hours": sla_hours,
                "hours_open": hours_open,
                "recurrence_count": RNG.choices([0, 1, 2, 3, 4, 5], weights=[42, 26, 15, 9, 5, 3])[0],
                "affected_users": RNG.randint(3, 180),
                "customer_effort_score": round(RNG.uniform(2.1, 6.8), 1),
                "vendor_blocked": RNG.choices([0, 1], weights=[78, 22])[0],
                "release_id": f"REL-{RNG.randint(1, 8):02d}",
            }
        )
    return rows


def generate_requirements(issues: list[dict]) -> list[dict]:
    rows = []
    for i in range(1, 121):
        source_count = RNG.randint(2, 18)
        rows.append(
            {
                "requirement_id": f"REQ-{i:03d}",
                "application": RNG.choice(APPLICATIONS),
                "source_issue_count": source_count,
                "priority": RNG.choices(["Critical", "High", "Medium", "Low"], weights=[10, 30, 45, 15])[0],
                "business_owner": RNG.choice(USER_GROUPS),
                "acceptance_criteria_count": RNG.randint(3, 9),
                "planned_increment": f"Increment {RNG.randint(1, 4)}",
            }
        )
    return rows


def generate_tests() -> list[dict]:
    rows = []
    for i in range(1, 181):
        pass_rate = round(RNG.uniform(0.72, 0.99), 3)
        open_defects = max(0, int((1 - pass_rate) * RNG.randint(8, 35)))
        rows.append(
            {
                "test_request_id": f"TEST-{i:03d}",
                "release_id": f"REL-{RNG.randint(1, 8):02d}",
                "application": RNG.choice(APPLICATIONS),
                "test_type": RNG.choice(["UAT", "Regression", "Vendor Validation", "Data Validation"]),
                "pass_rate": pass_rate,
                "open_defects": open_defects,
                "ready_for_release": 1 if pass_rate >= 0.9 and open_defects <= 2 else 0,
            }
        )
    return rows


def generate_user_groups() -> list[dict]:
    pain_points = ["SLA visibility", "Report accuracy", "Vendor turnaround", "Access defects", "Release communication"]
    return [
        {
            "user_group": group,
            "meeting_frequency": RNG.choice(["Weekly", "Biweekly", "Monthly"]),
            "active_members": RNG.randint(18, 95),
            "top_pain_point": RNG.choice(pain_points),
            "sharepoint_updates_last_30d": RNG.randint(3, 16),
        }
        for group in USER_GROUPS
    ]


def generate_vendors() -> list[dict]:
    rows = []
    dependency_types = ["Data Feed", "API", "Defect Fix", "Access", "Release Signoff"]
    for i in range(1, 13):
        app = APPLICATIONS[(i - 1) % len(APPLICATIONS)]
        rows.append(
            {
                "vendor_id": f"VEND-{i:02d}",
                "application": app,
                "dependency_type": dependency_types[(i - 1) % len(dependency_types)],
                "avg_turnaround_hours": RNG.randint(18, 160),
                "open_items": RNG.randint(1, 14),
                "risk_level": RNG.choices(["Low", "Medium", "High", "Critical"], weights=[20, 35, 32, 13])[0],
            }
        )
    return rows


def score_issue(row: dict) -> float:
    """Illustrative review score for prioritizing analyst attention."""
    sla_ratio = float(row["hours_open"]) / float(row["sla_hours"])
    score = SEVERITY_WEIGHT[row["severity"]]
    score += min(35, sla_ratio * 12)
    score += int(row["recurrence_count"]) * 4
    score += min(18, int(row["affected_users"]) / 10)
    score += float(row["customer_effort_score"]) * 3
    score += 10 if int(row["vendor_blocked"]) else 0
    return round(score, 2)


def scenario_score(row: pd.Series, scenario: dict) -> float:
    sla_ratio = float(row["hours_open"]) / float(row["sla_hours"])
    score = SEVERITY_WEIGHT[row["severity"]] * scenario["severity_multiplier"]
    score += min(scenario["sla_cap"], sla_ratio * scenario["sla_scale"])
    score += int(row["recurrence_count"]) * scenario["recurrence_weight"]
    score += min(scenario["affected_cap"], int(row["affected_users"]) / scenario["affected_divisor"])
    score += float(row["customer_effort_score"]) * scenario["effort_weight"]
    score += scenario["vendor_weight"] if int(row["vendor_blocked"]) else 0
    return round(score, 2)


def top_n_metrics(df: pd.DataFrame, score_col: str, n: int = 100) -> dict:
    selected = df[df["active_flag"]].sort_values(score_col, ascending=False).head(n)
    total_required = max(1, int(df["review_required"].sum()))
    captured = int(selected["review_required"].sum())
    return {
        "method": score_col,
        "selected_items": len(selected),
        "review_required_captured": captured,
        "precision_at_100": round(captured / max(1, len(selected)), 3),
        "recall_at_100": round(captured / total_required, 3),
        "vendor_blocked_share_at_100": round(selected["vendor_blocked"].mean(), 3),
        "avg_customer_effort_at_100": round(selected["customer_effort_score"].mean(), 2),
        "avg_sla_breach_rate_at_100": round(selected["sla_breached"].mean(), 3),
    }


def write_analysis_depth_outputs(ranked: list[dict], release_rows: list[dict]) -> None:
    issues = pd.DataFrame(ranked)
    releases = pd.DataFrame(release_rows)
    issues["active_flag"] = issues["status"].isin(ACTIVE_STATUSES)
    issues = issues.merge(
        releases[["release_id", "pass_rate_gap", "not_ready_tests", "open_defects"]],
        on="release_id",
        how="left",
    )
    high_release_risk = issues["not_ready_tests"] >= issues["not_ready_tests"].quantile(0.75)
    issues["review_required"] = (
        issues["active_flag"]
        & (
            ((issues["sla_breached"] == 1) & (issues["recurrence_count"] >= 2))
            | (issues["severity"].isin(["P1", "P2"]) & (issues["vendor_blocked"] == 1))
            | ((issues["customer_effort_score"] >= 6.0) & (issues["affected_users"] >= 100))
            | (high_release_risk & issues["severity"].isin(["P1", "P2"]))
        )
    ).astype(int)
    issues["severity_sla_rule_score"] = issues["severity"].map(SEVERITY_WEIGHT) + issues["sla_breached"] * 30 + issues["vendor_blocked"] * 8

    segment_summary = (
        issues[issues["active_flag"]]
        .groupby(["application", "user_group"])
        .agg(
            active_issue_count=("issue_id", "count"),
            avg_triage_score=("triage_score", "mean"),
            sla_breach_rate=("sla_breached", "mean"),
            vendor_blocked_share=("vendor_blocked", "mean"),
            avg_customer_effort=("customer_effort_score", "mean"),
            review_required_rate=("review_required", "mean"),
        )
        .reset_index()
        .round(3)
        .sort_values(["avg_triage_score", "active_issue_count"], ascending=[False, False])
    )
    segment_summary.to_csv(OUT / "eda_segment_summary.csv", index=False, lineterminator="\n")

    data_quality_rows = []
    source_tables = {
        "support_issues": DATA / "support_issues.csv",
        "product_requirements": DATA / "product_requirements.csv",
        "test_requests": DATA / "test_requests.csv",
        "user_groups": DATA / "user_groups.csv",
        "vendor_dependencies": DATA / "vendor_dependencies.csv",
    }
    key_columns = {
        "support_issues": "issue_id",
        "product_requirements": "requirement_id",
        "test_requests": "test_request_id",
        "user_groups": "user_group",
        "vendor_dependencies": "vendor_id",
    }
    for table_name, path in source_tables.items():
        table = pd.read_csv(path)
        key = key_columns[table_name]
        data_quality_rows.append(
            {
                "table_name": table_name,
                "row_count": len(table),
                "column_count": len(table.columns),
                "primary_key": key,
                "duplicate_key_count": int(table[key].duplicated().sum()),
                "missing_cell_count": int(table.isna().sum().sum()),
            }
        )
    pd.DataFrame(data_quality_rows).to_csv(OUT / "data_quality_checks.csv", index=False, lineterminator="\n")

    driver_cols = [
        "triage_score",
        "hours_open",
        "sla_breached",
        "recurrence_count",
        "affected_users",
        "customer_effort_score",
        "vendor_blocked",
        "pass_rate_gap",
        "not_ready_tests",
    ]
    issues[driver_cols].corr(numeric_only=True).round(3).to_csv(OUT / "driver_correlations.csv", lineterminator="\n")

    q1 = issues["triage_score"].quantile(0.25)
    q3 = issues["triage_score"].quantile(0.75)
    iqr_threshold = q3 + 1.5 * (q3 - q1)
    outliers = (
        issues[(issues["active_flag"]) & (issues["triage_score"] >= iqr_threshold)]
        .sort_values("triage_score", ascending=False)
        .head(25)
    )
    outliers[
        [
            "issue_id",
            "application",
            "user_group",
            "status",
            "severity",
            "triage_score",
            "hours_open",
            "sla_breached",
            "recurrence_count",
            "affected_users",
            "customer_effort_score",
            "vendor_blocked",
            "release_id",
            "not_ready_tests",
        ]
    ].to_csv(OUT / "triage_score_outliers.csv", index=False, lineterminator="\n")

    benchmark = pd.DataFrame(
        [
            top_n_metrics(issues, "severity_sla_rule_score"),
            top_n_metrics(issues, "triage_score"),
        ]
    )
    benchmark["method"] = benchmark["method"].map(
        {
            "severity_sla_rule_score": "Severity + SLA baseline",
            "triage_score": "Multi-signal triage score",
        }
    )
    benchmark.to_csv(OUT / "model_vs_rule_benchmark.csv", index=False, lineterminator="\n")

    scenarios = {
        "Current review weights": {
            "severity_multiplier": 1.0,
            "sla_scale": 12,
            "sla_cap": 35,
            "recurrence_weight": 4,
            "affected_divisor": 10,
            "affected_cap": 18,
            "effort_weight": 3,
            "vendor_weight": 10,
        },
        "SLA-heavy escalation": {
            "severity_multiplier": 1.0,
            "sla_scale": 18,
            "sla_cap": 45,
            "recurrence_weight": 3,
            "affected_divisor": 12,
            "affected_cap": 15,
            "effort_weight": 2.5,
            "vendor_weight": 8,
        },
        "User-impact heavy": {
            "severity_multiplier": 1.0,
            "sla_scale": 10,
            "sla_cap": 30,
            "recurrence_weight": 3,
            "affected_divisor": 6,
            "affected_cap": 25,
            "effort_weight": 4,
            "vendor_weight": 8,
        },
        "Vendor-escalation heavy": {
            "severity_multiplier": 0.95,
            "sla_scale": 11,
            "sla_cap": 32,
            "recurrence_weight": 4,
            "affected_divisor": 12,
            "affected_cap": 15,
            "effort_weight": 2.5,
            "vendor_weight": 20,
        },
    }
    active = issues[issues["active_flag"]].copy()
    current_top = set(active.sort_values("triage_score", ascending=False).head(25)["issue_id"])
    scenario_rows = []
    for scenario_name, scenario in scenarios.items():
        score_col = f"scenario_score_{len(scenario_rows)}"
        active[score_col] = active.apply(lambda row: scenario_score(row, scenario), axis=1)
        selected = active.sort_values(score_col, ascending=False).head(25)
        scenario_rows.append(
            {
                "scenario": scenario_name,
                "top_25_overlap_with_current": len(current_top & set(selected["issue_id"])),
                "avg_score": round(selected[score_col].mean(), 2),
                "sla_breach_rate": round(selected["sla_breached"].mean(), 3),
                "vendor_blocked_share": round(selected["vendor_blocked"].mean(), 3),
                "avg_customer_effort": round(selected["customer_effort_score"].mean(), 2),
                "review_required_share": round(selected["review_required"].mean(), 3),
            }
        )
    pd.DataFrame(scenario_rows).to_csv(OUT / "sensitivity_scenarios.csv", index=False, lineterminator="\n")


def write_outputs(issues: list[dict], tests: list[dict]) -> None:
    ranked = []
    for issue in issues:
        scored = dict(issue)
        scored["triage_score"] = score_issue(issue)
        scored["sla_breached"] = 1 if int(issue["hours_open"]) > int(issue["sla_hours"]) else 0
        ranked.append(scored)
    ranked.sort(key=lambda row: row["triage_score"], reverse=True)
    write_csv(OUT / "ranked_issue_queue.csv", ranked)

    active_blockers = []
    for row in ranked:
        if row["status"] not in ACTIVE_STATUSES:
            continue
        blocker = dict(row)
        blocker["sla_breach_flag"] = blocker.pop("sla_breached")
        active_blockers.append(blocker)
    write_csv(OUT / "top_25_upgrade_blockers.csv", active_blockers[:25])

    by_release: dict[str, list[dict]] = {}
    for test in tests:
        by_release.setdefault(test["release_id"], []).append(test)
    release_rows = []
    for release_id, release_tests in sorted(by_release.items()):
        release_rows.append(
            {
                "release_id": release_id,
                "test_requests": len(release_tests),
                "avg_pass_rate": round(sum(float(t["pass_rate"]) for t in release_tests) / len(release_tests), 3),
                "pass_rate_gap": round(1 - (sum(float(t["pass_rate"]) for t in release_tests) / len(release_tests)), 3),
                "open_defects": sum(int(t["open_defects"]) for t in release_tests),
                "not_ready_tests": sum(1 for t in release_tests if int(t["ready_for_release"]) == 0),
            }
        )
    write_csv(OUT / "release_readiness_summary.csv", release_rows)

    open_issues = [row for row in issues if row["status"] != "Closed"]
    kpis = [
        {"metric": "issue_count", "value": len(issues)},
        {"metric": "open_issue_count", "value": len(open_issues)},
        {"metric": "sla_breach_rate", "value": round(sum(1 for row in open_issues if int(row["hours_open"]) > int(row["sla_hours"])) / len(open_issues), 3)},
        {"metric": "avg_hours_open", "value": round(sum(int(row["hours_open"]) for row in open_issues) / len(open_issues), 1)},
        {"metric": "vendor_blocked_share", "value": round(sum(int(row["vendor_blocked"]) for row in open_issues) / len(open_issues), 3)},
        {"metric": "avg_customer_effort_score", "value": round(sum(float(row["customer_effort_score"]) for row in open_issues) / len(open_issues), 2)},
    ]
    write_csv(OUT / "kpi_snapshot.csv", kpis)
    write_analysis_depth_outputs(ranked, release_rows)


def write_evidence_images() -> None:
    IMAGES.mkdir(parents=True, exist_ok=True)
    issues = pd.read_csv(OUT / "ranked_issue_queue.csv")
    releases = pd.read_csv(OUT / "release_readiness_summary.csv")
    top_blockers = pd.read_csv(OUT / "top_25_upgrade_blockers.csv")
    segment_summary = pd.read_csv(OUT / "eda_segment_summary.csv")
    data_quality = pd.read_csv(OUT / "data_quality_checks.csv")
    benchmark = pd.read_csv(OUT / "model_vs_rule_benchmark.csv")
    correlations = pd.read_csv(OUT / "driver_correlations.csv", index_col=0)

    app_summary = (
        issues.groupby("application")
        .agg(
            avg_triage_score=("triage_score", "mean"),
            sla_breach_rate=("sla_breached", "mean"),
            issue_count=("issue_id", "count"),
        )
        .sort_values("avg_triage_score", ascending=True)
    )

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ["#315c74" if value < app_summary["avg_triage_score"].max() else "#b04a35" for value in app_summary["avg_triage_score"]]
    app_summary["avg_triage_score"].plot(kind="barh", ax=ax, color=colors)
    ax.set_title("Average Triage Score by Supported Application", fontsize=15, weight="bold")
    ax.set_xlabel("Average triage score")
    ax.set_ylabel("")
    for index, value in enumerate(app_summary["avg_triage_score"]):
        ax.text(value + 0.6, index, f"{value:.1f}", va="center", fontsize=9)
    fig.tight_layout()
    fig.savefig(IMAGES / "triage-score-by-application.png", dpi=180)
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    severity_counts = issues["severity"].value_counts().reindex(SEVERITY_ORDER)
    status_counts = issues["status"].value_counts().reindex(STATUS_ORDER)
    severity_counts.plot(kind="bar", ax=axes[0], color="#315c74")
    axes[0].set_title("Issue Volume by Severity", fontsize=13, weight="bold")
    axes[0].set_xlabel("")
    axes[0].set_ylabel("Issues")
    status_counts.plot(kind="bar", ax=axes[1], color="#7a5c2e")
    axes[1].set_title("Issue Volume by Status", fontsize=13, weight="bold")
    axes[1].set_xlabel("")
    axes[1].set_ylabel("Issues")
    for ax in axes:
        ax.tick_params(axis="x", rotation=25)
    fig.suptitle("EDA: Support Queue Distribution", fontsize=15, weight="bold")
    fig.tight_layout()
    fig.savefig(IMAGES / "eda-support-queue-distribution.png", dpi=180)
    plt.close(fig)

    active_issues = issues[issues["status"].isin(ACTIVE_STATUSES)]
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.hist(active_issues["triage_score"], bins=24, color="#315c74", edgecolor="white")
    q90 = active_issues["triage_score"].quantile(0.9)
    q95 = active_issues["triage_score"].quantile(0.95)
    ax.axvline(q90, color="#b04a35", linestyle="--", linewidth=2, label=f"90th percentile: {q90:.1f}")
    ax.axvline(q95, color="#6b2e6f", linestyle="--", linewidth=2, label=f"95th percentile: {q95:.1f}")
    ax.set_title("EDA: Active Issue Triage Score Distribution", fontsize=15, weight="bold")
    ax.set_xlabel("Triage score")
    ax.set_ylabel("Active issues")
    ax.legend()
    fig.tight_layout()
    fig.savefig(IMAGES / "eda-triage-score-distribution.png", dpi=180)
    plt.close(fig)

    pivot = segment_summary.pivot(index="application", columns="user_group", values="avg_triage_score").reindex(APPLICATIONS)
    fig, ax = plt.subplots(figsize=(11, 6))
    image = ax.imshow(pivot, cmap="PuBuGn", aspect="auto")
    ax.set_title("Segment Cut: Average Triage Score by Application and User Group", fontsize=15, weight="bold")
    ax.set_xticks(range(len(pivot.columns)), pivot.columns, rotation=25, ha="right")
    ax.set_yticks(range(len(pivot.index)), pivot.index)
    for row in range(len(pivot.index)):
        for col in range(len(pivot.columns)):
            value = pivot.iloc[row, col]
            ax.text(col, row, f"{value:.1f}", ha="center", va="center", fontsize=8)
    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    fig.savefig(IMAGES / "segment-risk-heatmap.png", dpi=180)
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    active_issues.plot.scatter(
        x="hours_open",
        y="triage_score",
        c="customer_effort_score",
        cmap="viridis",
        alpha=0.65,
        ax=axes[0],
        colorbar=True,
    )
    axes[0].set_title("Metric Relationship: Age, Effort, and Score", fontsize=12, weight="bold")
    axes[0].set_xlabel("Hours open")
    axes[0].set_ylabel("Triage score")
    selected_corr = correlations.loc[
        ["hours_open", "recurrence_count", "affected_users", "customer_effort_score", "vendor_blocked", "pass_rate_gap"],
        "triage_score",
    ].sort_values()
    selected_corr.plot(kind="barh", ax=axes[1], color="#315c74")
    axes[1].set_title("Correlation with Triage Score", fontsize=12, weight="bold")
    axes[1].set_xlabel("Correlation")
    fig.suptitle("EDA: Score Drivers and Metric Relationships", fontsize=15, weight="bold")
    fig.tight_layout()
    fig.savefig(IMAGES / "eda-score-driver-relationships.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9.5, 4.8))
    ax.axis("off")
    quality_table = data_quality[["table_name", "row_count", "duplicate_key_count", "missing_cell_count"]].copy()
    table = ax.table(
        cellText=quality_table.values,
        colLabels=["Table", "Rows", "Duplicate Keys", "Missing Cells"],
        loc="center",
        cellLoc="left",
        colLoc="left",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.45)
    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_text_props(weight="bold", color="white")
            cell.set_facecolor("#315c74")
        elif row % 2 == 0:
            cell.set_facecolor("#f2f5f7")
    ax.set_title("Data Quality Checks Before Triage Scoring", fontsize=15, weight="bold", pad=16)
    fig.tight_layout()
    fig.savefig(IMAGES / "data-quality-checks.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5))
    x = range(len(benchmark))
    width = 0.22
    ax.bar([value - width for value in x], benchmark["precision_at_100"], width=width, label="Precision@100", color="#315c74")
    ax.bar(x, benchmark["recall_at_100"], width=width, label="Recall@100", color="#b04a35")
    ax.bar([value + width for value in x], benchmark["vendor_blocked_share_at_100"], width=width, label="Vendor share@100", color="#7a5c2e")
    ax.set_title("Benchmark: Multi-Signal Score vs Severity + SLA Rule", fontsize=15, weight="bold")
    ax.set_xticks(list(x), benchmark["method"], rotation=10, ha="right")
    ax.set_ylim(0, 1)
    ax.set_ylabel("Share")
    ax.legend()
    fig.tight_layout()
    fig.savefig(IMAGES / "model-vs-rule-benchmark.png", dpi=180)
    plt.close(fig)

    heatmap_data = releases.set_index("release_id")[["pass_rate_gap", "open_defects", "not_ready_tests"]]
    normalized = heatmap_data.copy()
    normalized["pass_rate_gap"] = normalized["pass_rate_gap"] / max(0.001, normalized["pass_rate_gap"].max())
    normalized["open_defects"] = normalized["open_defects"] / max(1, normalized["open_defects"].max())
    normalized["not_ready_tests"] = normalized["not_ready_tests"] / max(1, normalized["not_ready_tests"].max())

    fig, ax = plt.subplots(figsize=(9, 5))
    image = ax.imshow(normalized, cmap="YlOrRd", aspect="auto")
    ax.set_title("Release Readiness Risk Matrix", fontsize=15, weight="bold")
    ax.set_xticks(range(len(normalized.columns)), ["Pass-rate gap", "Open defects", "Tests not ready"])
    ax.set_yticks(range(len(normalized.index)), normalized.index)
    for row in range(len(heatmap_data.index)):
        for col, column in enumerate(heatmap_data.columns):
            value = heatmap_data.iloc[row, col]
            label = f"{value:.1%}" if column == "pass_rate_gap" else str(int(value))
            ax.text(col, row, label, ha="center", va="center", color="#222", fontsize=9)
    ax.text(
        0.5,
        -0.16,
        "Darker color means higher release-readiness risk: larger pass-rate gap, more open defects, or more not-ready tests.",
        transform=ax.transAxes,
        ha="center",
        fontsize=8,
        color="#444",
    )
    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    fig.savefig(IMAGES / "release-readiness-risk-matrix.png", dpi=180)
    plt.close(fig)

    table_cols = ["issue_id", "application", "severity", "status", "triage_score", "sla_breach_flag"]
    table_data = top_blockers[table_cols].head(10).copy()
    table_data["sla_breach_flag"] = table_data["sla_breach_flag"].map({1: "Yes", 0: "No"})
    fig, ax = plt.subplots(figsize=(12, 4.8))
    ax.axis("off")
    table = ax.table(
        cellText=table_data.values,
        colLabels=["Issue", "Application", "Severity", "Status", "Score", "SLA Breached"],
        loc="center",
        cellLoc="left",
        colLoc="left",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.45)
    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_text_props(weight="bold", color="white")
            cell.set_facecolor("#315c74")
        elif row % 2 == 0:
            cell.set_facecolor("#f2f5f7")
    ax.set_title("Top Upgrade Blockers for Release Review", fontsize=15, weight="bold", pad=16)
    fig.tight_layout()
    fig.savefig(IMAGES / "top-upgrade-blockers.png", dpi=180)
    plt.close(fig)


def main() -> None:
    issues = generate_support_issues()
    requirements = generate_requirements(issues)
    tests = generate_tests()
    user_groups = generate_user_groups()
    vendors = generate_vendors()

    write_csv(DATA / "support_issues.csv", issues)
    write_csv(DATA / "product_requirements.csv", requirements)
    write_csv(DATA / "test_requests.csv", tests)
    write_csv(DATA / "user_groups.csv", user_groups)
    write_csv(DATA / "vendor_dependencies.csv", vendors)
    write_outputs(issues, tests)
    write_evidence_images()


if __name__ == "__main__":
    main()
