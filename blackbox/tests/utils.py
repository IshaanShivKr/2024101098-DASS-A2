import requests

def get(url, headers=None, params=None):
    return requests.get(url=url, headers=headers, params=params)

def post(url, headers=None, json=None):
    return requests.post(url, headers=headers, json=json)

def put(url, headers=None, json=None):
    return requests.put(url, headers=headers, json=json)

def delete(url, headers=None):
    return requests.delete(url, headers=headers)


def assert_json(response):
    assert "application/json" in response.headers.get("Content-Type", "")
