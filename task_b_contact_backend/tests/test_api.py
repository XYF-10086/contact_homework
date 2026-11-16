import os
from pathlib import Path
from fastapi.testclient import TestClient

TEST_DB = Path(__file__).resolve().parent / "test_contacts.db"
os.environ["DATABASE_PATH"] = str(TEST_DB)

from app.main import app
from app.database import init_db

def setup_module():
    if TEST_DB.exists():
        TEST_DB.unlink()
    init_db()

def teardown_module():
    if TEST_DB.exists():
        TEST_DB.unlink()

def test_contact_crud_and_multiple_methods():
    with TestClient(app) as client:
        response = client.post("/api/contacts", json={
            "name": "Test User",
            "notes": "testing",
            "methods": [
                {"type": "phone", "value": "123"},
                {"type": "phone", "value": "456"},
                {"type": "email", "value": "test@example.com"}
            ]
        })
        assert response.status_code == 201
        contact = response.json()
        assert len(contact["methods"]) == 3
        contact_id = contact["id"]

        detail = client.get(f"/api/contacts/{contact_id}")
        assert detail.status_code == 200
        assert len(detail.json()["methods"]) == 3

        favorite = client.patch(
            f"/api/contacts/{contact_id}/favorite", params={"favorite": "true"}
        )
        assert favorite.status_code == 200
        assert favorite.json()["is_favorite"] is True

        assert client.get("/api/contacts", params={"favorite": "true"}).status_code == 200
        assert client.delete(f"/api/contacts/{contact_id}").status_code == 200
        assert client.get(f"/api/contacts/{contact_id}").status_code == 404
