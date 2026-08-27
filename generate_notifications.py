# Purpose: generate the notications each user received.
# Key idea: each use issecretly assigned a "frequency_tier" (low/medium/high)
# that controls how many notifications they get per week. this tier is the 
# hidden varible the whole project is designed to uncover later. 
# It is NOT written into raw_users, so the eventual analysis is a real query result.
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(43)

ANALYSIS_START = datetime(2026, 5, 25) # ~90 daus before TODAY
CHANNELS = ['push', 'email', 'sms']
CHANNELS_WEIGHTS = [0.55, 0.35, 0.10]
NOTIF_TYPES = ['marketing', 'transactional', 'reminder']
NOTIF_TYPE_WEIGHTS = [0.5, 0.2, 0.3]
CAMPAIGNS = [f"c_{i:02d}" for i in range(1,11)]

# weekly send-count RANGE per tier - this is the independent variable
TIER_WEEKLY_TARGET = {'low': (1,2), 'medium': (3,5), 'high': (8,12)}
TIER_WEIGHTS = {'low': 0.4, 'medium': 0.4, 'high': 0.2} # most uses are low/medium; fewer are spammed hard

def assign_tiers(user_ids):
    tiers = np.random.choice(list(TIER_WEIGHTS.keys()), size=len(user_ids), p=list(TIER_WEIGHTS.values()))
    return pd.DataFrame({'user_id': user_ids, 'frequency_tier': tiers})

def generate_notification(users_df):
    tiers_df = assign_tiers(users_df['user_id'].tolist())
    notifications = []
    notif_counter = 1

    for _, row in tiers_df.iterrows():
        user_id, tier =row['user_id'], row['frequency_tier']
        low, high = TIER_WEEKLY_TARGET[tier]

        for week in range(13): # 13 weeks ~=90 days
            weekly_count = np.random.randint(low, high + 1)
            week_start = ANALYSIS_START + timedelta(weeks=week)

            for _ in range(weekly_count):
                sent_at = week_start + timedelta(hours=np.random.uniform(0,7*24))
                notifications.append({
                    'notification_id': f"n_{notif_counter:06d}",
                    'user_id': user_id,
                    'sent_at': sent_at.strftime('%Y-%m-%d %H:%M:%S'),
                     'channel': np.random.choice(CHANNELS, p=CHANNELS_WEIGHTS),
                     'notification_type': np.random.choice(NOTIF_TYPES, p=NOTIF_TYPE_WEIGHTS),
                     'campaign_id': np.random.choice(CAMPAIGNS)
                })
                notif_counter += 1
    return pd.DataFrame(notifications), tiers_df

if __name__ == '__main__':
    users_df = pd.read_csv('raw_users.csv')
    notification_df, tiers_df = generate_notification(users_df)
    notification_df.to_csv('raw_notifications_sent.csv', index=False)
    tiers_df.to_csv('_internal_user_tiers.csv', index=False)
    print(f"Generated {len(notification_df)} notifications -> raw_notification_sent.csv")