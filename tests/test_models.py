"""Tests for Pydantic models."""
import pytest
from datetime import datetime
from pydantic import ValidationError

from models import (
    Product, ProductCreate, ProductUpdate,
    User, UserCreate, UserUpdate
)


class TestProductModels:
    """Tests for Product models."""

    def test_product_create_minimal(self):
        """Test creating ProductCreate with minimal required fields."""
        product = ProductCreate(
            name="Test Product",
            description="Test Description",
            price=99.99,
            category="Test Category"
        )
        assert product.name == "Test Product"
        assert product.description == "Test Description"
        assert product.price == 99.99
        assert product.category == "Test Category"
        assert product.tags == []
        assert product.in_stock is True

    def test_product_create_with_all_fields(self):
        """Test creating ProductCreate with all fields."""
        product = ProductCreate(
            name="Test Product",
            description="Test Description",
            price=99.99,
            category="Test Category",
            tags=["tag1", "tag2"],
            in_stock=False
        )
        assert product.tags == ["tag1", "tag2"]
        assert product.in_stock is False

    def test_product_create_validation_missing_required(self):
        """Test ProductCreate validation with missing required fields."""
        with pytest.raises(ValidationError):
            ProductCreate(
                name="Test"
                # Missing required fields
            )

    def test_product_model(self):
        """Test Product model with all fields."""
        product = Product(
            id=1,
            name="Test Product",
            description="Test Description",
            price=99.99,
            category="Test Category",
            tags=["tag1"],
            in_stock=True,
            created_at=datetime.now()
        )
        assert product.id == 1
        assert product.name == "Test Product"
        assert isinstance(product.created_at, datetime)

    def test_product_update_all_fields(self):
        """Test ProductUpdate with all fields."""
        update = ProductUpdate(
            name="Updated",
            description="Updated Desc",
            price=149.99,
            category="Updated Cat",
            tags=["new"],
            in_stock=False
        )
        assert update.name == "Updated"
        assert update.description == "Updated Desc"
        assert update.price == 149.99
        assert update.category == "Updated Cat"
        assert update.tags == ["new"]
        assert update.in_stock is False

    def test_product_update_partial(self):
        """Test ProductUpdate with partial fields."""
        update = ProductUpdate(name="Updated")
        assert update.name == "Updated"
        assert update.description is None
        assert update.price is None

    def test_product_update_empty(self):
        """Test ProductUpdate with no fields."""
        update = ProductUpdate()
        assert update.name is None
        assert update.description is None
        assert update.price is None

    def test_product_update_dict_exclude_unset(self):
        """Test ProductUpdate dict with exclude_unset."""
        update = ProductUpdate(name="Updated")
        update_dict = update.model_dump(exclude_unset=True)
        assert "name" in update_dict
        assert "description" not in update_dict
        assert update_dict["name"] == "Updated"


class TestUserModels:
    """Tests for User models."""

    def test_user_create(self):
        """Test creating UserCreate with all required fields."""
        user = UserCreate(
            name="Test User",
            email="test@example.com",
            password="password123"
        )
        assert user.name == "Test User"
        assert user.email == "test@example.com"
        assert user.password == "password123"

    def test_user_create_validation_missing_required(self):
        """Test UserCreate validation with missing required fields."""
        with pytest.raises(ValidationError):
            UserCreate(
                name="Test"
                # Missing required fields
            )

    def test_user_model(self):
        """Test User model with all fields."""
        user = User(
            id=1,
            name="Test User",
            email="test@example.com",
            password="password123",
            created_at=datetime.now()
        )
        assert user.id == 1
        assert user.name == "Test User"
        assert user.email == "test@example.com"
        assert user.password == "password123"
        assert isinstance(user.created_at, datetime)

    def test_user_update_all_fields(self):
        """Test UserUpdate with all fields."""
        update = UserUpdate(
            name="Updated",
            email="updated@example.com",
            password="newpass"
        )
        assert update.name == "Updated"
        assert update.email == "updated@example.com"
        assert update.password == "newpass"

    def test_user_update_partial(self):
        """Test UserUpdate with partial fields."""
        update = UserUpdate(name="Updated")
        assert update.name == "Updated"
        assert update.email is None
        assert update.password is None

    def test_user_update_empty(self):
        """Test UserUpdate with no fields."""
        update = UserUpdate()
        assert update.name is None
        assert update.email is None
        assert update.password is None

    def test_user_update_dict_exclude_unset(self):
        """Test UserUpdate dict with exclude_unset."""
        update = UserUpdate(email="updated@example.com")
        update_dict = update.model_dump(exclude_unset=True)
        assert "email" in update_dict
        assert "name" not in update_dict
        assert update_dict["email"] == "updated@example.com"


class TestModelSerialization:
    """Tests for model serialization."""

    def test_product_serialization(self):
        """Test Product model serialization."""
        product = Product(
            id=1,
            name="Test",
            description="Desc",
            price=10.0,
            category="Cat",
            created_at=datetime.now()
        )
        product_dict = product.model_dump()
        assert product_dict["id"] == 1
        assert product_dict["name"] == "Test"
        assert "created_at" in product_dict

    def test_user_serialization(self):
        """Test User model serialization."""
        user = User(
            id=1,
            name="Test",
            email="test@example.com",
            password="pass",
            created_at=datetime.now()
        )
        user_dict = user.model_dump()
        assert user_dict["id"] == 1
        assert user_dict["name"] == "Test"
        assert user_dict["email"] == "test@example.com"
        assert "created_at" in user_dict

