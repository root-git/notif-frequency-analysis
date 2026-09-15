from pathlib import Path
from dagster import Definitions, load_assets_from_modules
from dagster_dbt import DbtCliResource

from notif_orchestration import assets, checks  # noqa: TID252

all_assets = load_assets_from_modules([assets])

defs = Definitions(
    assets=all_assets,
    asset_checks=[checks.no_duplicate_notification_ids, checks.no_orphaned_user_ids],
    resources={
        "dbt": DbtCliResource(project_dir=str(assets.notif_dbt_project.project_dir)),
    },
)