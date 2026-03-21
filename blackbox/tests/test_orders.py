from utils import get, post, assert_json

# ---------- GET /orders ----------

def test_get_orders_valid(base_url, valid_headers):
    r = get(f"{base_url}/orders", headers=valid_headers)
    assert r.status_code == 200
    assert_json(r)
    data = r.json()
    assert isinstance(data, list)
    for order in data:
        assert isinstance(order["order_id"], int)
        if "user_id" in order:
            assert isinstance(order["user_id"], int)
        assert isinstance(order["total_amount"], (int, float))
        if "gst_amount" in order:
            assert isinstance(order["gst_amount"], (int, float))
        assert isinstance(order["payment_status"], str)
        assert isinstance(order["order_status"], str)

def test_get_orders_missing_header(base_url):
    r = get(f"{base_url}/orders")
    assert r.status_code == 401

def test_get_orders_invalid_header(base_url):
    r = get(f"{base_url}/orders", headers={"X-Roll-Number": "abc"})
    assert r.status_code == 400

# ---------- GET /orders/{order_id} ----------

def test_get_order_valid(base_url, valid_headers):
    r = get(f"{base_url}/orders/1", headers=valid_headers)
    assert r.status_code in [200, 404]
    if r.status_code == 200:
        assert_json(r)
        data = r.json()
        assert isinstance(data["order_id"], int)

def test_get_order_not_found(base_url, valid_headers):
    r = get(f"{base_url}/orders/999999", headers=valid_headers)
    assert r.status_code == 404

def test_get_order_invalid_id(base_url, valid_headers):
    r = get(f"{base_url}/orders/abc", headers=valid_headers)
    assert r.status_code in [400, 404]

def test_get_order_missing_header(base_url):
    r = get(f"{base_url}/orders/1")
    assert r.status_code == 401

# ---------- POST /orders/{order_id}/cancel ----------

def test_cancel_order_valid(base_url, valid_headers):
    r = post(f"{base_url}/orders/1/cancel", headers=valid_headers)
    assert r.status_code in [200, 400, 404]
    assert_json(r)

def test_cancel_order_not_found(base_url, valid_headers):
    r = post(f"{base_url}/orders/999999/cancel", headers=valid_headers)
    assert r.status_code == 404

def test_cancel_order_invalid_id(base_url, valid_headers):
    r = post(f"{base_url}/orders/abc/cancel", headers=valid_headers)
    assert r.status_code in [400, 404]

def test_cancel_order_missing_header(base_url):
    r = post(f"{base_url}/orders/1/cancel")
    assert r.status_code == 401

# ---------- GET /orders/{order_id}/invoice ----------

def test_get_invoice_valid(base_url, valid_headers):
    r = get(f"{base_url}/orders/1/invoice", headers=valid_headers)
    assert r.status_code in [200, 404]
    if r.status_code == 200:
        assert_json(r)
        data = r.json()
        assert isinstance(data["subtotal"], (int, float))
        assert isinstance(data["gst_amount"], (int, float))
        assert isinstance(data["total"], (int, float))
        assert abs(data["subtotal"] + data["gst_amount"] - data["total"]) < 1e-6

def test_get_invoice_not_found(base_url, valid_headers):
    r = get(f"{base_url}/orders/999999/invoice", headers=valid_headers)
    assert r.status_code == 404

def test_get_invoice_invalid_id(base_url, valid_headers):
    r = get(f"{base_url}/orders/abc/invoice", headers=valid_headers)
    assert r.status_code in [400, 404]

def test_get_invoice_missing_header(base_url):
    r = get(f"{base_url}/orders/1/invoice")
    assert r.status_code == 401
