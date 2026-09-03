from fastapi.testclient import TestClient
from app.main import app

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


def test_list_cards():
    response = client.get("/api/v1/cards")
    assert response.status_code == 200
    cards = response.json()
    assert isinstance(cards, list)
    assert len(cards) >= 4
    assert cards[0]["store_name"] == "Starbucks"


def test_create_card():
    new_card_payload = {
        "store_name": "Target",
        "card_holder_name": "Alex Morgan",
        "card_number": "1122 3344 5566",
        "category": "Shopping",
        "gradient_colors": ["#CC0000", "#990000"],
        "icon_name": "cart_fill",
        "points": 250,
    }
    response = client.post("/api/v1/cards", json=new_card_payload)
    assert response.status_code == 201
    card = response.json()
    assert card["store_name"] == "Target"
    assert "id" in card
