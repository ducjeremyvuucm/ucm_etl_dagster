from dagster import with_resources, AssetExecutionContext, AssetKey, asset, op
from dagster_dbt import DbtCliResource, dbt_assets, load_assets_from_dbt_project
from dagster_airbyte import load_assets_from_airbyte_instance, build_airbyte_assets, airbyte_sync_op
from ucm_dagster.resource import airbyte_instance

from ucm_dagster.constants import dbt_manifest_path
from ucm_dagster.refresh import create_access_token, patch_spendesk_api_token


import os 


@dbt_assets(manifest=dbt_manifest_path)
def ucm_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()



airbyte_assets = load_assets_from_airbyte_instance(
    airbyte_instance,connection_to_asset_key_fn=lambda c, n: AssetKey([n]), key_prefix=["sources"], connection_to_group_fn=lambda c:c[:5].replace(":","_").lower()
)

# airbyte_assets = load_assets_from_airbyte_instance(airbyte_instance)
@op(
    description="refreshes the spendesk api token"
)
def update_spendesk_api_key() -> None:
    client_id = os.getenv('SPENDESK_CLIENT_ID')
    client_secret = os.getenv('SPENDESK_CLIENT_SECRET')
    token = create_access_token(client_id=client_id, client_secret=client_secret)
    patch_spendesk_api_token(token)
    return 

sync_spendesk = airbyte_sync_op.configured({"connection_id":"bcb4a837-4784-4647-a213-b161e0c12df5"}, name="sync_spendesk")