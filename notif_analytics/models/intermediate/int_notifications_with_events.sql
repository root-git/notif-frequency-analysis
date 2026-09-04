-- Purpose: turn the ling/skinny events table (one row per event) into one 
-- row per notification with delivered/opened/cliced/dismissed as columns.

with notifications as (
    select * from {{ref('stg_notifications_sent')}}
),
events as (
    select * from {{ref('stg_notification_events')}}
),
events_pivoted as (
    select
        notification_id,
        max(case when event_type = 'delivered' then event_at end) as delivered_at,
        max(case when event_type = 'opened' then event_at end) as opened_at,
        max(case when event_type = 'clicked' then event_at end) as clicked_at,
        max(case when event_type = 'dismissed' then event_at end) as dismissed_at
    from events
    group by notification_id
)

select
    n.notification_id, n.user_id, n.sent_at, n.channel, n.notification_type,
    e.delivered_at, e.opened_at, e.clicked_at, e.dismissed_at,
    e.opened_at is not null as was_opened,
    e.clicked_at is not null as was_clicked,
from notifications n
left join events_pivoted e on n.notification_id = e.notification_id
