from utils import get, post, delete, assert_json

# ---------- GET /cart ----------

def test_get_cart_valid(base_url, valid_headers):
    r = get(f"{base_url}/cart", headers=valid_headers)
    assert r.status_code == 200
    assert_json(r)
    data = r.json()
    assert isinstance(data, dict)
    if "items" in data:
        total = 0
        for item in data["items"]:
            assert isinstance(item["product_id"], int)
            assert isinstance(item["quantity"], int)
            assert isinstance(item["unit_price"], (int, float))
            assert isinstance(item["subtotal"], (int, float))
            expected = item["quantity"] * item["unit_price"]
            assert abs(item["subtotal"] - expected) < 1e-6
            total += expected
        if "total" in data:
            assert abs(data["total"] - total) < 1e-6

def test_get_cart_missing_header(base_url):
    r = get(f"{base_url}/cart")
    assert r.status_code == 401

def test_get_cart_invalid_header(base_url):
    r = get(f"{base_url}/cart", headers={"X-Roll-Number": "abc"})
    assert r.status_code == 400

# ---------- POST /cart/add ----------

def test_cart_add_valid(base_url, valid_headers):
    payload = {"product_id": 1, "quantity": 1}
    r = post(f"{base_url}/cart/add", headers=valid_headers, json=payload)
    assert r.status_code in [200, 400]
    assert_json(r)

def test_cart_add_invalid_quantity_zero(base_url, valid_headers):
    payload = {"product_id": 1, "quantity": 0}
    r = post(f"{base_url}/cart/add", headers=valid_headers, json=payload)
    assert r.status_code == 400

def test_cart_add_invalid_quantity_negative(base_url, valid_headers):
    payload = {"product_id": 1, "quantity": -1}
    r = post(f"{base_url}/cart/add", headers=valid_headers, json=payload)
    assert r.status_code == 400

def test_cart_add_product_not_found(base_url, valid_headers):
    payload = {"product_id": 999999, "quantity": 1}
    r = post(f"{base_url}/cart/add", headers=valid_headers, json=payload)
    assert r.status_code == 404

def test_cart_add_missing_fields(base_url, valid_headers):
    payload = {}
    r = post(f"{base_url}/cart/add", headers=valid_headers, json=payload)
    assert r.status_code == 400

def test_cart_add_wrong_type(base_url, valid_headers):
    payload = {"product_id": "one", "quantity": "two"}
    r = post(f"{base_url}/cart/add", headers=valid_headers, json=payload)
    assert r.status_code == 400

# ---------- POST /cart/update ----------

def test_cart_update_valid(base_url, valid_headers):
    payload = {"product_id": 1, "quantity": 2}
    r = post(f"{base_url}/cart/update", headers=valid_headers, json=payload)
    assert r.status_code in [200, 400]
    assert_json(r)

def test_cart_update_invalid_quantity(base_url, valid_headers):
    payload = {"product_id": 1, "quantity": 0}
    r = post(f"{base_url}/cart/update", headers=valid_headers, json=payload)
    assert r.status_code == 400

def test_cart_update_missing_fields(base_url, valid_headers):
    payload = {}
    r = post(f"{base_url}/cart/update", headers=valid_headers, json=payload)
    assert r.status_code == 400

# ---------- POST /cart/remove ----------

def test_cart_remove_valid(base_url, valid_headers):
    payload = {"product_id": 1}
    r = post(f"{base_url}/cart/remove", headers=valid_headers, json=payload)
    assert r.status_code in [200, 404]
    assert_json(r)

def test_cart_remove_not_found(base_url, valid_headers):
    payload = {"product_id": 999999}
    r = post(f"{base_url}/cart/remove", headers=valid_headers, json=payload)
    assert r.status_code == 404

def test_cart_remove_missing_field(base_url, valid_headers):
    payload = {}
    r = post(f"{base_url}/cart/remove", headers=valid_headers, json=payload)
    assert r.status_code == 400

# ---------- DELETE /cart/clear ----------

def test_cart_clear_valid(base_url, valid_headers):
    r = delete(f"{base_url}/cart/clear", headers=valid_headers)
    assert r.status_code == 200
    assert_json(r)

def test_cart_clear_missing_header(base_url):
    r = delete(f"{base_url}/cart/clear")
    assert r.status_code == 401

def test_cart_clear_invalid_header(base_url):
    r = delete(f"{base_url}/cart/clear", headers={"X-Roll-Number": "abc"})
    assert r.status_code == 400
