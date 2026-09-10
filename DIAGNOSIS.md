<!-- DIAGNOSIS.md -->
# Diagnosis

## What failed
- `unique_stg_notifications_sent_notification_id` — FAIL
- `relationships_fct_notifications_user_id__user_id__ref_dim_users_` — FAIL

## Root cause
Fault A: [N] notification_ids appear more than once in raw_notifications_sent
— consistent with a retried load job re-appending an already-ingested batch
without an idempotency check.

Fault B: [N] notifications reference user_ids with no matching row in
raw_users — consistent with a partial/out-of-order reload where the users
table sync hadn't completed before the notifications sync ran.

## How I'd confirm this in a real system
Check the load job's run history/logs for a retry around the affected
timestamp range, and check whether the users-table sync and
notifications-table sync are two independently-scheduled jobs with no
ordering guarantee between them.