from dagster import job
import os
from ucm_dagster.refresh import create_access_token, patch_spendesk_api_token

@job
def update_spendesk_api_key() -> None:
    client_id = os.getenv('SPENDESK_CLIENT_ID')
    client_secret = os.getenv('SPENDESK_CLIENT_SECRET')
    token = create_access_token(client_id=client_id, client_secret=client_secret)
    patch_spendesk_api_token(token)
    return 





