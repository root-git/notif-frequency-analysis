from pathlib import Path
from dagster_dbt import DbtCliResource, DbtProject, dbt_assets
from dagster import AssetExecutionContext

notif_dbt_project = DbtProject(
    project_dir=Path(__file__).parent.parent.parent / "notif_analytics"
)

@dbt_assets(manifest=notif_dbt_project.manifest_path)
def notif_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
    


