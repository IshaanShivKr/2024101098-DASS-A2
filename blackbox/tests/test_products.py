from utils import get, assert_json

# ---------- GET /products ----------

def test_get_products_valid(base_url, valid_headers):
    r = get(f"{base_url}/products", headers=valid_headers)
    assert r.status_code == 200
    assert_json(r)
    data = r.json()
    assert isinstance(data, list)
    for p in data:
        assert isinstance(p["product_id"], int)
        assert isinstance(p["name"], str)
        assert isinstance(p["category"], str)
        assert isinstance(p["price"], (int, float))
        assert isinstance(p["stock_quantity"], int)
        assert isinstance(p["is_active"], bool)
        assert p["is_active"] is True  # only active products allowed

def test_get_products_missing_header(base_url):
    r = get(f"{base_url}/products")
    assert r.status_code == 401

def test_get_products_invalid_header(base_url):
    r = get(f"{base_url}/products", headers={"X-Roll-Number": "abc"})
    assert r.status_code == 400

def test_get_products_filter_category(base_url, valid_headers):
    r = get(f"{base_url}/products?category=Fruits", headers=valid_headers)
    assert r.status_code == 200
    data = r.json()
    for p in data:
        assert p["category"] == "Fruits"

def test_get_products_invalid_category(base_url, valid_headers):
    r = get(f"{base_url}/products?category=INVALID", headers=valid_headers)
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)

def test_get_products_search(base_url, valid_headers):
    r = get(f"{base_url}/products?search=Apple", headers=valid_headers)
    assert r.status_code == 200
    data = r.json()
    for p in data:
        assert "apple" in p["name"].lower()

def test_get_products_sort_price_asc(base_url, valid_headers):
    r = get(f"{base_url}/products?sort=price_asc", headers=valid_headers)
    assert r.status_code == 200
    data = r.json()
    prices = [p["price"] for p in data]
    assert prices == sorted(prices)

def test_get_products_sort_price_desc(base_url, valid_headers):
    r = get(f"{base_url}/products?sort=price_desc", headers=valid_headers)
    assert r.status_code == 200
    data = r.json()
    prices = [p["price"] for p in data]
    assert prices == sorted(prices, reverse=True)

# ---------- GET /products/{id} ----------

def test_get_product_valid(base_url, valid_headers):
    r = get(f"{base_url}/products/1", headers=valid_headers)
    assert r.status_code in [200, 404]
    if r.status_code == 200:
        assert_json(r)
        data = r.json()
        assert isinstance(data["product_id"], int)
        assert isinstance(data["name"], str)
        assert isinstance(data["category"], str)
        assert isinstance(data["price"], (int, float))
        assert isinstance(data["stock_quantity"], int)
        assert isinstance(data["is_active"], bool)

def test_get_product_missing_header(base_url):
    r = get(f"{base_url}/products/1")
    assert r.status_code == 401

def test_get_product_missing_header(base_url):
    r = get(f"{base_url}/products/1")
    assert r.status_code == 401

def test_get_product_not_found(base_url, valid_headers):
    r = get(f"{base_url}/products/999999", headers=valid_headers)
    assert r.status_code == 404

def test_get_product_invalid_id_type(base_url, valid_headers):
    r = get(f"{base_url}/products/abc", headers=valid_headers)
    assert r.status_code in [400, 404]

def test_get_product_boundary_zero(base_url, valid_headers):
    r = get(f"{base_url}/products/0", headers=valid_headers)
    assert r.status_code in [400, 404]

def test_get_product_boundary_negative(base_url, valid_headers):
    r = get(f"{base_url}/products/-1", headers=valid_headers)
    assert r.status_code in [400, 404]
