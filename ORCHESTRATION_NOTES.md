# Orchestration Notes

## Why Dagster for this project
Dagster's asset-based model maps directly onto a dbt project — `dagster-dbt`
turns dbt models into Dagster assets automatically from the manifest, and
data quality checks become first-class `@asset_check`s attached to
specific assets rather than a separate test suite bolted on afterward.
That fits this project's DQ-first theme better than a generic
DAG-of-tasks tool would have in the same one-week budget.

## What actually got built
- dbt models loaded as Dagster software-defined assets via `@dbt_assets`
- Two asset checks (`no_duplicate_notification_ids`, `no_orphaned_user_ids`)
  reusing the exact diagnosis logic from the Week 5 fault-injection incident
- A schedule and a run-failure sensor, defined but not left running
  continuously (see below)
- A capstone demo: re-ran the Week 5 fault injection, watched
  `notif_dbt_assets` fail and both dependent checks correctly refuse to
  execute, then ran the Week 5 remediation script and re-materialized to
  confirm a clean, all-green run

## Honest scope
This is one week of hands-on exposure — enough to explain the concepts
(asset graph, scheduling, failure sensors, asset checks) and walk through
a working demo, not production Dagster experience. Built and orchestrated
with Dagster specifically; the underlying concepts (dependency graphs,
scheduling, failure handling, checks as pipeline citizens) transfer to
Airflow, which is more commonly named in DE job postings, but this
project doesn't demonstrate Airflow experience.

## The schedule and sensor are defined, not demonstrated live
`daily_schedule` and `on_pipeline_failure` are both wired into
`definitions.py` and visible in the Dagster UI, but neither was left
running. A schedule only fires while the Dagster daemon is alive
(started together with `dagster dev`), and a personal laptop isn't a
persistent host — leaving a schedule "on" wouldn't demonstrate anything
real without the process running 24/7. In a production deployment, the
daemon runs as its own long-lived service (e.g. in Kubernetes), separate
from any one developer's machine.