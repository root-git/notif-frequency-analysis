from google.cloud import bigquery

client = bigquery.Client()
DATASET = "notif-frequency-analysis.notif_raw"

# Fix A: de-duplicate, keeping one row per notification_id
client.query(f"""
    create or replace table `{DATASET}.raw_notifications_sent` as
    select * except(rn) from (
        select *, row_number() over (partition by notification_id) as rn
        from `{DATASET}.raw_notifications_sent`
    )
    where rn=1
""").result()

# Fix B: quarantine orphaned rows instead of deleting them
client.query(f"""
    create or replace table `{DATASET}.raw_notifications_sent_orphaned` as
    select n.* from `{DATASET}.raw_notifications_sent` n
    left join `{DATASET}.raw_users` u on n.user_id=u.user_id
    where u.user_id is null
""").result()

client.query(f"""
    create or replace table `{DATASET}.raw_notifications_sent` as
    select n.* from `{DATASET}.raw_notifications_sent` n
    left join `{DATASET}.raw_users` u on n.user_id = u.user_id
    where u.user_id is not null
""").result()

print("Remediation complete.")