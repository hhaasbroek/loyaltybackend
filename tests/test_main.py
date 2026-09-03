from fastapi.testclient import TestClient
from app.core.auth import get_current_user
from app.main import app
from app.models.user import UserDB
from tests.conftest import FAKE_UID, _fake_current_user

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["docs"] == "/docs"
    assert data["health"] == "/api/v1/health"


def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "Loyalty Backend"
    assert "timestamp" in data


NEW_CARD_PAYLOAD = {
    "store_name": "Target",
    "card_holder_name": "Alex Morgan",
    "card_number": "1122 3344 5566",
    "category": "Shopping",
    "gradient_colors": ["#CC0000", "#990000"],
    "icon_name": "cart_fill",
    "points": 250,
}


def test_create_card():
    response = client.post("/api/v1/cards", json=NEW_CARD_PAYLOAD)
    assert response.status_code == 201
    card = response.json()
    assert card["store_name"] == "Target"
    assert "id" in card


def test_list_cards():
    created = client.post("/api/v1/cards", json=NEW_CARD_PAYLOAD).json()

    response = client.get("/api/v1/cards")
    assert response.status_code == 200
    cards = response.json()
    assert isinstance(cards, list)
    assert any(c["id"] == created["id"] for c in cards)


def test_cards_require_auth():
    app.dependency_overrides.pop(get_current_user, None)
    try:
        response = client.get("/api/v1/cards")
        assert response.status_code == 401
    finally:
        app.dependency_overrides[get_current_user] = _fake_current_user


def test_cards_are_scoped_to_user():
    created = client.post("/api/v1/cards", json=NEW_CARD_PAYLOAD).json()

    def _other_user() -> UserDB:
        return UserDB(id="other-uid", email="other@example.com", display_name="Other")

    app.dependency_overrides[get_current_user] = _other_user
    try:
        response = client.get(f"/api/v1/cards/{created['id']}")
        assert response.status_code == 404
    finally:
        app.dependency_overrides[get_current_user] = _fake_current_user
