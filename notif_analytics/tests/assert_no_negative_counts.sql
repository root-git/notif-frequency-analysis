-- Purpose: sanity rule - aggregated counts should never be negative.
-- Catches a whole class of aggregation bugs ( bag joins fanning out signs,
-- miscounted coalesce logic) that type/null tests won't catch.
select user_id, total_notifications, total_opens, total_clicks, total_app_opens
from {{ref('int_user_engagement_summary')}}
where total_notifications < 0
   or total_opens < 0
   or total_clicks < 0
   or total_app_opens < 0