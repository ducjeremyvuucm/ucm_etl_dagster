from dagster import with_resources, AssetExecutionContext, AssetKey
from dagster_dbt import DbtCliResource, dbt_assets, load_assets_from_dbt_project
from dagster_airbyte import load_assets_from_airbyte_instance, build_airbyte_assets
from ucm_dagster.resource import airbyte_instance

from ucm_dagster.constants import dbt_manifest_path
from ucm_dagster.refresh import create_access_token, patch_spendesk_api_token


import os 


@dbt_assets(manifest=dbt_manifest_path)
def ucm_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()



# airbyte_clockify = build_airbyte_assets(connection_id = "baa9848c-9558-4503-8534-91863ad20c22", destination_tables=['clients','projects','tags','tasks','time_entries','user_groups','users'], asset_key_prefix='airbyte')


# airbyte_assets = with_resources(
#     airbyte_clockify,
#     {'airbyte': airbyte_instance}
# )

airbyte_assets = load_assets_from_airbyte_instance(
    airbyte_instance,connection_to_asset_key_fn=lambda c, n: AssetKey([n]), key_prefix=["sources"]
)

# airbyte_assets = load_assets_from_airbyte_instance(airbyte_instance)
