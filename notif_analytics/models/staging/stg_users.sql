select 
    user_id,
    cast(signup_date as date) as signup_date,
    country,
    plan_type
from {{source('notif_raw', 'raw_users')}}