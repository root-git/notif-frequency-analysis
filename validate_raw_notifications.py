# Purpose: schema + referential integrity checks. This is the first table
# where a foreign key relationship exists (user_id -? raw_users), so the
# key new check type here is referential integrity, not just column shape.

import pandas as pd

EXPECTED_CHANNELS = {'push', 'email', 'sms'}
EXPTECTED_TYPES = {'marketing', 'transactional', 'reminder'}

def validate(notif_df, user_df):
    checks = []

    checks.append(("notification_id: no nulls", notif_df['notification_id'].notna().all()))
    checks.append(("notification_id: no duplicates", notif_df['notification_id'].is_unique))
    checks.append(("user_id: no nulls", notif_df['user_id'].notna().all()))
    checks.append(("user_id: referential inegrity vs raw_users",
                   set(notif_df['user_id']) <= set(users_df['user_id'])))
    checks.append(("channel: only expected values",
                   set(notif_df['channel'].unique()) <= EXPECTED_CHANNELS))
    checks.append(("notification_type: only expected values", set(notif_df['notification_type'].unique()) <= EXPTECTED_TYPES))
    checks.append(("sent_at: parses as valid timestamp", 
                   pd.to_datetime(notif_df['sent_at'], errors='coerce').notna().all()))

    return checks 

if __name__ == '__main__':
    notif_df = pd.read_csv('raw_notifications_sent.csv', dtype={'user_id': str, 'notification_id': str})
    users_df = pd.read_csv('raw_users.csv', dtype={'user_id': str})
    results = validate(notif_df, users_df)

    print("== raw_notifications_sent.csv validation ===")
    all_passed = True
    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        if not passed:
            all_passed = False
        print(f"[{status}] {name}")

    if not all_passed:
        raise SystemExit("Validation failed - do not proceed until fixed.")
    print("All checks passed.")