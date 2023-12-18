import os

from dagster import Definitions
from dagster_dbt import DbtCliResource

from .assets import core_assets
from .constants import dbt_project_dir
from .schedules import schedules
from .resource import airbyte_instance

all_assets = [
    #    core_assets.airbyte_assets,
    core_assets.ucm_dbt_assets
]


defs = Definitions(
    assets=all_assets,
    schedules=schedules,
    resources={
        "dbt": DbtCliResource(project_dir=os.fspath(dbt_project_dir)),
        "airbyte": airbyte_instance,
    },
)
