# Purpose: Create the first raw table - a synthetic user base.
# This is the "dimension" table everything else will join back to.
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42) # fixed seed so results are reproduciable across runs

N_USERS = 1000
COUNTRIES = ['US', 'GB', 'CA', 'AU', 'DE', 'IN', 'BR']
COUNTRY_WEIGHTS = [0.35, 0.15, 0.10, 0.08, 0.12, 0.12, 0.08] # rough market-share-style weighting 
TODAY = datetime(2026,8, 24)

def generate_users(n=N_USERS):
    # zero=padded IDs (u_00001) so they sort correctly as string later
    user_ids = [f"u_{i:05d}" for i in range(1, n + 1)]

    # everyone signed up well before the 90-day analysis window starts,
    # so no one is missing early weeks of notification/activity data
    signup_days_ago = np.random.randint(120, 365, size=n)
    signup_dates = [TODAY - timedelta(days=int(d)) for d in signup_days_ago]

    countries = np.random.choice(COUNTRIES, size=n, p=COUNTRY_WEIGHTS)
    plan_types = np.random.choice(['free', 'pro'], size=n, p=[0.7, 0.3])

    return pd.DataFrame({
        'user_id': user_ids,
        'signup_date': [d.strftime('%Y-%m-%d') for d in signup_dates],
        'country': countries,
        'plan_type': plan_types,
    })

if __name__ == '__main__':
    df = generate_users()
    df.to_csv('raw_users.csv', index=False)
    print(f"Generated {len(df)} users -> raw_users.csv")