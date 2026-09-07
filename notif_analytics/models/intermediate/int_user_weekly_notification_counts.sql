select
  user_id,
  date_trunc(date(sent_at), week) as week_start,
  count(*) as notifications_sent
from {{ ref('stg_notifications_sent') }}
group by 1, 2 