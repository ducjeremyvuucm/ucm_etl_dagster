from dagster import AssetExecutionContext, EnvVar, asset
from dagster_dbt import DbtCliResource, dbt_assets
from dagster_airbyte import AirbyteResource, load_assets_from_airbyte_instance

from .refresh import create_access_token, patch_spendesk_api_token

from dotenv import load_dotenv
import os 


load_dotenv()

from .constants import dbt_manifest_path


@dbt_assets(manifest=dbt_manifest_path)
def ucm_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()




airbyte_instance = AirbyteResource(
    host="localhost",
    port="8000",
    # If using basic auth, include username and password:
    username="airbyte",
    password=EnvVar("AIRBYTE_PASSWORD"),
)

# Use the airbyte_instance resource we defined in Step 1
airbyte_assets = load_assets_from_airbyte_instance(airbyte_instance)



@asset
def update_spendesk_api_key() -> None:
    client_id = os.getenv('SPENDESK_CLIENT_ID')
    client_secret = os.getenv('SPENDESK_CLIENT_SECRET')
    token = create_access_token(client_id=client_id, client_secret=client_secret)
    patch_spendesk_api_token(token)






