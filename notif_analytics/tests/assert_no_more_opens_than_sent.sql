select user_id, week_start, notifications_sent, opens
from {{ref('fct_user_weekly_frequency')}}
where opens > notifications_sent