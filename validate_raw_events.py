# validate_raw_events.py
# Purpose: referential integrity + a chronological business-rule check.
# The new check type here is ORDERING — delivered must happen before
# opened, which must happen before clicked. This is the kind of check
# that schema-only validation (types, nulls, sets) never catches.
import pandas as pd

EXPECTED_EVENT_TYPES = {'delivered', 'opened', 'clicked', 'dismissed'}

def validate(events_df, notif_df):
    checks = []

    checks.append(("event_id: no nulls", events_df['event_id'].notna().all()))
    checks.append(("event_id: no duplicates", events_df['event_id'].is_unique))
    checks.append(("notification_id: referential integrity vs raw_notifications_sent",
                    set(events_df['notification_id']) <= set(notif_df['notification_id'])))
    checks.append(("event_type: only expected values",
                    set(events_df['event_type'].unique()) <= EXPECTED_EVENT_TYPES))

    pivot = events_df.pivot_table(index='notification_id', columns='event_type',
                                   values='event_at', aggfunc='first')
    for col in ['delivered', 'opened', 'clicked']:
        if col not in pivot.columns:
            pivot[col] = pd.NaT
        pivot[col] = pd.to_datetime(pivot[col])

    opened_after_delivered = ((pivot['opened'].isna()) |
                               (pivot['opened'] >= pivot['delivered'])).all()
    clicked_after_opened = ((pivot['clicked'].isna()) |
                             (pivot['clicked'] >= pivot['opened'])).all()
    checks.append(("chronological order: opened >= delivered", bool(opened_after_delivered)))
    checks.append(("chronological order: clicked >= opened", bool(clicked_after_opened)))

    return checks

if __name__ == '__main__':
    events_df = pd.read_csv('raw_notification_events.csv', dtype={'notification_id': str, 'event_id': str})
    notif_df = pd.read_csv('raw_notifications_sent.csv', dtype={'notification_id': str})
    results = validate(events_df, notif_df)

    print("=== raw_notification_events.csv validation ===")
    all_passed = True
    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        if not passed:
            all_passed = False
        print(f"[{status}] {name}")

    if not all_passed:
        raise SystemExit("Validation failed — do not proceed until fixed.")
    print("All checks passed.")