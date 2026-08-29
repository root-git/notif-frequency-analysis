-- Purpose: this is the formal handoff point - the last check before dbt
-- takes over as the validation layer in Week 2. Confirm the laod didn't
-- silently drop or duplicate rows in transit to BigQuery

select count(*) from notif_raw.raw_users;
select min(sent_at), max(sent_at), count(*) from notif_raw.raw_notifications_sent;
select event_type, count(*) from notif_raw.raw_notification_events group by 1;
select count(*) from notif_raw.raw_unsubscribes;
select count(*) from notif_raw.raw_user_activity;

-- confirm the load didn't introduce duplicates that weren't in the source CSVs
select notification_id, count(*) from notif_raw.raw_notifications_sent
group by 1 having count(*) > 1;  -- expect 0 rows