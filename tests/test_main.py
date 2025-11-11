"""Tests for main FastAPI application endpoints."""
import pytest
from fastapi import status


class TestRootEndpoint:
    """Tests for root endpoint."""

    def test_read_root(self, client):
        """Test root endpoint returns welcome message."""
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"message": "Welcome to the Product CRUD API"}


class TestHealthEndpoint:
    """Tests for health check endpoint."""

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"status": "healthy"}


class TestProductEndpoints:
    """Tests for product CRUD endpoints."""

    def test_get_all_products_empty(self, client):
        """Test getting all products when database is empty."""
        response = client.get("/products")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_create_product(self, client, sample_product_data):
        """Test creating a new product."""
        response = client.post("/products", json=sample_product_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == sample_product_data["name"]
        assert data["description"] == sample_product_data["description"]
        assert data["price"] == sample_product_data["price"]
        assert data["category"] == sample_product_data["category"]
        assert data["tags"] == sample_product_data["tags"]
        assert data["in_stock"] == sample_product_data["in_stock"]
        assert "created_at" in data

    def test_create_product_minimal(self, client):
        """Test creating a product with minimal required fields."""
        product_data = {
            "name": "Minimal Product",
            "description": "Minimal description",
            "price": 50.0,
            "category": "Category"
        }
        response = client.post("/products", json=product_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == product_data["name"]
        assert data["tags"] == []
        assert data["in_stock"] is True

    def test_get_all_products(self, client, sample_product_data):
        """Test getting all products."""
        # Create multiple products
        client.post("/products", json=sample_product_data)
        product2 = sample_product_data.copy()
        product2["name"] = "Product 2"
        client.post("/products", json=product2)
        
        response = client.get("/products")
        assert response.status_code == status.HTTP_200_OK
        products = response.json()
        assert len(products) == 2
        assert products[0]["name"] == sample_product_data["name"]
        assert products[1]["name"] == "Product 2"

    def test_get_product_by_id(self, client, sample_product_data):
        """Test getting a specific product by ID."""
        create_response = client.post("/products", json=sample_product_data)
        product_id = create_response.json()["id"]
        
        response = client.get(f"/products/{product_id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == product_id
        assert data["name"] == sample_product_data["name"]

    def test_get_product_not_found(self, client):
        """Test getting a product that doesn't exist."""
        response = client.get("/products/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Product not found"

    def test_update_product(self, client, sample_product_data):
        """Test updating an existing product."""
        create_response = client.post("/products", json=sample_product_data)
        product_id = create_response.json()["id"]
        
        update_data = {
            "name": "Updated Product",
            "price": 149.99
        }
        response = client.put(f"/products/{product_id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Updated Product"
        assert data["price"] == 149.99
        # Unchanged fields should remain
        assert data["description"] == sample_product_data["description"]
        assert data["category"] == sample_product_data["category"]

    def test_update_product_partial(self, client, sample_product_data):
        """Test partial update of a product."""
        create_response = client.post("/products", json=sample_product_data)
        product_id = create_response.json()["id"]
        
        update_data = {"in_stock": False}
        response = client.put(f"/products/{product_id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["in_stock"] is False
        assert data["name"] == sample_product_data["name"]

    def test_update_product_not_found(self, client):
        """Test updating a product that doesn't exist."""
        update_data = {"name": "Updated"}
        response = client.put("/products/999", json=update_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Product not found"

    def test_delete_product(self, client, sample_product_data):
        """Test deleting a product."""
        create_response = client.post("/products", json=sample_product_data)
        product_id = create_response.json()["id"]
        
        response = client.delete(f"/products/{product_id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"message": "Product deleted successfully"}
        
        # Verify product is deleted
        get_response = client.get(f"/products/{product_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_product_not_found(self, client):
        """Test deleting a product that doesn't exist."""
        response = client.delete("/products/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Product not found"

    def test_create_product_validation(self, client):
        """Test product creation with invalid data."""
        invalid_data = {
            "name": "Test",
            # Missing required fields
        }
        response = client.post("/products", json=invalid_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_update_product_with_tags(self, client, sample_product_data):
        """Test updating product tags."""
        create_response = client.post("/products", json=sample_product_data)
        product_id = create_response.json()["id"]
        
        update_data = {"tags": ["new", "updated", "tags"]}
        response = client.put(f"/products/{product_id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["tags"] == ["new", "updated", "tags"]


class TestUserEndpoints:
    """Tests for user CRUD endpoints."""

    def test_get_all_users_empty(self, client):
        """Test getting all users when database is empty."""
        response = client.get("/users")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_create_user(self, client, sample_user_data):
        """Test creating a new user."""
        response = client.post("/users", json=sample_user_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == sample_user_data["name"]
        assert data["email"] == sample_user_data["email"]
        assert data["password"] == sample_user_data["password"]
        assert "created_at" in data

    def test_get_all_users(self, client, sample_user_data):
        """Test getting all users."""
        client.post("/users", json=sample_user_data)
        user2 = sample_user_data.copy()
        user2["name"] = "User 2"
        user2["email"] = "user2@example.com"
        client.post("/users", json=user2)
        
        response = client.get("/users")
        assert response.status_code == status.HTTP_200_OK
        users = response.json()
        assert len(users) == 2
        assert users[0]["name"] == sample_user_data["name"]
        assert users[1]["name"] == "User 2"

    def test_get_user_by_id(self, client, sample_user_data):
        """Test getting a specific user by ID."""
        create_response = client.post("/users", json=sample_user_data)
        user_id = create_response.json()["id"]
        
        response = client.get(f"/users/{user_id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == user_id
        assert data["name"] == sample_user_data["name"]
        assert data["email"] == sample_user_data["email"]

    def test_get_user_not_found(self, client):
        """Test getting a user that doesn't exist."""
        response = client.get("/users/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "User not found"

    def test_update_user(self, client, sample_user_data):
        """Test updating an existing user."""
        create_response = client.post("/users", json=sample_user_data)
        user_id = create_response.json()["id"]
        
        update_data = {
            "name": "Updated User",
            "email": "updated@example.com"
        }
        response = client.put(f"/users/{user_id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Updated User"
        assert data["email"] == "updated@example.com"
        # Password should remain unchanged if not updated
        assert data["password"] == sample_user_data["password"]

    def test_update_user_password(self, client, sample_user_data):
        """Test updating user password."""
        create_response = client.post("/users", json=sample_user_data)
        user_id = create_response.json()["id"]
        
        update_data = {"password": "newpassword123"}
        response = client.put(f"/users/{user_id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["password"] == "newpassword123"
        assert data["name"] == sample_user_data["name"]

    def test_update_user_partial(self, client, sample_user_data):
        """Test partial update of a user."""
        create_response = client.post("/users", json=sample_user_data)
        user_id = create_response.json()["id"]
        
        update_data = {"name": "Partially Updated"}
        response = client.put(f"/users/{user_id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Partially Updated"
        assert data["email"] == sample_user_data["email"]

    def test_update_user_not_found(self, client):
        """Test updating a user that doesn't exist."""
        update_data = {"name": "Updated"}
        response = client.put("/users/999", json=update_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "User not found"

    def test_delete_user(self, client, sample_user_data):
        """Test deleting a user."""
        create_response = client.post("/users", json=sample_user_data)
        user_id = create_response.json()["id"]
        
        response = client.delete(f"/users/{user_id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"message": "User deleted successfully"}
        
        # Verify user is deleted
        get_response = client.get(f"/users/{user_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_user_not_found(self, client):
        """Test deleting a user that doesn't exist."""
        response = client.delete("/users/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "User not found"

    def test_create_user_validation(self, client):
        """Test user creation with invalid data."""
        invalid_data = {
            "name": "Test"
            # Missing required fields
        }
        response = client.post("/users", json=invalid_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_user_crud_workflow(self, client, sample_user_data):
        """Test complete CRUD workflow for users."""
        # Create
        create_response = client.post("/users", json=sample_user_data)
        user_id = create_response.json()["id"]
        
        # Read
        get_response = client.get(f"/users/{user_id}")
        assert get_response.status_code == status.HTTP_200_OK
        
        # Update
        update_response = client.put(f"/users/{user_id}", json={"name": "Updated"})
        assert update_response.status_code == status.HTTP_200_OK
        
        # Delete
        delete_response = client.delete(f"/users/{user_id}")
        assert delete_response.status_code == status.HTTP_200_OK

