import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app.database import Base
import os

# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def client():
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    # Clean up
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("./test.db"):
        os.remove("./test.db")

def test_create_and_get_vehicle(client):
    payload = {"vin":"TESTVIN123","make":"Toyota","model":"Corolla","year":2020,"owner":"Alice"}
    r = client.post("/vehicles/", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["vin"] == "TESTVIN123"
    assert data["make"] == "Toyota"
    
    # Test getting the vehicle
    vehicle_id = data["id"]
    r2 = client.get(f"/vehicles/{vehicle_id}")
    assert r2.status_code == 200
    data2 = r2.json()
    assert data2["vin"] == "TESTVIN123"

def test_duplicate_vin_error(client):
    payload = {"vin":"DUPLICATE123","make":"Honda","model":"Civic","year":2021,"owner":"Bob"}
    
    # First creation should succeed
    r1 = client.post("/vehicles/", json=payload)
    assert r1.status_code == 200
    
    # Second creation with same VIN should fail
    r2 = client.post("/vehicles/", json=payload)
    assert r2.status_code == 400
    assert "VIN already exists" in r2.json()["detail"]

def test_chat_endpoint(client):
    payload = {"message": "Hello", "use_memory": True}
    r = client.post("/chat", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "response" in data
