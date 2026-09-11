-- Purpose: aggregate table for hypothesis validation - buckets each 
-- user-week by notification volume and computes open rate and unsubscribe 
-- rate per bucket. This is a technical aggregate, consumed by query or by 
-- the validation summary below - not a stakehorlder-facing report.

with bucketed as (
    select
        user_id, week_start, notifications_sent, opens, unsubscribed_this_week,
        case
            when notifications_sent <= 2 then '1-2 per week'
            when notifications_sent <= 5 then '3-5 per week'
            when notifications_sent <= 8 then "6-8 per week"
            else '9+ per week'
        end as frequency_bucket
    from {{ref('fct_user_weekly_frequency')}}
    where notifications_sent > 0
)

select 
    frequency_bucket,
    count(*) as user_weeks,
    sum(notifications_sent) as total_notifications,
    sum(opens) as total_opens,
    round(safe_divide(sum(opens), sum(notifications_sent)), 3) as open_rate,
    round(safe_divide(countif(unsubscribed_this_week), count(*)), 4) as unsubscribe_ratio
from bucketed
group by 1
order by case frequency_bucket
when '1-2 per week' then 1 when '3-5 per week' then 2
when '6-8 per week' then 3 else 4 end