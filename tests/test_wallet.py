import socket
import py_test
import requests
import threading


from typing import Dict, Any

# from multiapi_routes.Routes.Wallet import Wallet

# def test_server():
#     app = FastAPI()

#     #app.include_router(Wallet())

#     # Run the FastAPI server in a thread
#     def run_server():
#         uvicorn.run("test_wallet:app", host="0.0.0.0", port=8001)

#     # Start the server in a separate thread
#     server_thread = threading.Thread(target=run_server)
#     server_thread.start()

import random
import string

def generate_random_api():
    # Generate a random API name
    api_name = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    # Generate random API keys
    api_key = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    api_secret = ''.join(random.choices(string.ascii_letters + string.digits, k=32))

    return api_name, api_key, api_secret

ENDPOINT = "http://127.0.0.1:8000/v1/multiapi/wallets"

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
    'token' : '543eb83e3ff14d23ce6dac3c4f21bef40552ae479f590bb6bb72bfd0f2d4066b0b9a15c59c17c2d3ae2cec012ec4d1795eb9aaa3c9a7837a7c0c962c3c177533'
}

def test_wgenerate_random_apiallet_get():
    keys_ =  {
        "id": str,
        "author": str,
        "key_wallet": Dict[str, str],
        "date_created_timestamp": float,
        "date_updated_timestamp": float,
        "date_accessed_timestamp": float
    }

    response = requests.get(ENDPOINT,headers=headers)
    assert response.status_code == 200
    if isinstance(response.json(), list):
        response = response.json()[0]
    else:
        response = response.json()
    assert response.json().keys() == keys_.keys()
    assert len([_ for _ in response.json().keys() if isinstance(response.json()[_], keys_[_])]) == len(keys_.keys())

def test_wallet_post():
    keys_ =  {
        "id": str,
        "author": str,
        "key_wallet": Dict[str, str],
        "date_created_timestamp": float,
        "date_updated_timestamp": float,
        "date_accessed_timestamp": float
    }
    name,api_key,secret = generate_random_api()

    json_params = {
        "key_wallet" : {name:api_key}
    }

    response = requests.post(ENDPOINT,headers=headers,json=json_params)
    assert response.status_code == 200
    if isinstance(response.json(), list):
        response = response.json()[0]
    else:
        response = response.json()
    assert response.json().keys() == keys_.keys()
    assert len([_ for _ in response.json().keys() if isinstance(response.json()[_], keys_[_])]) == len(keys_.keys())