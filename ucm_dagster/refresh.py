import requests
import base64


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
    token = data['access_token']
    return token

def encode_base64(string):
    encoded_bytes = base64.b64encode(string.encode('utf-8'))
    return encoded_bytes.decode('utf-8')

def encode_client(client_id, client_secret):
    # Replace 'auth_string' with your actual authorization string.
    auth_string = str(client_id)+':'+str(client_secret)
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

