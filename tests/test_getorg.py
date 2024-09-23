import pytest
from utils.request_helper import get

def test_get_user(environment, auth_headers):
    response = get("/v3/organizations", headers=auth_headers)
    assert response.status_code == 200
