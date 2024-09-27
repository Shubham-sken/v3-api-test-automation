import pytest
import pandas as pd
import json
from utils.request_helper import get_crm

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

def clean_expected_response(response_str):
    if pd.isna(response_str):
        return None
    try:
        return json.loads(response_str)
    except json.JSONDecodeError:
        return response_str

def call_CRMEnrichment_endpoint(api_base_url, orgid,crmid, auth_headers, additional_params=None):
    if orgid in [None, 'nan', '']:  # Check for None, 'nan', or empty string
        endpoint = "/v3/organizations//crms//enrichment-mapping"
    else:
        endpoint = f"/v3/organizations/{orgid}/crms/{crmid}/enrichment-mapping"
    if additional_params:
        params = {'other_param': additional_params}
    else:
        params = None
    print(f"Values passes:{api_base_url}{endpoint}")
    response = get_crm(endpoint, headers=auth_headers, params=params)
    return response

# Assert and validate API response
def assert_api_response(index, row, api_response):
    expected_code = int(row['code'])  # Get the expected code
    expected_response = clean_expected_response(row['response'])
    # Extract the actual response from the API
    api_response_body = extract_response_data(api_response)
    normalized_api_response = normalize_json(api_response_body)
    assert api_response.status_code == expected_code, \
        f"Row {index}: Expected status code {expected_code}, but got {api_response.status_code}. Response: {api_response.text}"
    # Compare only relevant fields in the response body
    if expected_response is not None:
        # Assuming that the API response is a dictionary
        api_response_str = normalized_api_response.get('response', None)
        print(f"Row {index}:")
        print(f"  Expected Response Message: {expected_response}")
        print(f"  Actual Response Message: {api_response_str}")
        assert api_response_str == expected_response, \
            f"Row {index}: Expected response message does not match. Expected: {expected_response}, Got: {api_response_str}"
    print(f"Row {index}: Passed with status code {api_response.status_code} and matching response body.")

@pytest.mark.parametrize("index, row", pd.read_csv(r"TestData\CRMEnrichment.csv").iterrows())
def test_CRMEnrichment_api(index, row, api_base_url, auth_headers):
    orgid = row['orgid'] if pd.notna(row['orgid']) else None
    crmid=row['crmid']
    api_response = call_CRMEnrichment_endpoint(api_base_url, orgid,crmid, auth_headers)
    assert_api_response(index, row, api_response)
