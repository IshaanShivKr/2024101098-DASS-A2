from utils import get, post, assert_json

# ---------- GET /products/{product_id}/reviews ----------

def test_get_reviews_valid(base_url, valid_headers):
    r = get(f"{base_url}/products/1/reviews", headers=valid_headers)
    assert r.status_code == 200
    assert_json(r)
    data = r.json()
    assert "average_rating" in data
    assert "reviews" in data
    assert isinstance(data["average_rating"], (int, float))
    assert isinstance(data["reviews"], list)

def test_get_reviews_not_found(base_url, valid_headers):
    r = get(f"{base_url}/products/999999/reviews", headers=valid_headers)
    assert r.status_code in [200, 404]

def test_get_reviews_missing_header(base_url):
    r = get(f"{base_url}/products/1/reviews")
    assert r.status_code == 401

def test_get_reviews_invalid_header(base_url):
    r = get(f"{base_url}/products/1/reviews", headers={"X-Roll-Number": "abc"})
    assert r.status_code == 400

# ---------- POST /products/{product_id}/reviews ----------

def test_post_review_valid(base_url, valid_headers):
    payload = {"rating": 5, "comment": "Great product"}
    r = post(f"{base_url}/products/1/reviews", headers=valid_headers, json=payload)
    assert r.status_code == 200
    assert_json(r)

def test_post_review_invalid_rating_low(base_url, valid_headers):
    payload = {"rating": 0, "comment": "Bad"}
    r = post(f"{base_url}/products/1/reviews", headers=valid_headers, json=payload)
    assert r.status_code == 400

def test_post_review_invalid_rating_high(base_url, valid_headers):
    payload = {"rating": 6, "comment": "Bad"}
    r = post(f"{base_url}/products/1/reviews", headers=valid_headers, json=payload)
    assert r.status_code == 400

def test_post_review_comment_empty(base_url, valid_headers):
    payload = {"rating": 3, "comment": ""}
    r = post(f"{base_url}/products/1/reviews", headers=valid_headers, json=payload)
    assert r.status_code == 400

def test_post_review_comment_too_long(base_url, valid_headers):
    payload = {"rating": 3, "comment": "A" * 201}
    r = post(f"{base_url}/products/1/reviews", headers=valid_headers, json=payload)
    assert r.status_code == 400

def test_post_review_missing_fields(base_url, valid_headers):
    payload = {}
    r = post(f"{base_url}/products/1/reviews", headers=valid_headers, json=payload)
    assert r.status_code == 400

def test_post_review_wrong_type(base_url, valid_headers):
    payload = {"rating": "five", "comment": 123}
    r = post(f"{base_url}/products/1/reviews", headers=valid_headers, json=payload)
    assert r.status_code == 400

def test_post_review_boundary_rating(base_url, valid_headers):
    for rating in [1, 5]:
        payload = {"rating": rating, "comment": "ok"}
        r = post(f"{base_url}/products/1/reviews", headers=valid_headers, json=payload)
        assert r.status_code == 200
