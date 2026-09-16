from dagster import run_failure_sensor, RunFailureSensorContext
import subprocess

@run_failure_sensor
def on_pipeline_failure(context: RunFailureSensorContext):
    subprocess.run(["python", "dq_validation_summary.py"], cwd="../notif_analytics")

    