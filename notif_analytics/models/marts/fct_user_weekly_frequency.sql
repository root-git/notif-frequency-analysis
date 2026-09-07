-- Purpose: the central fact table - one row per user per week, with 
-- notifications sent, opens, clicks, and whether they unsubscribed that
-- week. Everything downstream is built on top of this.

with weekly_counts as (
    select * from {{ref('int_user_weekly_notification_counts')}}
),
weekly_opens as (
    select user_id, date_trunc(date(sent_at), week) as week_start,
      countif(was_opened) as opens, countif(was_clicked) as clicks
    from {{ref('int_notifications_with_events')}}
    group by 1,2
),
weekly_unsubs as (
    select user_id, date_trunc(Date(unsubscribed_at), week) as week_start, true as unsubscribed_this_week
    from {{ref('stg_unsubscribes')}}
)
select
    wc.user_id, wc.week_start, wc.notifications_sent,
    coalesce(wo.opens, 0) as opens, coalesce(wo.clicks,0) as clicks,
    coalesce(wu.unsubscribed_this_week, false) as unsubscribed_this_week
from weekly_counts wc
left join weekly_opens wo on wc.user_id = wo.user_id and wc.week_start = wo.week_start
left join weekly_unsubs wu on wc.user_id = wu.user_id and wc.week_start = wu.week_start
