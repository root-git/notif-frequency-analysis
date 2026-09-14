import great_expectations as gx
import json

context = gx.get_context()
validator = context.sources.pandas_default.read_csv("raw_notifications_sent.csv")

validator.expect_column_values_to_not_be_null("notification_id")
validator.expect_column_values_to_be_unique("notification_id")
validator.expect_column_values_to_be_in_set("channel", ["push", "email", "sms"])
validator.expect_column_values_to_be_in_set(
    "notification_type", ["marketing", "transactional", "reminder"]
)

results = validator.validate()

with open("gx_results_raw_notifications.json", "w") as f:
    json.dump(results.to_json_dict(), f, indent=2) 
    
print("Overall success:", results.success)
print()
for result in results.results:
    status = "PASS" if result.success else "FAIL"
    print(f"[{status}] {result.expectation_config.expectation_type}: {result.expectation_config.kwargs}")