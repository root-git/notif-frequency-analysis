-- confirm Fault A: which notification_ids are duplicated, and by how much
select notification_id, count(*) as row_count
from notif_raw.raw_notifications_sent
group by 1 having count(*) > 1
order by row_count desc;

-- confirm Fault B: which notifications reference a user_id that doesn't exist 
select n.notification_id, n.user_id
from notif_raw.raw_notifications_sent n
left join notif_raw.raw_user u on n.user_id=u.user_id
where u.user_id is null;