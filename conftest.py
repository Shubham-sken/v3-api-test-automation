import pytest
import os
import configparser

# Fixture to load config.ini file
@pytest.fixture(scope="session")
def config():
    config = configparser.ConfigParser()
    config.read(r'C:\Users\itsup\Desktop\auto-new\v3-api-test-automation\config\config.ini')
    return config

# Fixture to determine the environment from an environment variable
@pytest.fixture(scope="session")
def environment():
    """Fixture to determine the environment, default is 'QA'."""
    env = os.getenv('ENV', 'QA')  # Set default to 'QA' if ENV variable isn't set
    print(f"Environment set to: {env}")
    return env

# Fixture for the API Base URL based on environment
@pytest.fixture(scope="session")
def api_base_url(config, environment):
    if environment in config:
        return config[environment]['base_url']
    else:
        raise KeyError(f"Environment '{environment}' not found in config.ini")

@pytest.fixture(scope="session")
def api_crm_base_url(config, environment):
    if environment in config:
        return config[environment]['base_url_crm']
    else:
        raise KeyError(f"Environment '{environment}' not found in config.ini")

# Fixture for Authorization Token based on environment
@pytest.fixture(scope="session")
def auth_headers(config, environment):
    if environment in config:
        token = config[environment]['token']
        return {"Authorization": f"Bearer {token}"}
    else:
        raise KeyError(f"Environment '{environment}' not found in config.ini")
