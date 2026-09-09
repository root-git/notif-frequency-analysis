# Incident Scenario (Planned - Gameday Style)

## Fault A: Duplicate ingestion
Simulats a retried/re-run load job appending an already-loaded batch of
notification rows a second time. Expected to break: notification_id
uniqueness test in stg_notifications_sent and fct_notifications.

## Fault B: Orphaned foreign key
Simulates a partial reload - new notifications reference user_ids that 
were never synced into raw_users. Expected to break: the relationships
test on fct_notifications.user_id.

## Why these two
Both are common, boring, real incidents (not exotic edge cases) - the
kind of thing a retru-without-idempotency-key or an out -of-order backfill
actually causes in production.