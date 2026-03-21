from utils import post, assert_json

# ---------- APPLY COUPON ----------

def test_apply_coupon_valid_format(base_url, valid_headers):
    payload = {"coupon_code": "BONUS75"}
    r = post(f"{base_url}/coupon/apply", headers=valid_headers, json=payload)
    assert r.status_code in [200, 400]
    assert_json(r)

def test_apply_coupon_missing_field(base_url, valid_headers):
    payload = {}
    r = post(f"{base_url}/coupon/apply", headers=valid_headers, json=payload)
    assert r.status_code == 400

def test_apply_coupon_wrong_type(base_url, valid_headers):
    payload = {"coupon_code": 12345}
    r = post(f"{base_url}/coupon/apply", headers=valid_headers, json=payload)
    assert r.status_code == 400

def test_apply_coupon_invalid_code(base_url, valid_headers):
    payload = {"coupon_code": "INVALIDCODE"}
    r = post(f"{base_url}/coupon/apply", headers=valid_headers, json=payload)
    assert r.status_code in [400, 404]

def test_apply_coupon_expired(base_url, valid_headers):
    payload = {"coupon_code": "BIGDEAL500"}
    r = post(f"{base_url}/coupon/apply", headers=valid_headers, json=payload)
    assert r.status_code == 400

def test_apply_coupon_min_cart_value_not_met(base_url, valid_headers):
    payload = {"coupon_code": "BONUS75"}
    r = post(f"{base_url}/coupon/apply", headers=valid_headers, json=payload)
    assert r.status_code in [200, 400]

def test_apply_coupon_response_structure(base_url, valid_headers):
    payload = {"coupon_code": "BONUS75"}
    r = post(f"{base_url}/coupon/apply", headers=valid_headers, json=payload)

    assert r.status_code in [200, 400]
    assert_json(r)

    data = r.json()

    if r.status_code == 200:
        assert "message" in data
    else:
        assert "error" in data

def test_apply_coupon_discount_non_negative(base_url, valid_headers):
    payload = {"coupon_code": "BONUS75"}
    r = post(f"{base_url}/coupon/apply", headers=valid_headers, json=payload)
    if r.status_code == 200:
        data = r.json()
        if "discount" in data:
            assert data["discount"] >= 0

# ---------- REMOVE COUPON ----------

def test_remove_coupon_valid(base_url, valid_headers):
    r = post(f"{base_url}/coupon/remove", headers=valid_headers)
    assert r.status_code in [200, 400]
    assert_json(r)

def test_remove_coupon_without_applying(base_url, valid_headers):
    r = post(f"{base_url}/coupon/remove", headers=valid_headers)
    assert r.status_code in [200, 400]

def test_remove_coupon_missing_header(base_url):
    r = post(f"{base_url}/coupon/remove")
    assert r.status_code == 401

def test_apply_coupon_missing_header(base_url):
    payload = {"coupon_code": "BONUS75"}
    r = post(f"{base_url}/coupon/apply", json=payload)
    assert r.status_code == 401

def test_apply_coupon_invalid_header(base_url):
    payload = {"coupon_code": "BONUS75"}
    r = post(f"{base_url}/coupon/apply", headers={"X-Roll-Number": "abc"}, json=payload)
    assert r.status_code == 400
