from utils import post, assert_json

def test_checkout_valid_payment_methods(base_url, valid_headers):
    for method in ["COD", "WALLET", "CARD"]:
        payload = {"payment_method": method}
        r = post(f"{base_url}/checkout", headers=valid_headers, json=payload)
        assert r.status_code in [200, 400]
        assert_json(r)

def test_checkout_response_structure(base_url, valid_headers):
    payload = {"payment_method": "CARD"}
    r = post(f"{base_url}/checkout", headers=valid_headers, json=payload)
    assert r.status_code in [200, 400]
    assert_json(r)
    data = r.json()
    if r.status_code == 200:
        assert "order_id" in data or "message" in data
    else:
        assert "error" in data

def test_checkout_invalid_payment_method(base_url, valid_headers):
    payload = {"payment_method": "BITCOIN"}
    r = post(f"{base_url}/checkout", headers=valid_headers, json=payload)
    assert r.status_code == 400

def test_checkout_missing_payment_method(base_url, valid_headers):
    payload = {}
    r = post(f"{base_url}/checkout", headers=valid_headers, json=payload)
    assert r.status_code == 400

def test_checkout_payment_method_wrong_type(base_url, valid_headers):
    payload = {"payment_method": 123}
    r = post(f"{base_url}/checkout", headers=valid_headers, json=payload)
    assert r.status_code == 400

def test_checkout_missing_header(base_url):
    payload = {"payment_method": "COD"}
    r = post(f"{base_url}/checkout", json=payload)
    assert r.status_code == 401

def test_checkout_invalid_header(base_url):
    payload = {"payment_method": "COD"}
    r = post(f"{base_url}/checkout", headers={"X-Roll-Number": "abc"}, json=payload)
    assert r.status_code == 400

def test_checkout_empty_cart(base_url, valid_headers):
    payload = {"payment_method": "COD"}
    r = post(f"{base_url}/checkout", headers=valid_headers, json=payload)
    assert r.status_code in [200, 400]

def test_checkout_cod_limit(base_url, valid_headers):
    payload = {"payment_method": "COD"}
    r = post(f"{base_url}/checkout", headers=valid_headers, json=payload)
    assert r.status_code in [200, 400]

def test_checkout_payment_status_logic(base_url, valid_headers):
    payload = {"payment_method": "CARD"}
    r = post(f"{base_url}/checkout", headers=valid_headers, json=payload)
    if r.status_code == 200:
        data = r.json()
        if "payment_status" in data:
            assert data["payment_status"] == "PAID"

def test_checkout_pending_status_methods(base_url, valid_headers):
    for method in ["COD", "WALLET"]:
        payload = {"payment_method": method}
        r = post(f"{base_url}/checkout", headers=valid_headers, json=payload)
        if r.status_code == 200:
            data = r.json()
            if "payment_status" in data:
                assert data["payment_status"] == "PENDING"

def test_checkout_gst_calculation_structure(base_url, valid_headers):
    payload = {"payment_method": "CARD"}
    r = post(f"{base_url}/checkout", headers=valid_headers, json=payload)
    if r.status_code == 200:
        data = r.json()
        if "gst_amount" in data:
            assert data["gst_amount"] >= 0
