from utils import get, assert_json


# ---------- /admin/users ----------

def test_admin_users_valid(base_url, admin_headers):
    r = get(f"{base_url}/admin/users", headers=admin_headers)

    assert r.status_code == 200
    assert_json(r)

    data = r.json()
    assert isinstance(data, list)

    for user in data:
        assert "wallet_balance" in user
        assert "loyalty_points" in user


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
        assert_json(r)
        data = r.json()
        assert "user_id" in data


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

    assert r.status_code == 200
    assert_json(r)
    assert isinstance(r.json(), list)


def test_admin_carts_missing_header(base_url):
    r = get(f"{base_url}/admin/carts")
    assert r.status_code == 401


def test_admin_carts_invalid_header(base_url):
    r = get(f"{base_url}/admin/carts", headers={"X-Roll-Number": "abc"})
    assert r.status_code == 400


# ---------- /admin/orders ----------

def test_admin_orders_valid(base_url, admin_headers):
    r = get(f"{base_url}/admin/orders", headers=admin_headers)

    assert r.status_code == 200
    assert_json(r)

    data = r.json()
    assert isinstance(data, list)

    for order in data:
        assert "payment_status" in order
        assert "order_status" in order


def test_admin_orders_missing_header(base_url):
    r = get(f"{base_url}/admin/orders")
    assert r.status_code == 401


def test_admin_orders_invalid_header(base_url):
    r = get(f"{base_url}/admin/orders", headers={"X-Roll-Number": "abc"})
    assert r.status_code == 400


# ---------- /admin/products ----------

def test_admin_products_valid(base_url, admin_headers):
    r = get(f"{base_url}/admin/products", headers=admin_headers)

    assert r.status_code == 200
    assert_json(r)
    assert isinstance(r.json(), list)


def test_admin_products_missing_header(base_url):
    r = get(f"{base_url}/admin/products")
    assert r.status_code == 401


def test_admin_products_invalid_header(base_url):
    r = get(f"{base_url}/admin/products", headers={"X-Roll-Number": "abc"})
    assert r.status_code == 400


# ---------- /admin/coupons ----------

def test_admin_coupons_valid(base_url, admin_headers):
    r = get(f"{base_url}/admin/coupons", headers=admin_headers)

    assert r.status_code == 200
    assert_json(r)
    assert isinstance(r.json(), list)


def test_admin_coupons_missing_header(base_url):
    r = get(f"{base_url}/admin/coupons")
    assert r.status_code == 401


def test_admin_coupons_invalid_header(base_url):
    r = get(f"{base_url}/admin/coupons", headers={"X-Roll-Number": "abc"})
    assert r.status_code == 400


# ---------- /admin/tickets ----------

def test_admin_tickets_valid(base_url, admin_headers):
    r = get(f"{base_url}/admin/tickets", headers=admin_headers)

    assert r.status_code == 200
    assert_json(r)
    assert isinstance(r.json(), list)


def test_admin_tickets_missing_header(base_url):
    r = get(f"{base_url}/admin/tickets")
    assert r.status_code == 401


def test_admin_tickets_invalid_header(base_url):
    r = get(f"{base_url}/admin/tickets", headers={"X-Roll-Number": "abc"})
    assert r.status_code == 400


# ---------- /admin/addresses ----------

def test_admin_addresses_valid(base_url, admin_headers):
    r = get(f"{base_url}/admin/addresses", headers=admin_headers)

    assert r.status_code == 200
    assert_json(r)
    assert isinstance(r.json(), list)


def test_admin_addresses_missing_header(base_url):
    r = get(f"{base_url}/admin/addresses")
    assert r.status_code == 401


def test_admin_addresses_invalid_header(base_url):
    r = get(f"{base_url}/admin/addresses", headers={"X-Roll-Number": "abc"})
    assert r.status_code == 400
