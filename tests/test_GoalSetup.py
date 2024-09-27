import pytest
import pandas as pd
import json
from utils.request_helper import get

# Function to normalize JSON structure for comparison
def normalize_json(json_data):
    if isinstance(json_data, str):
        try:
            json_data = json.loads(json_data)
        except json.JSONDecodeError:
            return json_data  # Return as-is if not JSON
    return json_data

# Function to extract relevant part of API response
def extract_response_data(api_response):
    try:
        return api_response.json()
    except ValueError:
        return api_response.text  # Return as text if not JSON

# Make API request based on test data inputs
def call_GoalSetup_endpoint(api_base_url, orgid,auth_headers, additional_params=None):
    if orgid in [None, 'nan', '']:  # Check for None, 'nan', or empty string
        endpoint = "/v3/organizations//goals"
    else:
        endpoint = f"/v3/organizations/{orgid}/goals"
    if additional_params:
        params = {'other_param': additional_params}
    else:
        params = None
    print(f"Values passes:{api_base_url}{endpoint}")
    response = get(endpoint, headers=auth_headers, params=params)
    return response
# Clean and process expected response from CSV
def clean_expected_response(response_str):
    if pd.isna(response_str):
        return None
    try:
        # Try to parse the string as JSON (for lists or dicts)
        return json.loads(response_str.replace("'", '"'))  # Ensure single quotes are replaced with double quotes for valid JSON
    except json.JSONDecodeError:
        # If it's not valid JSON, return the string as-is
        return response_str

# Assert and validate API response
def assert_api_response(index, row, api_response):
    expected_code = int(row['code'])  # Get the expected code
    expected_response = clean_expected_response(row['response'])  # Get the expected response message
    # Extract the actual response from the API
    api_response_body = extract_response_data(api_response)
    normalized_api_response = normalize_json(api_response_body)
    # Assert status code matches
    assert api_response.status_code == expected_code, \
        f"Row {index}: Expected status code {expected_code}, but got {api_response.status_code}. Response: {api_response.text}"
    # Compare only relevant fields in the response body
    if expected_response is not None:
        # Assuming that the API response is a dictionary
        api_response_str = normalized_api_response.get('response', None)
        # If the expected response is a list, ensure the API response is also treated as a list
        if isinstance(expected_response, list) and not isinstance(api_response_str, list):
            api_response_str = [api_response_str]
        # Debug prints for expected and actual values
        print(f"Row {index}:")
        print(f"  Expected Response Message: {expected_response}")
        print(f"  Actual Response Message: {api_response_str}")
        # Assertion for the response
        assert api_response_str == expected_response, \
            f"Row {index}: Expected response message does not match. Expected: {expected_response}, Got: {api_response_str}"

    print(f"Row {index}: Passed with status code {api_response.status_code} and matching response body.")

@pytest.mark.parametrize("index, row", pd.read_csv(r"TestData\GoalSetup.csv").iterrows())
def test_GoalSetup_api(index, row, api_base_url, auth_headers):
    orgid = row['orgid'] if pd.notna(row['orgid']) else None
    api_response = call_GoalSetup_endpoint(api_base_url, orgid, auth_headers)
    assert_api_response(index, row, api_response)
