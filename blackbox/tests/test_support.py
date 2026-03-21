from utils import get, post, put, assert_json

# ---------- POST /support/ticket ----------

def test_create_ticket_valid(base_url, valid_headers):
    payload = {
        "subject": "Order issue",
        "message": "The delivered item was damaged"
    }
    r = post(f"{base_url}/support/ticket", headers=valid_headers, json=payload)
    assert r.status_code == 200
    assert_json(r)
    data = r.json()
    assert "ticket" in data or "message" in data

def test_create_ticket_subject_too_short(base_url, valid_headers):
    payload = {
        "subject": "Hey",
        "message": "Valid message"
    }
    r = post(f"{base_url}/support/ticket", headers=valid_headers, json=payload)
    assert r.status_code == 400

def test_create_ticket_subject_too_long(base_url, valid_headers):
    payload = {
        "subject": "A" * 101,
        "message": "Valid message"
    }
    r = post(f"{base_url}/support/ticket", headers=valid_headers, json=payload)
    assert r.status_code == 400

def test_create_ticket_message_empty(base_url, valid_headers):
    payload = {
        "subject": "Order issue",
        "message": ""
    }
    r = post(f"{base_url}/support/ticket", headers=valid_headers, json=payload)
    assert r.status_code == 400

def test_create_ticket_message_too_long(base_url, valid_headers):
    payload = {
        "subject": "Order issue",
        "message": "A" * 501
    }
    r = post(f"{base_url}/support/ticket", headers=valid_headers, json=payload)
    assert r.status_code == 400

def test_create_ticket_missing_fields(base_url, valid_headers):
    payload = {}
    r = post(f"{base_url}/support/ticket", headers=valid_headers, json=payload)
    assert r.status_code == 400

def test_create_ticket_wrong_type(base_url, valid_headers):
    payload = {
        "subject": 12345,
        "message": 67890
    }
    r = post(f"{base_url}/support/ticket", headers=valid_headers, json=payload)
    assert r.status_code == 400

def test_create_ticket_subject_boundary_min(base_url, valid_headers):
    payload = {
        "subject": "A" * 5,
        "message": "Valid"
    }
    r = post(f"{base_url}/support/ticket", headers=valid_headers, json=payload)
    assert r.status_code == 200

def test_create_ticket_subject_boundary_max(base_url, valid_headers):
    payload = {
        "subject": "A" * 100,
        "message": "Valid"
    }
    r = post(f"{base_url}/support/ticket", headers=valid_headers, json=payload)
    assert r.status_code == 200

def test_create_ticket_message_boundary_min(base_url, valid_headers):
    payload = {
        "subject": "Order issue",
        "message": "A"
    }
    r = post(f"{base_url}/support/ticket", headers=valid_headers, json=payload)
    assert r.status_code == 200

def test_create_ticket_message_boundary_max(base_url, valid_headers):
    payload = {
        "subject": "Order issue",
        "message": "A" * 500
    }
    r = post(f"{base_url}/support/ticket", headers=valid_headers, json=payload)
    assert r.status_code == 200

# ---------- GET /support/tickets ----------

def test_get_tickets_valid(base_url, valid_headers):
    r = get(f"{base_url}/support/tickets", headers=valid_headers)
    assert r.status_code == 200
    assert_json(r)
    data = r.json()
    assert isinstance(data, list)
    for ticket in data:
        assert isinstance(ticket["ticket_id"], int)
        assert ticket["status"] in ["OPEN", "IN_PROGRESS", "CLOSED"]
        assert isinstance(ticket["subject"], str)
        assert isinstance(ticket["message"], str)

def test_get_tickets_missing_header(base_url):
    r = get(f"{base_url}/support/tickets")
    assert r.status_code == 401

def test_get_tickets_invalid_header(base_url):
    r = get(f"{base_url}/support/tickets", headers={"X-Roll-Number": "abc"})
    assert r.status_code == 400

# ---------- PUT /support/tickets/{ticket_id} ----------

def test_update_ticket_valid_transition_open_to_in_progress(base_url, valid_headers):
    create_payload = {
        "subject": "Track order",
        "message": "Please check this order"
    }
    r = post(f"{base_url}/support/ticket", headers=valid_headers, json=create_payload)
    ticket_id = r.json()["ticket"]["ticket_id"]
    update_payload = {"status": "IN_PROGRESS"}
    r = put(f"{base_url}/support/tickets/{ticket_id}", headers=valid_headers, json=update_payload)
    assert r.status_code == 200
    assert_json(r)

def test_update_ticket_invalid_transition_open_to_closed(base_url, valid_headers):
    create_payload = {
        "subject": "Track order",
        "message": "Please check this order"
    }
    r = post(f"{base_url}/support/ticket", headers=valid_headers, json=create_payload)
    ticket_id = r.json()["ticket"]["ticket_id"]
    update_payload = {"status": "CLOSED"}
    r = put(f"{base_url}/support/tickets/{ticket_id}", headers=valid_headers, json=update_payload)
    assert r.status_code == 400

def test_update_ticket_invalid_status_value(base_url, valid_headers):
    create_payload = {
        "subject": "Track order",
        "message": "Please check this order"
    }
    r = post(f"{base_url}/support/ticket", headers=valid_headers, json=create_payload)
    ticket_id = r.json()["ticket"]["ticket_id"]
    update_payload = {"status": "INVALID"}
    r = put(f"{base_url}/support/tickets/{ticket_id}", headers=valid_headers, json=update_payload)
    assert r.status_code == 400

def test_update_ticket_missing_field(base_url, valid_headers):
    create_payload = {
        "subject": "Track order",
        "message": "Please check this order"
    }
    r = post(f"{base_url}/support/ticket", headers=valid_headers, json=create_payload)
    ticket_id = r.json()["ticket"]["ticket_id"]
    update_payload = {}
    r = put(f"{base_url}/support/tickets/{ticket_id}", headers=valid_headers, json=update_payload)
    assert r.status_code == 400

def test_update_ticket_wrong_type(base_url, valid_headers):
    create_payload = {
        "subject": "Track order",
        "message": "Please check this order"
    }
    r = post(f"{base_url}/support/ticket", headers=valid_headers, json=create_payload)
    ticket_id = r.json()["ticket"]["ticket_id"]
    update_payload = {"status": 123}
    r = put(f"{base_url}/support/tickets/{ticket_id}", headers=valid_headers, json=update_payload)
    assert r.status_code == 400

def test_update_ticket_not_found(base_url, valid_headers):
    update_payload = {"status": "IN_PROGRESS"}
    r = put(f"{base_url}/support/tickets/999999", headers=valid_headers, json=update_payload)
    assert r.status_code in [400, 404]
