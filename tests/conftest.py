"""Pytest configuration and fixtures."""
import pytest
from fastapi.testclient import TestClient

from database import InMemoryDatabase


@pytest.fixture
def test_db():
    """Create a fresh database instance for each test."""
    db = InMemoryDatabase()
    # Clear sample data that was initialized
    db.products.clear()
    db.users.clear()
    # Reset IDs to start from 1
    db.next_id = 1
    db.next_user_id = 1
    return db


@pytest.fixture
def client(test_db, monkeypatch):
    """Create a test client with a fresh database instance."""
    # Import here to ensure monkeypatch happens before app uses db
    import database
    import main
    
    # Replace the global db instance with our test instance
    monkeypatch.setattr(database, "db", test_db)
    # Also update main's reference if it exists
    if hasattr(main, 'db'):
        monkeypatch.setattr(main, "db", test_db)
    
    from main import app
    return TestClient(app)


@pytest.fixture
def sample_product_data():
    """Sample product data for testing."""
    return {
        "name": "Test Product",
        "description": "Test Description",
        "price": 99.99,
        "category": "Test Category",
        "tags": ["test", "sample"],
        "in_stock": True
    }


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpassword123"
    }

