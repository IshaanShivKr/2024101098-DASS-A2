from utils import get, post, assert_json

# ---------- GET /wallet ----------

def test_get_wallet_valid(base_url, valid_headers):
    r = get(f"{base_url}/wallet", headers=valid_headers)
    assert r.status_code == 200
    assert_json(r)
    data = r.json()
    assert isinstance(data["wallet_balance"], (int, float))

def test_get_wallet_missing_header(base_url):
    r = get(f"{base_url}/wallet")
    assert r.status_code == 401

def test_get_wallet_invalid_header(base_url):
    r = get(f"{base_url}/wallet", headers={"X-Roll-Number": "abc"})
    assert r.status_code == 400

# ---------- POST /wallet/add ----------

def test_wallet_add_valid(base_url, valid_headers):
    payload = {"amount": 100}
    r = post(f"{base_url}/wallet/add", headers=valid_headers, json=payload)
    assert r.status_code == 200
    assert_json(r)

def test_wallet_add_zero(base_url, valid_headers):
    payload = {"amount": 0}
    r = post(f"{base_url}/wallet/add", headers=valid_headers, json=payload)
    assert r.status_code == 400

def test_wallet_add_negative(base_url, valid_headers):
    payload = {"amount": -10}
    r = post(f"{base_url}/wallet/add", headers=valid_headers, json=payload)
    assert r.status_code == 400

def test_wallet_add_exceeds_limit(base_url, valid_headers):
    payload = {"amount": 100001}
    r = post(f"{base_url}/wallet/add", headers=valid_headers, json=payload)
    assert r.status_code == 400

def test_wallet_add_missing_field(base_url, valid_headers):
    payload = {}
    r = post(f"{base_url}/wallet/add", headers=valid_headers, json=payload)
    assert r.status_code == 400

def test_wallet_add_wrong_type(base_url, valid_headers):
    payload = {"amount": "abc"}
    r = post(f"{base_url}/wallet/add", headers=valid_headers, json=payload)
    assert r.status_code == 400

# ---------- POST /wallet/pay ----------

def test_wallet_pay_valid(base_url, valid_headers):
    payload = {"amount": 10}
    r = post(f"{base_url}/wallet/pay", headers=valid_headers, json=payload)
    assert r.status_code in [200, 400]
    assert_json(r)

def test_wallet_pay_zero(base_url, valid_headers):
    payload = {"amount": 0}
    r = post(f"{base_url}/wallet/pay", headers=valid_headers, json=payload)
    assert r.status_code == 400

def test_wallet_pay_negative(base_url, valid_headers):
    payload = {"amount": -5}
    r = post(f"{base_url}/wallet/pay", headers=valid_headers, json=payload)
    assert r.status_code == 400

def test_wallet_pay_insufficient_balance(base_url, valid_headers):
    payload = {"amount": 999999}
    r = post(f"{base_url}/wallet/pay", headers=valid_headers, json=payload)
    assert r.status_code == 400

def test_wallet_pay_missing_field(base_url, valid_headers):
    payload = {}
    r = post(f"{base_url}/wallet/pay", headers=valid_headers, json=payload)
    assert r.status_code == 400

def test_wallet_pay_wrong_type(base_url, valid_headers):
    payload = {"amount": "abc"}
    r = post(f"{base_url}/wallet/pay", headers=valid_headers, json=payload)
    assert r.status_code == 400
