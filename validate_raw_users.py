# Purpse: the first data quality gate. Schema, null, duplicated, and 
# range checks on raw_users before anything else is built on top of it.
# This is deliberately framework-free ( no dbt, no Great Expectations yet)
# the point is to internalize what a validation check actually asserts
# before reaching for a library that does it for you.

import pandas as pd
from datetime import datetime
EXPECTED_COUNTRIES = {'US', 'GB', 'CA', 'AU', 'DE', 'IN', 'BR'}
EXPECTED_PLAN_TYPES = {'free', 'pro'}

def validate(df):
    checks = []

    checks.append(("row_count == 1000", len(df) == 1000))
    checks.append(("user_id: no nulls", df['user_id'].notna().all()))
    checks.append(("user_id: no duplicates", df['user_id'].is_unique))
    checks.append(("user_id: matches u_##### format",
                   df['user_id'].str.match(r'u_\d{5}$').all()))
    checks.append(("signup_date: parse as valid date",
                   pd.to_datetime(df['signup_date'], errors='coerce').notna().all()))
    checks.append(("country: only expected values",
                   set(df['country'].unique()) <= EXPECTED_COUNTRIES))
    checks.append(("plan_type: only expected values",
                   set(df['plan_type'].unique()) <= EXPECTED_PLAN_TYPES))

    return checks

if __name__ == '__main__':
    df = pd.read_csv('raw_users.csv', dtype={'user_id': str})
    results = validate(df)

    print("== raw_users.csv validation ==")
    all_passed = True
    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        if not passed:
            all_passed =False
        print(f"[{status}] {name}")

    if not all_passed:
        raise SystemExit("Validation failed - do not proceed until fixed. ")

    print("All checks passed.")