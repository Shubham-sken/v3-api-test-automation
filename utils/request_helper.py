import requests
import configparser
import os

# Helper function to read config based on environment
def get_config():
    config = configparser.ConfigParser()
    config.read(r'C:\Users\itsup\Desktop\auto-new\v3-api-test-automation\config\config.ini')
    env = os.getenv('ENV', 'QA')  # Environment variable or default to 'QA'
    return config[env]

# Adding Authorization header to API request
def add_auth_header(headers=None):
    config = get_config()
    token = config['token']
    if headers is None:
        headers = {}
    headers['Authorization'] = f"Bearer {token}"
    headers['Content-Type'] = 'application/json'
    return headers

# GET request with dynamic base URL
def get(endpoint, headers=None, params=None):
    config = get_config()
    base_url = config['base_url']
    url = f"{base_url}/{endpoint}"
    headers = add_auth_header(headers)
    response = requests.get(url, headers=headers, params=params)
    return response

# POST request with dynamic base URL
def post(endpoint, data=None, headers=None):
    config = get_config()
    base_url = config['base_url']
    url = f"{base_url}/{endpoint}"
    headers = add_auth_header(headers)
    response = requests.post(url, json=data, headers=headers)
    return response

# GET request for CRM-related endpoints (if needed)
def get_crm(endpoint, headers=None, params=None):
    config = get_config()
    base_url_crm = config['base_url_crm']
    url = f"{base_url_crm}/{endpoint}"
    headers = add_auth_header(headers)
    response = requests.get(url, headers=headers, params=params)
    return response
