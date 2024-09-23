import requests
import configparser

# Read config.ini
config = configparser.ConfigParser()
config.read(r'C:\Users\itsup\Desktop\auto-new\v3-api-test-automation\config\config.ini')  # Path to your config.ini file

# Select the environment (This could be dynamic based on environment variable)
environment = 'QA'  # Or 'DEV', 'PROD', etc.
BASE_URL = config[environment]['BASE_URL']
TOKEN = config[environment]['TOKEN']

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
