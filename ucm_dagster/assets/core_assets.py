from dagster import AssetExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets
from dagster_airbyte import load_assets_from_airbyte_instance
from ucm_dagster.resource import airbyte_instance

from ucm_dagster.constants import dbt_manifest_path


@dbt_assets(manifest=dbt_manifest_path)
def ucm_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()


airbyte_assets = load_assets_from_airbyte_instance(airbyte_instance)
