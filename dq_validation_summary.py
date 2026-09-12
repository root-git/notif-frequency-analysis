import json
from datetime import datetime, timezone

def summarize(run_results_path="notif_analytics/target/run_results.json"):
    with open(run_results_path) as f:
        results = json.load(f)

    summary = []
    for r in results["results"]:
        if r["unique_id"].startswith("test."):
            summary.append({
                "check_name": r["unique_id"].split(".")[-1],
                "status": r["status"],
                "row_affected": r.get("failures", 0),
                "execution_time_seconds": round(r["execution_time"], 2),
            })

    return {
        "run_at": datetime.now(timezone.utc).isoformat(),
        "total_checks": len(summary),
        "passed": sum(1 for s in summary if s["status"] == "pass"),
        "failed": sum(1 for s in summary if s["status"] != "pass"),
        "checks": summary,
        }

if __name__ == '__main__':
    summary = summarize()
    with open("dq_validation_summary.josn", "w") as f:
        json.dump(summary, f, indent=2
        )


    print(f"=== DQ Validation Summary ({summary['run_at']}) ===")
    print(f"{summary['passed']}/{summary['total_checks']} checks passed")
    for check in summary["checks"]:
        if check["status"] != "pass":
            print(f" [FAIL] {check['check_name']} - {check['row_affected']} rows affected")