from utils import get, post, assert_json

# ---------- GET /loyalty ----------

def test_get_loyalty_valid(base_url, valid_headers):
    r = get(f"{base_url}/loyalty", headers=valid_headers)
    assert r.status_code == 200
    assert_json(r)
    data = r.json()
    assert isinstance(data["loyalty_points"], int)

def test_get_loyalty_missing_header(base_url):
    r = get(f"{base_url}/loyalty")
    assert r.status_code == 401

def test_get_loyalty_invalid_header(base_url):
    r = get(f"{base_url}/loyalty", headers={"X-Roll-Number": "abc"})
    assert r.status_code == 400

# ---------- POST /loyalty/redeem ----------

def test_loyalty_redeem_valid(base_url, valid_headers):
    payload = {"points": 1}
    r = post(f"{base_url}/loyalty/redeem", headers=valid_headers, json=payload)
    assert r.status_code in [200, 400]
    assert_json(r)

def test_loyalty_redeem_zero(base_url, valid_headers):
    payload = {"points": 0}
    r = post(f"{base_url}/loyalty/redeem", headers=valid_headers, json=payload)
    assert r.status_code == 400

def test_loyalty_redeem_negative(base_url, valid_headers):
    payload = {"points": -5}
    r = post(f"{base_url}/loyalty/redeem", headers=valid_headers, json=payload)
    assert r.status_code == 400

def test_loyalty_redeem_insufficient_points(base_url, valid_headers):
    payload = {"points": 999999}
    r = post(f"{base_url}/loyalty/redeem", headers=valid_headers, json=payload)
    assert r.status_code == 400

def test_loyalty_redeem_missing_field(base_url, valid_headers):
    payload = {}
    r = post(f"{base_url}/loyalty/redeem", headers=valid_headers, json=payload)
    assert r.status_code == 400

def test_loyalty_redeem_wrong_type(base_url, valid_headers):
    payload = {"points": "abc"}
    r = post(f"{base_url}/loyalty/redeem", headers=valid_headers, json=payload)
    assert r.status_code == 400
