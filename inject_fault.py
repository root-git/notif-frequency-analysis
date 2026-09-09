
# Purpose: intentionally corrupt the BigQuery raw layer to trigger the
# faults listed in INCIDENT_SCENARIO.md. Run once; do not re-run without first re-loading clean
# data, or the row counts below will drift.
from google.cloud import bigquery

client = bigquery.Client()
DATASET = "notif-frequency-analysis.notif_raw"

# Fault A: duplicate 20 existing notification rows
client.query(f"""
    insert into `{DATASET}.raw_notifications_sent`
    select * from `{DATASET}.raw_notifications_sent`
    order by notification_id limit 20
""").result()

# Fault B: insert 15 rows referencing user_ids that don't exist in raw_users
client.query(f"""
    insert into `{DATASET}.raw_notifications_sent`
    (notification_id, user_id, sent_at, channel, notification_type, campaign_id)
    select
        concat('n_fault_', cast(row_number() over() as string)),
        concat('u_ghost_', cast(row_number() over() as string)),
        current_timestamp(),
        'push', 'marketing', 'c_01'
    from unnest(generate_array(1, 15))
""").result()

print("Faults injected. Raw layer is now intentionally broken.")