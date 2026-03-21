from utils import get, post, put, delete, assert_json

# ---------- GET /addresses ----------

def test_get_addresses_valid(base_url, valid_headers):
    r = get(f"{base_url}/addresses", headers=valid_headers)
    assert r.status_code == 200
    assert_json(r)
    data = r.json()
    assert isinstance(data, list)
    for addr in data:
        assert isinstance(addr["address_id"], int)
        assert addr["label"] in ["HOME", "OFFICE", "OTHER"]
        assert isinstance(addr["street"], str)
        assert isinstance(addr["city"], str)
        assert isinstance(addr["pincode"], str)
        assert isinstance(addr["is_default"], bool)

def test_get_addresses_missing_header(base_url):
    r = get(f"{base_url}/addresses")
    assert r.status_code == 401

def test_get_addresses_invalid_header(base_url):
    r = get(f"{base_url}/addresses", headers={"X-Roll-Number": "abc"})
    assert r.status_code == 400

# ---------- POST /addresses (spec validation) ----------

def test_post_address_valid(base_url, valid_headers):
    payload = {
        "label": "HOME",
        "street": "221 Baker Street",
        "city": "Hyderabad",
        "pincode": "500001",
        "is_default": False
    }
    r = post(f"{base_url}/addresses", headers=valid_headers, json=payload)
    assert r.status_code == 200

def test_post_address_invalid_pincode(base_url, valid_headers):
    payload = {
        "label": "HOME",
        "street": "Valid Street",
        "city": "City",
        "pincode": "50001"
    }
    r = post(f"{base_url}/addresses", headers=valid_headers, json=payload)
    assert r.status_code == 400  # expected per spec (API bug if fails)

def test_post_address_invalid_label(base_url, valid_headers):
    payload = {
        "label": "INVALID",
        "street": "Valid Street",
        "city": "City",
        "pincode": "50001"
    }
    r = post(f"{base_url}/addresses", headers=valid_headers, json=payload)
    assert r.status_code == 400

def test_post_address_missing_fields(base_url, valid_headers):
    payload = {"label": "HOME"}
    r = post(f"{base_url}/addresses", headers=valid_headers, json=payload)
    assert r.status_code == 400

def test_post_address_short_street(base_url, valid_headers):
    payload = {
        "label": "HOME",
        "street": "abc",
        "city": "City",
        "pincode": "50001"
    }
    r = post(f"{base_url}/addresses", headers=valid_headers, json=payload)
    assert r.status_code == 400

def test_post_address_short_city(base_url, valid_headers):
    payload = {
        "label": "HOME",
        "street": "Valid Street",
        "city": "A",
        "pincode": "50001"
    }
    r = post(f"{base_url}/addresses", headers=valid_headers, json=payload)
    assert r.status_code == 400

def test_post_address_pincode_non_numeric(base_url, valid_headers):
    payload = {
        "label": "HOME",
        "street": "Valid Street",
        "city": "City",
        "pincode": "abc123"
    }
    r = post(f"{base_url}/addresses", headers=valid_headers, json=payload)
    assert r.status_code == 400

def test_post_address_street_boundary_min_per_spec(base_url, valid_headers):
    payload = {
        "label": "HOME",
        "street": "12345",
        "city": "City",
        "pincode": "50001"
    }
    r = post(f"{base_url}/addresses", headers=valid_headers, json=payload)
    assert r.status_code == 200

def test_post_address_street_boundary_max_per_spec(base_url, valid_headers):
    payload = {
        "label": "HOME",
        "street": "A" * 100,
        "city": "City",
        "pincode": "50001"
    }
    r = post(f"{base_url}/addresses", headers=valid_headers, json=payload)
    assert r.status_code == 200

# ---------- POST workaround (to enable chaining tests) ----------

def test_post_address_workaround_create(base_url, valid_headers):
    payload = {
        "label": "HOME",
        "street": "Workaround Street",
        "city": "City",
        "pincode": "50001"
    }
    r = post(f"{base_url}/addresses", headers=valid_headers, json=payload)
    assert r.status_code == 200

# ---------- default constraint ----------

def test_post_address_single_default_constraint(base_url, valid_headers):
    payload1 = {
        "label": "HOME",
        "street": "Street 1",
        "city": "City",
        "pincode": "50001",
        "is_default": True
    }
    payload2 = {
        "label": "HOME",
        "street": "Street 2",
        "city": "City",
        "pincode": "50001",
        "is_default": True
    }
    post(f"{base_url}/addresses", headers=valid_headers, json=payload1)
    post(f"{base_url}/addresses", headers=valid_headers, json=payload2)
    r = get(f"{base_url}/addresses", headers=valid_headers)
    data = r.json()
    defaults = [a for a in data if a["is_default"]]
    assert len(defaults) == 1

# ---------- PUT /addresses ----------

def test_put_address_valid(base_url, valid_headers):
    payload = {
        "label": "HOME",
        "street": "Old Street",
        "city": "City",
        "pincode": "50001"
    }
    r = post(f"{base_url}/addresses", headers=valid_headers, json=payload)
    addr_id = r.json()["address"]["address_id"]
    update_payload = {
        "street": "New Street",
        "is_default": True
    }
    r = put(f"{base_url}/addresses/{addr_id}", headers=valid_headers, json=update_payload)
    assert r.status_code == 200
    data = r.json()
    assert data["address"]["street"] == "New Street"
    assert data["address"]["is_default"] is True

def test_put_address_disallowed_fields(base_url, valid_headers):
    payload = {
        "label": "HOME",
        "street": "Street",
        "city": "City",
        "pincode": "50001"
    }
    r = post(f"{base_url}/addresses", headers=valid_headers, json=payload)
    addr_id = r.json()["address"]["address_id"]
    update_payload = {
        "city": "NewCity"
    }
    r = put(f"{base_url}/addresses/{addr_id}", headers=valid_headers, json=update_payload)
    assert r.status_code == 400

# ---------- DELETE /addresses ----------

def test_delete_address_valid(base_url, valid_headers):
    payload = {
        "label": "HOME",
        "street": "Delete Street",
        "city": "City",
        "pincode": "50001"
    }
    r = post(f"{base_url}/addresses", headers=valid_headers, json=payload)
    addr_id = r.json()["address"]["address_id"]
    r = delete(f"{base_url}/addresses/{addr_id}", headers=valid_headers)
    assert r.status_code == 200
    assert "message" in r.json()

def test_delete_address_not_found(base_url, valid_headers):
    r = delete(f"{base_url}/addresses/999999", headers=valid_headers)
    assert r.status_code == 404
