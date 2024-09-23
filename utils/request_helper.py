
import requests
from config.config import BASE_URL, TOKEN

def add_auth_header(headers=None):
    if headers is None:
        headers = {}
    headers['Authorization'] = f"Bearer {TOKEN}"
    headers['Content-Type'] = 'application/json'
    return headers

def get(endpoint, headers=None, params=None):
    url = f"{BASE_URL}/{endpoint}"
    headers = add_auth_header(headers)
    response = requests.get(url, headers=headers, params=params)
    return response

def post(endpoint, data=None, headers=None):
    url = f"{BASE_URL}/{endpoint}"
    headers = add_auth_header(headers)
    response = requests.post(url, json=data, headers=headers)
    return response


