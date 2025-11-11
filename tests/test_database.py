"""Tests for database operations."""
import pytest
from datetime import datetime

from database import InMemoryDatabase
from models import ProductCreate, ProductUpdate, UserCreate, UserUpdate


class TestInMemoryDatabase:
    """Tests for InMemoryDatabase class."""

    @pytest.fixture
    def db(self):
        """Create a fresh database instance."""
        db = InMemoryDatabase()
        db.products.clear()
        db.users.clear()
        db.next_id = 1
        db.next_user_id = 1
        return db

    class TestProductOperations:
        """Tests for product database operations."""

        def test_create_product(self, db):
            """Test creating a product."""
            product_data = ProductCreate(
                name="Test Product",
                description="Test Description",
                price=99.99,
                category="Test Category",
                tags=["test"],
                in_stock=True
            )
            product = db.create_product(product_data)
            assert product.id == 1
            assert product.name == "Test Product"
            assert product.description == "Test Description"
            assert product.price == 99.99
            assert product.category == "Test Category"
            assert product.tags == ["test"]
            assert product.in_stock is True
            assert isinstance(product.created_at, datetime)
            assert len(db.products) == 1

        def test_create_product_auto_increment_id(self, db):
            """Test that product IDs auto-increment."""
            product_data = ProductCreate(
                name="Product 1",
                description="Desc",
                price=10.0,
                category="Cat"
            )
            product1 = db.create_product(product_data)
            assert product1.id == 1
            
            product2 = db.create_product(product_data)
            assert product2.id == 2
            assert len(db.products) == 2

        def test_get_all_products(self, db):
            """Test getting all products."""
            assert db.get_all_products() == []
            
            product_data = ProductCreate(
                name="Product 1",
                description="Desc",
                price=10.0,
                category="Cat"
            )
            db.create_product(product_data)
            db.create_product(product_data)
            
            products = db.get_all_products()
            assert len(products) == 2

        def test_get_product_by_id(self, db):
            """Test getting a product by ID."""
            product_data = ProductCreate(
                name="Test Product",
                description="Desc",
                price=10.0,
                category="Cat"
            )
            created_product = db.create_product(product_data)
            
            found_product = db.get_product(created_product.id)
            assert found_product is not None
            assert found_product.id == created_product.id
            assert found_product.name == "Test Product"

        def test_get_product_not_found(self, db):
            """Test getting a product that doesn't exist."""
            product = db.get_product(999)
            assert product is None

        def test_update_product(self, db):
            """Test updating a product."""
            product_data = ProductCreate(
                name="Original Name",
                description="Original Desc",
                price=10.0,
                category="Original Cat",
                tags=["tag1"],
                in_stock=True
            )
            created_product = db.create_product(product_data)
            
            update_data = ProductUpdate(
                name="Updated Name",
                price=20.0,
                in_stock=False
            )
            updated_product = db.update_product(created_product.id, update_data)
            
            assert updated_product is not None
            assert updated_product.name == "Updated Name"
            assert updated_product.price == 20.0
            assert updated_product.in_stock is False
            # Unchanged fields should remain
            assert updated_product.description == "Original Desc"
            assert updated_product.category == "Original Cat"
            assert updated_product.tags == ["tag1"]

        def test_update_product_tags(self, db):
            """Test updating product tags."""
            product_data = ProductCreate(
                name="Product",
                description="Desc",
                price=10.0,
                category="Cat",
                tags=["old"]
            )
            created_product = db.create_product(product_data)
            
            update_data = ProductUpdate(tags=["new", "tags"])
            updated_product = db.update_product(created_product.id, update_data)
            
            assert updated_product.tags == ["new", "tags"]

        def test_update_product_not_found(self, db):
            """Test updating a product that doesn't exist."""
            update_data = ProductUpdate(name="Updated")
            result = db.update_product(999, update_data)
            assert result is None

        def test_delete_product(self, db):
            """Test deleting a product."""
            product_data = ProductCreate(
                name="Product",
                description="Desc",
                price=10.0,
                category="Cat"
            )
            created_product = db.create_product(product_data)
            assert len(db.products) == 1
            
            result = db.delete_product(created_product.id)
            assert result is True
            assert len(db.products) == 0
            assert db.get_product(created_product.id) is None

        def test_delete_product_not_found(self, db):
            """Test deleting a product that doesn't exist."""
            result = db.delete_product(999)
            assert result is False

        def test_delete_product_maintains_other_products(self, db):
            """Test that deleting one product doesn't affect others."""
            product_data = ProductCreate(
                name="Product",
                description="Desc",
                price=10.0,
                category="Cat"
            )
            product1 = db.create_product(product_data)
            product2 = db.create_product(product_data)
            product3 = db.create_product(product_data)
            
            db.delete_product(product2.id)
            
            assert len(db.products) == 2
            assert db.get_product(product1.id) is not None
            assert db.get_product(product2.id) is None
            assert db.get_product(product3.id) is not None

    class TestUserOperations:
        """Tests for user database operations."""

        def test_create_user(self, db):
            """Test creating a user."""
            user_data = UserCreate(
                name="Test User",
                email="test@example.com",
                password="password123"
            )
            user = db.create_user(user_data)
            assert user.id == 1
            assert user.name == "Test User"
            assert user.email == "test@example.com"
            assert user.password == "password123"
            assert isinstance(user.created_at, datetime)
            assert len(db.users) == 1

        def test_create_user_auto_increment_id(self, db):
            """Test that user IDs auto-increment."""
            user_data = UserCreate(
                name="User 1",
                email="user1@example.com",
                password="pass"
            )
            user1 = db.create_user(user_data)
            assert user1.id == 1
            
            user2_data = UserCreate(
                name="User 2",
                email="user2@example.com",
                password="pass"
            )
            user2 = db.create_user(user2_data)
            assert user2.id == 2
            assert len(db.users) == 2

        def test_get_all_users(self, db):
            """Test getting all users."""
            assert db.get_all_users() == []
            
            user_data = UserCreate(
                name="User 1",
                email="user1@example.com",
                password="pass"
            )
            db.create_user(user_data)
            db.create_user(user_data)
            
            users = db.get_all_users()
            assert len(users) == 2

        def test_get_user_by_id(self, db):
            """Test getting a user by ID."""
            user_data = UserCreate(
                name="Test User",
                email="test@example.com",
                password="pass"
            )
            created_user = db.create_user(user_data)
            
            found_user = db.get_user(created_user.id)
            assert found_user is not None
            assert found_user.id == created_user.id
            assert found_user.name == "Test User"
            assert found_user.email == "test@example.com"

        def test_get_user_not_found(self, db):
            """Test getting a user that doesn't exist."""
            user = db.get_user(999)
            assert user is None

        def test_update_user(self, db):
            """Test updating a user."""
            user_data = UserCreate(
                name="Original Name",
                email="original@example.com",
                password="originalpass"
            )
            created_user = db.create_user(user_data)
            
            update_data = UserUpdate(
                name="Updated Name",
                email="updated@example.com"
            )
            updated_user = db.update_user(created_user.id, update_data)
            
            assert updated_user is not None
            assert updated_user.name == "Updated Name"
            assert updated_user.email == "updated@example.com"
            # Password should remain unchanged if not updated
            assert updated_user.password == "originalpass"

        def test_update_user_password(self, db):
            """Test updating user password."""
            user_data = UserCreate(
                name="User",
                email="user@example.com",
                password="oldpass"
            )
            created_user = db.create_user(user_data)
            
            update_data = UserUpdate(password="newpass")
            updated_user = db.update_user(created_user.id, update_data)
            
            assert updated_user.password == "newpass"
            assert updated_user.name == "User"

        def test_update_user_partial(self, db):
            """Test partial update of a user."""
            user_data = UserCreate(
                name="Original",
                email="original@example.com",
                password="pass"
            )
            created_user = db.create_user(user_data)
            
            update_data = UserUpdate(name="Updated")
            updated_user = db.update_user(created_user.id, update_data)
            
            assert updated_user.name == "Updated"
            assert updated_user.email == "original@example.com"
            assert updated_user.password == "pass"

        def test_update_user_not_found(self, db):
            """Test updating a user that doesn't exist."""
            update_data = UserUpdate(name="Updated")
            result = db.update_user(999, update_data)
            assert result is None

        def test_delete_user(self, db):
            """Test deleting a user."""
            user_data = UserCreate(
                name="User",
                email="user@example.com",
                password="pass"
            )
            created_user = db.create_user(user_data)
            assert len(db.users) == 1
            
            result = db.delete_user(created_user.id)
            assert result is True
            assert len(db.users) == 0
            assert db.get_user(created_user.id) is None

        def test_delete_user_not_found(self, db):
            """Test deleting a user that doesn't exist."""
            result = db.delete_user(999)
            assert result is False

        def test_delete_user_maintains_other_users(self, db):
            """Test that deleting one user doesn't affect others."""
            user1_data = UserCreate(
                name="User 1",
                email="user1@example.com",
                password="pass"
            )
            user2_data = UserCreate(
                name="User 2",
                email="user2@example.com",
                password="pass"
            )
            user3_data = UserCreate(
                name="User 3",
                email="user3@example.com",
                password="pass"
            )
            user1 = db.create_user(user1_data)
            user2 = db.create_user(user2_data)
            user3 = db.create_user(user3_data)
            
            db.delete_user(user2.id)
            
            assert len(db.users) == 2
            assert db.get_user(user1.id) is not None
            assert db.get_user(user2.id) is None
            assert db.get_user(user3.id) is not None

    class TestDatabaseIsolation:
        """Tests for database isolation and state management."""

        def test_products_and_users_independent(self, db):
            """Test that products and users are independent."""
            product_data = ProductCreate(
                name="Product",
                description="Desc",
                price=10.0,
                category="Cat"
            )
            user_data = UserCreate(
                name="User",
                email="user@example.com",
                password="pass"
            )
            
            product = db.create_product(product_data)
            user = db.create_user(user_data)
            
            assert product.id == 1
            assert user.id == 1
            assert len(db.products) == 1
            assert len(db.users) == 1
            
            # IDs should be independent
            product2 = db.create_product(product_data)
            user2 = db.create_user(user_data)
            
            assert product2.id == 2
            assert user2.id == 2

