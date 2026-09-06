select
u.user_id, u.signup_date, u.country, u.plan_type,
s.unsubscribed_at is not null as has_unsubscribed,
s.unsubscribed_at
from {{ref('stg_users')}} u
left join {{ref('stg_unsubscribes')}} s on u.user_id=s.user_id