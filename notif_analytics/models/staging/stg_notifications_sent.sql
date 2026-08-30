select
    notification_id,
    user_id,
    cast(sent_at as timestamp) as sent_at,
    channel,
    notification_type,
    campaign_id
from {{source('notif_raw', 'raw_notifications_sent')}}