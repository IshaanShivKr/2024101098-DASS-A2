from utils import get


def test_missing_roll_number(base_url):
    r = get(f"{base_url}/products")
    assert r.status_code == 401


def test_invalid_roll_number(base_url):
    headers = {"X-Roll-Number": "abc"}
    r = get(f"{base_url}/products", headers=headers)
    assert r.status_code == 400


def test_missing_user_id(base_url):
    headers = {"X-Roll-Number": "2024101098"}
    r = get(f"{base_url}/profile", headers=headers)
    assert r.status_code == 400
