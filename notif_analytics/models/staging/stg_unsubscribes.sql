select
    user_id,
    cast(unsubscribed_at as timestamp) as unsubscribed_at,
    channel
from {{source('notif_raw', 'raw_unsubscribes')}}