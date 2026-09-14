import json
from datetime import datetime, timezone

def summarize_dbt(run_results_path="notif_analytics/target/run_results.json"):
    with open(run_results_path) as f:
        results = json.load(f)

    summary = []
    for r in results["results"]:
        if r["unique_id"].startswith("test."):
            summary.append({
                "source": "dbt",
                "check_name": r["unique_id"].split(".")[-1],
                "status": r["status"],
                "rows_affected": r.get("failures", 0),
            })
    return summary


def summarize_gx(gx_json_path, table_name):
    with open(gx_json_path) as f:
        gx_results = json.load(f)

    summary = []
    for r in gx_results["results"]:
        status = "pass" if r["success"] else "fail"
        summary.append({
            "source": f"great_expectations ({table_name})",
            "check_name": r["expectation_config"]["expectation_type"],
            "status": status,
            "rows_affected": r["result"].get("unexpected_count", 0),
        })
    return summary

if __name__ == '__main__':
    all_checks = []
    all_checks += summarize_dbt()
    all_checks += summarize_gx("gx_results_raw_notifications.json", "raw_notifications_sent")
    all_checks += summarize_gx("gx_results_fct_notifications.json", "fct_notifications")

    summary = {
        "run_at": datetime.now(timezone.utc).isoformat(),
        "total_checks": len(all_checks),
        "passed": sum(1 for c in all_checks if c["status"] =="pass"),
        "failed": sum(1 for c in all_checks if c["status"] != "pass"),
        "checks": all_checks,
    }
    with open("dq_validation_summary.josn", "w") as f:
        json.dump(summary, f, indent=2)


    print(f"=== DQ Validation Summary ({summary['run_at']}) ===")
    print(f"{summary['passed']}/{summary['total_checks']} checks passed")
    for check in summary["checks"]:
        if check["status"] != "pass":
            print(f" [FAIL] {check['check_name']} - {check['rows_affected']} rows affected")