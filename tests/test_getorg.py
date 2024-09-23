# tests/test_get_user.py
import pytest
from utils.request_helper import get

# Test to retrieve a user
def test_get_user():
    response = get("/v3/organizations")  
    assert response.status_code == 200


