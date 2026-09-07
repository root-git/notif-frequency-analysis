select
   notification_id, user_id, sent_at, channel, notification_type, campaign_id
   was_opened, was_clicked, delivered_at, opened_at, clicked_at
   from {{ref('int_notifications_with_events')}}