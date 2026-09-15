# notif_orchestration/notif_orchestration/checks.py
from dagster import asset_check, AssetCheckResult
from dagster_dbt import get_asset_key_for_model
from google.cloud import bigquery

from notif_orchestration.assets import notif_dbt_assets

client = bigquery.Client()

@asset_check(asset=get_asset_key_for_model([notif_dbt_assets], "stg_notifications_sent"))
def no_duplicate_notification_ids(context):
    query = """
        select count(*) as dup_count from (
            select notification_id
            from `notif-frequency-analysis.notif_analytics.stg_notifications_sent`
            group by 1 having count(*) > 1
        )
    """
    result = list(client.query(query).result())
    dup_count = result[0].dup_count
    return AssetCheckResult(passed=(dup_count == 0), metadata={"duplicate_count": dup_count})

@asset_check(asset=get_asset_key_for_model([notif_dbt_assets], "fct_notifications"))
def no_orphaned_user_ids(context):
    query = """
        select count(*) as orphan_count
        from `notif-frequency-analysis.notif_analytics.fct_notifications` f
        left join `notif-frequency-analysis.notif_analytics.dim_users` u on f.user_id = u.user_id
        where u.user_id is null
    """
    result = list(client.query(query).result())
    orphan_count = result[0].orphan_count
    return AssetCheckResult(passed=(orphan_count == 0), metadata={"orphaned_count": orphan_count})