from dagster import AssetExecutionContext, asset
from dagster_dbt import DbtCliResource, dbt_assets
from dagster_airbyte import load_assets_from_airbyte_instance
from ucm_dagster.resource import airbyte_instance

from ucm_dagster.constants import dbt_manifest_path
from ucm_dagster.refresh import create_access_token, patch_spendesk_api_token


import os 

@dbt_assets(manifest=dbt_manifest_path)
def ucm_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()

@asset
def update_spendesk_api_key() -> None:
    client_id = os.getenv('SPENDESK_CLIENT_ID')
    client_secret = os.getenv('SPENDESK_CLIENT_SECRET')
    token = create_access_token(client_id=client_id, client_secret=client_secret)
    patch_spendesk_api_token(token)
    return 


airbyte_assets = load_assets_from_airbyte_instance(airbyte_instance)
