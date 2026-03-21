from utils import get, put, assert_json


# ---------- GET /profile ----------

def test_get_profile_valid(base_url, valid_headers):
    r = get(f"{base_url}/profile", headers=valid_headers)

    assert r.status_code == 200
    assert_json(r)

    data = r.json()
    assert isinstance(data, dict)

    assert isinstance(data["user_id"], int)
    assert isinstance(data["name"], str)
    assert isinstance(data["email"], str)
    assert isinstance(data["phone"], str)
    assert isinstance(data["wallet_balance"], (int, float))
    assert isinstance(data["loyalty_points"], int)

    assert 2 <= len(data["name"]) <= 50
    assert data["phone"].isdigit()
    assert len(data["phone"]) == 10

def test_get_profile_missing_header(base_url):
    r = get(f"{base_url}/profile")
    assert r.status_code == 401

def test_get_profile_invalid_header(base_url):
    r = get(f"{base_url}/profile", headers={"X-Roll-Number": "abc"})
    assert r.status_code == 400

def test_get_profile_missing_user_id(base_url):
    headers = {"X-Roll-Number": "2024101098"}
    r = get(f"{base_url}/profile", headers=headers)
    assert r.status_code == 400

# ---------- PUT /profile ----------

def test_put_profile_valid(base_url, valid_headers):
    payload = {
        "name": "John Doe",
        "phone": "9876543210"
    }

    r = put(f"{base_url}/profile", headers=valid_headers, json=payload)

    assert r.status_code == 200
    assert_json(r)

    data = r.json()

    assert "message" in data
    assert isinstance(data["message"], str)
    assert data["message"] == "Profile updated successfully"

def test_put_profile_missing_name(base_url, valid_headers):
    payload = {"phone": "9876543210"}
    r = put(f"{base_url}/profile", headers=valid_headers, json=payload)
    assert r.status_code == 400


def test_put_profile_missing_phone(base_url, valid_headers):
    payload = {"name": "John"}
    r = put(f"{base_url}/profile", headers=valid_headers, json=payload)
    assert r.status_code == 400

def test_put_profile_name_too_short(base_url, valid_headers):
    payload = {"name": "A", "phone": "9876543210"}
    r = put(f"{base_url}/profile", headers=valid_headers, json=payload)
    assert r.status_code == 400

def test_put_profile_name_too_long(base_url, valid_headers):
    payload = {"name": "A" * 51, "phone": "9876543210"}
    r = put(f"{base_url}/profile", headers=valid_headers, json=payload)
    assert r.status_code == 400

def test_put_profile_phone_too_short(base_url, valid_headers):
    payload = {"name": "John", "phone": "12345"}
    r = put(f"{base_url}/profile", headers=valid_headers, json=payload)
    assert r.status_code == 400

def test_put_profile_phone_too_long(base_url, valid_headers):
    payload = {"name": "John", "phone": "1" * 11}
    r = put(f"{base_url}/profile", headers=valid_headers, json=payload)
    assert r.status_code == 400

def test_put_profile_phone_non_numeric(base_url, valid_headers):
    payload = {"name": "John", "phone": "abcd123456"}
    r = put(f"{base_url}/profile", headers=valid_headers, json=payload)
    assert r.status_code == 400


def test_put_profile_name_wrong_type(base_url, valid_headers):
    payload = {"name": 12345, "phone": "9876543210"}
    r = put(f"{base_url}/profile", headers=valid_headers, json=payload)
    assert r.status_code == 400

def test_put_profile_name_boundary_min(base_url, valid_headers):
    payload = {"name": "AB", "phone": "9876543210"}
    r = put(f"{base_url}/profile", headers=valid_headers, json=payload)
    assert r.status_code == 200

def test_put_profile_name_boundary_max(base_url, valid_headers):
    payload = {"name": "A" * 50, "phone": "9876543210"}
    r = put(f"{base_url}/profile", headers=valid_headers, json=payload)
    assert r.status_code == 200

def test_put_profile_phone_boundary_exact(base_url, valid_headers):
    payload = {"name": "John", "phone": "1" * 10}
    r = put(f"{base_url}/profile", headers=valid_headers, json=payload)
    assert r.status_code == 200

def test_put_profile_missing_header(base_url):
    payload = {"name": "John", "phone": "9876543210"}
    r = put(f"{base_url}/profile", json=payload)
    assert r.status_code == 401

def test_put_profile_invalid_header(base_url):
    payload = {"name": "John", "phone": "9876543210"}
    r = put(f"{base_url}/profile", headers={"X-Roll-Number": "abc"}, json=payload)
    assert r.status_code == 400

def test_put_profile_missing_user_id(base_url):
    payload = {"name": "John", "phone": "9876543210"}
    headers = {"X-Roll-Number": "2024101098"}
    r = put(f"{base_url}/profile", headers=headers, json=payload)
    assert r.status_code == 400
