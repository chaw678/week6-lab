import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


# a. fee comes back as JSON with the right value
def test_fee_value(client):
    # 5 days late, no deluxe: chargeable = 3, fee = 3 * 0.50 = 1.50
    resp = client.get("/fine?days=5")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["fee"] == 1.50
    assert data["days_late"] == 5


# b. deluxe flag reaches the calculation
def test_deluxe_doubles_fee(client):
    # 5 days late, deluxe: fee = 1.50 * 2 = 3.00
    resp = client.get("/fine?days=5&deluxe=1")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["fee"] == 3.00
    assert data["deluxe"] is True


# c. non-numeric days gives 400
def test_non_numeric_days(client):
    resp = client.get("/fine?days=abc")
    assert resp.status_code == 400
    assert "error" in resp.get_json()


# d. negative days gives 400
def test_negative_days(client):
    resp = client.get("/fine?days=-1")
    assert resp.status_code == 400
    assert "error" in resp.get_json()
