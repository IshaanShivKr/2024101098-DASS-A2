from utils import get, assert_json


# ---------- helpers ----------

def assert_list_response(r):
    assert r.status_code == 200
    assert_json(r)
    data = r.json()
    assert isinstance(data, list)
    return data

def assert_object_response(r):
    assert r.status_code == 200
    assert_json(r)
    data = r.json()
    assert isinstance(data, dict)
    return data

# ---------- /admin/users ----------

def test_admin_users_valid(base_url, admin_headers):
    r = get(f"{base_url}/admin/users", headers=admin_headers)
    data = assert_list_response(r)

    for user in data:
        assert isinstance(user["user_id"], int)
        assert isinstance(user["name"], str)
        assert isinstance(user["email"], str)
        assert isinstance(user["phone"], str)
        assert isinstance(user["wallet_balance"], (int, float))
        assert isinstance(user["loyalty_points"], int)

        assert len(user["phone"]) == 10
        assert user["phone"].isdigit()

def test_admin_users_missing_header(base_url):
    r = get(f"{base_url}/admin/users")
    assert r.status_code == 401

def test_admin_users_invalid_header(base_url):
    r = get(f"{base_url}/admin/users", headers={"X-Roll-Number": "abc"})
    assert r.status_code == 400

# ---------- /admin/users/{user_id} ----------

def test_admin_user_valid(base_url, admin_headers):
    r = get(f"{base_url}/admin/users/1", headers=admin_headers)

    assert r.status_code in [200, 404]

    if r.status_code == 200:
        data = assert_object_response(r)

        assert isinstance(data["user_id"], int)
        assert isinstance(data["name"], str)
        assert isinstance(data["email"], str)
        assert isinstance(data["phone"], str)
        assert isinstance(data["wallet_balance"], (int, float))
        assert isinstance(data["loyalty_points"], int)

        assert len(data["phone"]) == 10
        assert data["phone"].isdigit()

def test_admin_user_not_found(base_url, admin_headers):
    r = get(f"{base_url}/admin/users/999999", headers=admin_headers)
    assert r.status_code == 404

def test_admin_user_invalid_type(base_url, admin_headers):
    r = get(f"{base_url}/admin/users/abc", headers=admin_headers)
    assert r.status_code in [400, 404]

def test_admin_user_boundary_zero(base_url, admin_headers):
    r = get(f"{base_url}/admin/users/0", headers=admin_headers)
    assert r.status_code in [400, 404]

def test_admin_user_boundary_negative(base_url, admin_headers):
    r = get(f"{base_url}/admin/users/-1", headers=admin_headers)
    assert r.status_code in [400, 404]

def test_admin_user_missing_header(base_url):
    r = get(f"{base_url}/admin/users/1")
    assert r.status_code == 401

def test_admin_user_invalid_header(base_url):
    r = get(f"{base_url}/admin/users/1", headers={"X-Roll-Number": "abc"})
    assert r.status_code == 400

# ---------- /admin/carts ----------

def test_admin_carts_valid(base_url, admin_headers):
    r = get(f"{base_url}/admin/carts", headers=admin_headers)
    data = assert_list_response(r)

    for cart in data:
        assert isinstance(cart["cart_id"], int)
        assert isinstance(cart["user_id"], int)
        assert isinstance(cart["items"], list)

        total = 0

        for item in cart["items"]:
            assert isinstance(item["product_id"], int)
            assert isinstance(item["name"], str)
            assert isinstance(item["quantity"], int)
            assert isinstance(item["unit_price"], (int, float))
            assert isinstance(item["subtotal"], (int, float))

            assert item["quantity"] >= 0

            expected = item["quantity"] * item["unit_price"]
            assert abs(item["subtotal"] - expected) < 1e-6

            total += expected

        assert abs(cart["total"] - total) < 1e-6

def test_admin_carts_missing_header(base_url):
    r = get(f"{base_url}/admin/carts")
    assert r.status_code == 401

def test_admin_carts_invalid_header(base_url):
    r = get(f"{base_url}/admin/carts", headers={"X-Roll-Number": "abc"})
    assert r.status_code == 400

# ---------- /admin/orders ----------

