import os

from dagster import Definitions, define_asset_job, AssetSelection
from dagster_dbt import DbtCliResource

from .assets import core_assets
from .constants import dbt_project_dir
from .schedules import schedules
from .resource import airbyte_instance
from .jobs import jobs


all_assets = [
    core_assets.airbyte_assets,
    core_assets.ucm_dbt_assets,
#    core_assets.update_spendesk_api_key
#    airbyte_clockify
]# + 

# airbyte_dbt_job = define_asset_job(
#     "airbyte_to_dbt",
#     AssetSelection.keys("ucm_dbt_assets")
#     .upstream()  # all upstream assets (in this case, just the starazers Airbyte asset)
#     .required_multi_asset_neighbors(),  # all Airbyte assets linked to the same connection
# )

defs = Definitions(
    assets=all_assets,
    schedules=schedules,
    jobs=jobs,
    resources={
        "dbt": DbtCliResource(project_dir=os.fspath(dbt_project_dir)),
     #   "airbyte": airbyte_instance,
    },
)
