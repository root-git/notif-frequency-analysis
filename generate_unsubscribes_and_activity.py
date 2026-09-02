# Purpose: two more raw tables.
# - raw_unsubscribers: high-tier users unsubscribe more often (the other
# half of the "high frequency hurts engagement" signals).
# - raw_user_activity: organic app usage, generated INDEPENDENTLY of
# notification tier, so it acts as a neutral baseline engagement signal.

import pandas as pd
import numpy as np 
from datetime import datetime, timedelta

np.random.seed(45)
ANALYSIS_START = datetime(2026,5,25)
ANALYSIS_DAYS = 90
TIER_UNSUB_RATE = {'low': 0.3, 'medium':0.08, 'high':0.25}

def generate_unsubscribes(tiers_df):
    rows = []
    for _, row in tiers_df.iterrows():
        tier = row['frequency_tier']
        if np.random.random() < TIER_UNSUB_RATE[tier]:
            unsub_day = np.random.randint(5, ANALYSIS_DAYS)
            unsub_at = ANALYSIS_START + timedelta(days=int(unsub_day), hours=np.random.uniform(0,24))
            rows.append({'user_id': row['user_id'], 'unsubscribed_at': unsub_at.strftime('%Y-%m-%d %H:%M:%S'),
                         'channel': np.random.choice(['push', 'email', 'sms'], p=[0.55, 0.35, 0.10])})
    return pd.DataFrame(rows)

def generate_activity(users_df, n_days=ANALYSIS_DAYS):
    rows, counter = [], 1
    for _, row in users_df.iterrows():
        user_id = row['user_id']
        daily_open_prob = np.random.uniform(0.1,0.6)
        for day in range(n_days):
            if np.random.random() < daily_open_prob:
                start = ANALYSIS_START + timedelta(days=day, hours=np.random.uniform(0,24))
                rows.append({'activity_id': f"a_{counter:07d}", 'user_id': user_id,
                             'activity_at': start.strftime('%Y-%m-%d %H:%M:%S'), 'activity_type': 'session_end'})
                counter += 1
    return pd.DataFrame(rows)

if __name__ == '__main__':
    users_df = pd.read_csv('raw_users.csv')
    tiers_df = pd.read_csv('_internal_user_tiers.csv')

    unsub_df = generate_unsubscribes(tiers_df)
    unsub_df.to_csv('raw_unsubscribes.csv', index=False)
    print(f"Generate {len(unsub_df)} unsubscribes -> raw_unsubscribes.csv")

    activity_df = generate_activity(users_df)
    activity_df.to_csv('raw_user_activity.csv', index=False)
    print(f"Generated {len(activity_df)} activity rows -> raw_user_activity.csv")
