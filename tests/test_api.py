"""
Unit tests for the DevOps Learning API
"""
import pytest
from fastapi.testclient import TestClient
from src.main import app, contacts

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_contacts():
    """Reset contacts before each test"""
    contacts.clear()
    yield
    contacts.clear()


class TestHealthEndpoints:
    """Test health check endpoints"""

    def test_root_endpoint(self):
        """Test the root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "OK"
        assert "version" in data
        assert "environment" in data

    def test_health_check_endpoint(self):
        """Test the health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "environment" in data


class TestContactsEndpoints:
    """Test contact management endpoints"""

    def test_create_contact(self):
        """Test creating a new contact"""
        response = client.post(
            "/contacts",
            params={
                "name": "John Doe",
                "email": "john@example.com",
                "phone": "+1234567890"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "John Doe"
        assert data["email"] == "john@example.com"
        assert "id" in data
        assert "created_at" in data

    def test_create_contact_missing_fields(self):
        """Test creating a contact with missing fields"""
        response = client.post(
            "/contacts",
            params={
                "name": "John Doe",
                "email": "john@example.com"
            }
        )
        assert response.status_code == 422

    def test_list_contacts(self):
        """Test listing all contacts"""
        client.post(
            "/contacts",
            params={
                "name": "Jane Doe",
                "email": "jane@example.com",
                "phone": "+0987654321"
            }
        )

        response = client.get("/contacts")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert len(data["contacts"]) == 1

    def test_get_contact(self):
        """Test getting a specific contact"""
        create_response = client.post(
            "/contacts",
            params={
                "name": "Alice",
                "email": "alice@example.com",
                "phone": "+1111111111"
            }
        )
        contact_id = create_response.json()["id"]

        response = client.get(f"/contacts/{contact_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Alice"

    def test_get_contact_not_found(self):
        """Test getting a contact that doesn't exist"""
        response = client.get("/contacts/999")
        assert response.status_code == 404


class TestInfoEndpoint:
    """Test API info endpoint"""

    def test_get_api_info(self):
        """Test getting API information"""
        response = client.get("/info")
        assert response.status_code == 200
        data = response.json()
        assert "api_name" in data
        assert "api_version" in data
        assert "environment" in data