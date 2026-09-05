-- Purpose: custom singular test - user_id + week_start should be unique
-- grain. There's no built-in dbt test for compsite-key uniqueness without
-- adding the dbt_util package, and adding a dependency for one check isn't
-- worth it, so this is written directly
select user_id, week_start, count(*)
from {{ref('int_user_weekly_notification_counts')}} 
group by 1, 2
having count(*) > 1