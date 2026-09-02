# Purpose: same pattern applied to the last two raw tables.

import pandas as pd

def validate(unsub_df, activity_df, users_df):
    checks = []

    checks.append(("unsubscribes: user_id refrential integrity",
                   set(unsub_df['user_id']) <= set(users_df['user_id'])))
    checks.append(("unsubscribes: unsubscribed_at parses as valid timestamp",
                   pd.to_datetime(unsub_df['unsubscribed_at'], errors='coerce').notna().all()))
    checks.append(("activity: activity_id no nulls", activity_df['activity_id'].notna().all()))
    checks.append(("activity: activity_id no duplicates", activity_df['activity_id'].is_unique))
    checks.append(("activity: user_id referential integrity",
                   set(activity_df['user_id']) <= set(users_df['user_id'])))
    checks.append(("activity: activity_type only expected values", 
                   set(activity_df['activity_type'].unique()) <= {'app_open', 'session_end'}))
    checks.append(("activity: activity_at parses as valid timestamp",
                pd.to_datetime(activity_df['activity_at'], errors='coerce').notna().all()))

    return checks

if __name__ == '__main__':
    unsub_df = pd.read_csv('raw_unsubscribes.csv', dtype={'user_id': str})
    activity_df = pd.read_csv('raw_user_activity.csv', dtype={'user_id': str, 'activity_id': str})
    users_df = pd.read_csv('raw_users.csv', dtype={'user_id': str})
    results = validate(unsub_df, activity_df, users_df)

    print("=== raw_unsubscribes.csv + raw_user_activity.csv validation ===")
    all_passed = True
    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        if not passed:
            all_passed = False
        print(f"[{status}] {name}")

    if not all_passed:
        raise SystemExit("Validation failed - d not proceed until fixed.")
    print("All checks passed.")