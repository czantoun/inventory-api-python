import pytest
from fastapi.testclient import TestClient
from main import app, Base, engine, get_db
from sqlalchemy.orm import sessionmaker

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_inventory.db"
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client

def test_create_item(client):
    response = client.post("/items/", json={"name": "Test Item", "description": "Test description", "quantity": 10})
    assert response.status_code == 200
    assert response.json()["message"] == "Item created successfully"

def test_read_items(client):
    response = client.get("/items/")
    assert response.status_code == 200

def test_update_item(client):
    response = client.post("/items/", json={"name": "Test Item", "description": "Test description", "quantity": 10})
    item_id = response.json()["id"]
    update_response = client.put(f"/items/{item_id}", json={"name": "Updated Name"})
    assert update_response.status_code == 200
    assert update_response.json()["message"] == "Item updated successfully"

def test_delete_item(client):
    response = client.post("/items/", json={"name": "Test Item", "description": "Test description", "quantity": 10})
    item_id = response.json()["id"]
    delete_response = client.delete(f"/items/{item_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Item deleted successfully"
