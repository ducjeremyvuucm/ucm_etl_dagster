import os

from dagster import Definitions, AssetSelection, define_asset_job
from dagster_dbt import DbtCliResource

from .assets import ucm_dbt_assets, airbyte_assets, airbyte_instance, update_spendesk_api_key
from .constants import dbt_project_dir
from .schedules import schedules

my_upstream_job = define_asset_job(
    "airbyte_to_dbt",
    AssetSelection.keys("ucm_dbt_assets")
    .upstream()  # all upstream assets (in this case, just the stargazers Airbyte asset)
    .required_multi_asset_neighbors(),  # all Airbyte assets linked to the same connection
)


defs = Definitions(
    assets=[ucm_dbt_assets, airbyte_assets, update_spendesk_api_key],
    jobs=[my_upstream_job],
    schedules=schedules,
    resources={
        "dbt": DbtCliResource(project_dir=os.fspath(dbt_project_dir)),
        "airbyte":airbyte_instance
    },
)