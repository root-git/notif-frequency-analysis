with notif_summary as (
    select user_id, count(*) as total_notifications,
    countif(was_opened) as total_opens, countif(was_clicked) as total_clicks 
    from {{ref('int_notifications_with_events')}}
    group by user_id
), 
activity_summary as (
    select user_id, countif(activity_type ='app_open') as total_app_opens
    from {{ref('stg_user_activity')}}
    group by user_id
)

select
    coalesce(n.user_id, a.user_id) as user_id,
    coalesce(n.total_notifications, 0) as total_notifications,
    coalesce(n.total_opens, 0) as total_opens,
    coalesce(n.total_clicks, 0) as total_clicks,
    coalesce(a.total_app_opens, 0) as total_app_opens
from notif_summary n
full outer join activity_summary a on n.user_id = a.user_id