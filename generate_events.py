# Purpose: for every notification sent, simulate what happened to it: 
# delivered, opened, clicked, or dismissed. Open/click probability is tied
# to frequency_tier so highter-frequency users engage LESS - this is the 
# core signal the final analysis will surface.

import pandas as pd
import numpy as np 
from datetime import timedelta

np.random.seed(44)

TIER_OPEN_RATE = {'low': 0.55, 'medium': 0.35, 'high': 0.15}
TIER_CLICK_GIVEN_OPEN_RATE = {'low': 0.30, 'medium': 0.25, 'high': 0.15}

def generate_events(notifications_df, tiers_df):
    df = notifications_df.merge(tiers_df, on='user_id', how='left')
    df['sent_at'] = pd.to_datetime(df['sent_at'])

    events = []
    counter = 1

    for _, row in df.iterrows():
        notif_id, tier, sent_at = row['notification_id'], row['frequency_tier'], row['sent_at']

        delivered_at = sent_at + timedelta(minutes=np.random.randint(1,10))
        events.append({'event_id': f"e_{counter:07d}", 'notification_id': notif_id,
                        'event_type': 'delivered', 'event_at': delivered_at.strftime('%Y-%m-%d %H:%M:%S')})
        counter += 1

        if np.random.random() < TIER_OPEN_RATE[tier]:
            opened_at = delivered_at + timedelta(minutes=np.random.randint(1,720))
            events.append({'event_id': f"e_{counter:07d}", "notification_id": notif_id,
                           'event_type': 'opened', 'event_at': opened_at.strftime('%Y-%m-%d %H:%M:%S')})
            counter += 1

            if np.random.random() < TIER_CLICK_GIVEN_OPEN_RATE[tier]:
                clicked_at = opened_at + timedelta(minutes=np.random.randint(1,30))
                events.append({'event_id': f"e_{counter:07d}", 'notification_id': notif_id,
                               'event_type': 'clicked', 'event_at': clicked_at.strftime('%Y-%m-%d %H:%M:%S')})
                counter += 1

        elif np.random.random() < 0.2:
            dimissed_at = delivered_at + timedelta(minutes=np.random.randint(1,60))
            events.append({'event_id': f"e_{counter:07d}", 'notification_id':notif_id,
                           'event_type': 'dismissed', 'event_at': dimissed_at.strftime('%Y-%m-%d %H:%M:%S')})

    return pd.DataFrame(events)

if __name__ =='__main__':
    notifications_df = pd.read_csv('raw_notifications_sent.csv')
    tiers_df = pd.read_csv('_internal_user_tiers.csv')
    events_df = generate_events(notifications_df, tiers_df)
    events_df.to_csv('raw_notification_events.csv', index=False)
    print(f"Generated {len(events_df)} events -> raw_notification_events.csv")