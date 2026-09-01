select
    event_id,
    notification_id,
    event_type,
    cast(event_at as timestamp) as event_at
from {{source('notif_raw', 'raw_notification_events')}}