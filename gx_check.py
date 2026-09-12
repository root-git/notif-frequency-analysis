import great_expectations as gx

context = gx.get_context()
validator = context.sources.pandas_default.read_csv("raw_notifications_sent.csv")

validator.expect_column_values_to_not_be_null("notification_id")
validator.expect_column_values_to_be_unique("notification_id")
validator.expect_column_values_to_be_in_set("channel", ["push", "email", "sms"])
validator.expect_column_values_to_be_in_set(
    "notification_type", ["marketing", "transactional", "reminder"]
)

results = validator.validate()
print("Overall success:", results.success)
print()
for result in results.results:
    status = "PASS" if result.success else "FAIL"
    print(f"[{status}] {result.expectation_config.expectation_type}: {result.expectation_config.kwargs}")