def test_admin_orders_valid(base_url, admin_headers):
    r = get(f"{base_url}/admin/orders", headers=admin_headers)
    data = assert_list_response(r)

    for order in data:
        assert isinstance(order["order_id"], int)
        assert isinstance(order["user_id"], int)
        assert isinstance(order["total_amount"], (int, float))
        assert isinstance(order["gst_amount"], (int, float))

        assert order["payment_method"] in ["COD", "WALLET", "CARD"]
        assert order["payment_status"] in ["PENDING", "PAID"]
        assert isinstance(order["order_status"], str)

def test_admin_orders_missing_header(base_url):
    r = get(f"{base_url}/admin/orders")
    assert r.status_code == 401

def test_admin_orders_invalid_header(base_url):
    r = get(f"{base_url}/admin/orders", headers={"X-Roll-Number": "abc"})
    assert r.status_code == 400

# ---------- /admin/products ----------

def test_admin_products_valid(base_url, admin_headers):
    r = get(f"{base_url}/admin/products", headers=admin_headers)
    data = assert_list_response(r)

    for product in data:
        assert isinstance(product["product_id"], int)
        assert isinstance(product["name"], str)
        assert isinstance(product["category"], str)
        assert isinstance(product["price"], (int, float))
        assert isinstance(product["stock_quantity"], int)
        assert isinstance(product["is_active"], bool)

def test_admin_products_missing_header(base_url):
    r = get(f"{base_url}/admin/products")
    assert r.status_code == 401

def test_admin_products_invalid_header(base_url):
    r = get(f"{base_url}/admin/products", headers={"X-Roll-Number": "abc"})
    assert r.status_code == 400

# ---------- /admin/coupons ----------

def test_admin_coupons_valid(base_url, admin_headers):
    r = get(f"{base_url}/admin/coupons", headers=admin_headers)
    data = assert_list_response(r)

    for coupon in data:
        assert isinstance(coupon["coupon_code"], str)
        assert coupon["discount_type"] in ["PERCENT", "FIXED"]
        assert isinstance(coupon["discount_value"], (int, float))
        assert isinstance(coupon["min_cart_value"], (int, float))
        assert isinstance(coupon["max_discount"], (int, float))
        assert isinstance(coupon["expiry_date"], str)
        assert isinstance(coupon["is_active"], bool)

def test_admin_coupons_missing_header(base_url):
    r = get(f"{base_url}/admin/coupons")
    assert r.status_code == 401

def test_admin_coupons_invalid_header(base_url):
    r = get(f"{base_url}/admin/coupons", headers={"X-Roll-Number": "abc"})
    assert r.status_code == 400

# ---------- /admin/tickets ----------

def test_admin_tickets_valid(base_url, admin_headers):
    r = get(f"{base_url}/admin/tickets", headers=admin_headers)
    data = assert_list_response(r)

    for ticket in data:
        assert isinstance(ticket["ticket_id"], int)
        assert isinstance(ticket["user_id"], int)
        assert isinstance(ticket["subject"], str)
        assert isinstance(ticket["message"], str)

        assert ticket["status"] in ["OPEN", "IN_PROGRESS", "CLOSED"]

def test_admin_tickets_missing_header(base_url):
    r = get(f"{base_url}/admin/tickets")
    assert r.status_code == 401

def test_admin_tickets_invalid_header(base_url):
    r = get(f"{base_url}/admin/tickets", headers={"X-Roll-Number": "abc"})
    assert r.status_code == 400

# ---------- /admin/addresses ----------

def test_admin_addresses_valid(base_url, admin_headers):
    r = get(f"{base_url}/admin/addresses", headers=admin_headers)
    data = assert_list_response(r)

    for address in data:
        assert isinstance(address["address_id"], int)
        assert isinstance(address["user_id"], int)

        assert address["label"] in ["HOME", "OFFICE", "OTHER"]

        assert isinstance(address["street"], str)
        assert 5 <= len(address["street"]) <= 100

        assert isinstance(address["city"], str)
        assert 2 <= len(address["city"]) <= 50

        assert isinstance(address["pincode"], str)
        assert address["pincode"].isdigit()
        assert len(address["pincode"]) == 6

        assert isinstance(address["is_default"], bool)

def test_admin_addresses_missing_header(base_url):
    r = get(f"{base_url}/admin/addresses")
    assert r.status_code == 401

def test_admin_addresses_invalid_header(base_url):
    r = get(f"{base_url}/admin/addresses", headers={"X-Roll-Number": "abc"})
    assert r.status_code == 400
