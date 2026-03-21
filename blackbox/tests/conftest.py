import pytest

BASE_URL = "http://localhost:8080/api/v1"

@pytest.fixture
def base_url():
    return BASE_URL

@pytest.fixture
def valid_headers():
    return {
        "X-Roll-Number": "2024101098",
        "X-User-ID": "1"
    }

@pytest.fixture
def admin_headers():
    return {
        "X-Roll-Number": "2024101098"
    }
