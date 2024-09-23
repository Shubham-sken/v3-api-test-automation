import pytest
import os
import configparser

# Load config.ini file
config = configparser.ConfigParser()

# Use a raw string or double backslashes for the path
config.read(r'C:\Users\itsup\Desktop\auto-new\v3-api-test-automation\config\config.ini')

@pytest.fixture(scope="session")
def environment():
    """Fixture to determine the environment from an environment variable."""
    env = os.getenv('ENV', 'QA')
    print(f"Environment set to: {env}")
    return env

@pytest.fixture(scope="session")
def auth_headers(environment):
    """Fixture to provide authorization headers with a token read from the config file."""
    token = config.get(environment, 'token')
    return {"Authorization": token}
