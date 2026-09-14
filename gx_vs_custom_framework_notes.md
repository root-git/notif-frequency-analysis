# Great Expectations vs. a Custom SQL DQ Framework

Great Expectations trades flexibility for standardization: instead of
hand-writing SQL for every check, you declare intent (`expect_column_
values_to_be_unique`) and GX handles the query generation, result
formatting, and suite management underneath. That's valuable for
consistency across a team and for onboarding — anyone who knows GX's
vocabulary can read any check, whereas a custom SQL framework's checks
are only as readable as whoever wrote the SQL made them.

The trade-off is expressiveness: a custom SQL framework can encode
business logic no generic library anticipates in advance — like this
project's chronological-ordering check (delivered before opened before
clicked) or a composite-key uniqueness rule. GX has a large expectation
library, but anything outside it means either finding a workaround
expectation or dropping back to a custom SQL/Python check anyway — which
is exactly what happened here for the checks GX's built-ins didn't cover.

A concrete example from this project: a missing comma in a dbt model
silently aliased one column as another (valid SQL, no error). It passed
every dbt schema test for three weeks because those tests only checked
null/uniqueness, never actual column values. Great Expectations caught
it immediately, because its value-set checks inspect real data content
— a category of test the dbt suite didn't have for that column. Neither
framework is "better"; they were checking different things.