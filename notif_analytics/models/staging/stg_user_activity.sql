select
    activity_id,
    user_id,
    cast(activity_at as timestamp) as activity_at,
    activity_type
from {{ source('notif_raw', 'raw_user_activity') }}