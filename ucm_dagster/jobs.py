from dagster import job, define_asset_job, AssetSelection, op
from dagster_airbyte import airbyte_sync_op
from .refresh import create_access_token, patch_spendesk_api_token
from .resource import airbyte_instance
import os
from .assets.core_assets import update_spendesk_api_key, airbyte_assets


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

@job(resource_defs={"airbyte":airbyte_instance})
def spendesk():
    refresh_spendesk = sync_spendesk(start_after=update_spendesk_api_key())

# spendesk = define_asset_job(
#     "spendesk",
#     selection=AssetSelection.groups("spend")
# )



jobs = [
    spendesk
]


