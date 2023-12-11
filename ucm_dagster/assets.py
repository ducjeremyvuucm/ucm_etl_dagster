from dagster import AssetExecutionContext, EnvVar, asset
from dagster_dbt import DbtCliResource, dbt_assets
from dagster_airbyte import AirbyteResource, load_assets_from_airbyte_instance
import requests 
import json


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


import requests
import base64
from dotenv import load_dotenv
import os 


load_dotenv()

def create_access_token(client_id, client_secret):
    headers = {
        'Authorization': 'Basic ' + encode_client(client_id, client_secret),
        'Content-Type': 'application/json'
    }
    payload = {
        "grant_type": "client_credentials"
    }
    url = 'https://public-api.spendesk.com/v0/auth/token'
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    print(data)
    token = data['access_token']
    return token

def encode_base64(string):
    encoded_bytes = base64.b64encode(string.encode('utf-8'))
    return encoded_bytes.decode('utf-8')

def encode_client(client_id, client_secret):
    # Replace 'auth_string' with your actual authorization string.
    auth_string = str(client_id)+':'+str(client_secret)
    print(encode_base64(auth_string))
    return encode_base64(auth_string)

def patch_spendesk_api_token(token):
    airbyte_id = 'airbyte'
    airbyte_pw = 'password'

    auth = encode_client(airbyte_id, airbyte_pw)

    headers = {
        'Authorization': 'Basic ' + auth,
        'Content-Type': 'application/json'
    }
    airbyte_url = 'http://localhost:8006/v1/sources'

    body = { # renew token body 
        'configuration':{
            'api_key':token
        },
        'name':'Spendesk'
    }
    requests.put(airbyte_url+'/68ca2993-5921-464f-85bd-fba603f4eb29', headers=headers, json=body).json()
    print('spendesk api key renewed')
    return 'success'

@asset
def update_spendesk_api_key():
    client_id = os.getenv('SPENDESK_CLIENT_ID')
    client_secret = os.getenv('SPENDESK_CLIENT_SECRET')
    token = create_access_token(client_id=client_id, client_secret=client_secret)
    return patch_spendesk_api_token(token)






