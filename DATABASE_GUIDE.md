# MongoDB Database Layer Guide

## 📁 **Final Database Folder Structure**

```
apps/db/
├── __init__.py                    # Package initialization with exports
├── mongo/
│   ├── __init__.py                # MongoDB module exports
│   ├── connection.py              # Singleton MongoDB connection
│   ├── collections.py             # Collection classes with CRUD operations
│   ├── models.py                 # Data models and validation
│   ├── utils.py                  # Utility functions and helpers
│   ├── client.py                 # DEPRECATED (backward compatibility)
│   ├── db_collections.py         # DEPRECATED (backward compatibility)
│   └── test_mongo.py            # DEPRECATED (backward compatibility)
└── tests/
    ├── __init__.py                # Test package init
    └── test_connection.py        # Comprehensive database tests
```

## 🔗 **Database Connection**

### Singleton Pattern Implementation
```python
from apps.db import mongo_connection

# Check connection
if mongo_connection.is_connected():
    print("✅ MongoDB is connected")

# Get database instance
db = mongo_connection.get_database()

# Close connection (cleanup)
mongo_connection.close_connection()
```

### Environment Variables Required
```env
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/dbname
MONGO_DB_NAME=nirmatriDB  # Optional (defaults to nirmatriDB)
```

## 📊 **Collection Usage Examples**

### Users Collection
```python
from apps.db import users_collection, UserModel, validate_object_id

# Create user
user_data = {
    "email": "user@example.com",
    "name": "John Doe",
    "role": "buyer"
}
user_id = users_collection.create_user(user_data)

# Find user by email
user = users_collection.find_by_email("user@example.com")

# Find user by ID
if validate_object_id(user_id):
    user = users_collection.find_by_id(user_id)

# Update user
success = users_collection.update_user(user_id, {"name": "Jane Doe"})

# Delete user
success = users_collection.delete_one({"_id": user_id})
```

### Products Collection
```python
from apps.db import products_collection, ProductModel

# Create product
product_data = ProductModel(
    name="Product Name",
    description="Product description",
    price=99.99,
    stock=50,
    seller_id="seller_id_here"
)
product_id = products_collection.create_product(product_data.to_dict())

# Find products by seller
seller_products = products_collection.find_by_seller("seller_id_here")

# Search products
search_results = products_collection.search_products("search query")

# Update product
success = products_collection.update_product(product_id, {"price": 149.99})

# Delete product
success = products_collection.delete_product(product_id)
```

### Orders Collection
```python
from apps.db import orders_collection, OrderModel

# Create order
order_data = OrderModel(
    user_id="user_id_here",
    product_ids=["product1", "product2"],
    total_amount=299.99,
    seller_id="seller_id_here"
)
order_id = orders_collection.create_order(order_data.to_dict())

# Find orders by user
user_orders = orders_collection.find_by_user("user_id_here")

# Find orders by seller
seller_orders = orders_collection.find_by_seller("seller_id_here")

# Update order status
success = orders_collection.update_order_status(order_id, "confirmed")
```

## 🛠️ **Utility Functions**

### ObjectId Serialization
```python
from apps.db import serialize_doc, serialize_docs, validate_object_id

# Serialize single document
doc = {"_id": ObjectId("507f1f77bcf86cd799439011"), "name": "Test"}
serialized = serialize_doc(doc)
# Result: {"_id": "507f1f77bcf86cd799439011", "name": "Test"}

# Serialize list of documents
docs = [{"_id": ObjectId("..."), "name": "Test1"}, {"_id": ObjectId("..."), "name": "Test2"}]
serialized = serialize_docs(docs)

# Validate ObjectId
is_valid = validate_object_id("507f1f77bcf86cd799439011")  # True
is_invalid = validate_object_id("invalid_id")  # False
```

### Data Sanitization
```python
from apps.db import sanitize_user_data, sanitize_product_data

# Sanitize user data
raw_user_data = {
    "email": "USER@EXAMPLE.COM  ",
    "name": "John Doe",
    "password": "secret123"  # Will be removed
}
clean_data = sanitize_user_data(raw_user_data)
# Result: {"email": "user@example.com", "name": "John Doe"}

# Sanitize product data
raw_product_data = {
    "name": "Product Name  ",
    "price": "99.99",  # Will be converted to float
    "stock": "50"      # Will be converted to int
}
clean_data = sanitize_product_data(raw_product_data)
```

### Pagination
```python
from apps.db import paginate_query

# Apply pagination to cursor
cursor = products_collection.collection.find({})
documents, page_info = paginate_query(cursor, page=1, per_page=20)

# page_info contains:
# {
#     "page": 1,
#     "per_page": 20,
#     "total": 100,
#     "pages": 5,
#     "has_next": True,
#     "has_prev": False
# }
```

## 🏗️ **Data Models**

### User Model
```python
from apps.db import UserModel

# Create user model
user = UserModel(
    email="user@example.com",
    name="John Doe",
    role="buyer"
)

# Validate data
user.validate()  # Raises ValidationError if invalid

# Convert to dictionary for database
user_dict = user.to_dict()

# Create from database document
user_from_db = UserModel.from_dict(database_document)
```

### Product Model
```python
from apps.db import ProductModel

product = ProductModel(
    name="Product Name",
    description="Description",
    price=99.99,
    stock=50,
    seller_id="seller_id"
)

product.validate()  # Validates required fields and data types
product_dict = product.to_dict()
```

### Order Model
```python
from apps.db import OrderModel

order = OrderModel(
    user_id="user_id",
    product_ids=["product1", "product2"],
    total_amount=299.99,
    seller_id="seller_id"
)

order.validate()  # Validates order structure
order_dict = order.to_dict()
```

## 🧪 **Database Testing**

### Run All Tests
```bash
cd apps/db/tests
python test_connection.py
```

### Individual Test Functions
```python
from apps.db.tests.test_connection import (
    test_connection,
    test_user_operations,
    test_product_operations,
    test_order_operations
)

# Run specific test
test_connection()
test_user_operations()
```

## 📝 **How Data is Stored**

### User Registration Data Storage
```python
# When user registers via Google OAuth:
user_data = {
    "email": "user@gmail.com",  # Converted to lowercase
    "name": "User Name",        # Trimmed
    "picture": "https://...",    # Profile picture URL
    "role": "buyer",           # Default role
    "created_at": datetime.utcnow(),
    "updated_at": datetime.utcnow()
}

# Stored in MongoDB users collection:
{
    "_id": ObjectId("..."),
    "email": "user@gmail.com",
    "name": "User Name",
    "picture": "https://...",
    "role": "buyer",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
}
```

### Login Verification from Database
```python
# Google OAuth flow:
1. User provides Google token
2. Token is verified (existing logic)
3. Email extracted from token
4. Database queried: users_collection.find_by_email(email)
5. If user exists → Login successful
6. If not exists → Create new user with Google data
7. Session created with user ID
```

### Seller Product Data Storage
```python
# When seller uploads product:
product_data = {
    "name": "Handmade Basket",
    "description": "Beautiful handmade basket",
    "price": 500.0,           # Converted to float
    "stock": 10,               # Converted to int
    "seller_id": "seller_id",   # References users collection
    "category": "crafts",       # Optional category
    "images": ["url1", "url2"], # Array of image URLs
    "status": "active",         # Product status
    "created_at": datetime.utcnow(),
    "updated_at": datetime.utcnow()
}

# Stored with automatic indexing on:
# - seller_id (for seller product queries)
# - created_at (for sorting)
# - price (for range queries)
# - text index on name, description (for search)
```

## 🔄 **Django Integration**

### Update Existing Views
```python
# Before (Django ORM):
from django.http import JsonResponse
from .models import User

@csrf_exempt
def google_login(request):
    # ... token verification ...
    user, _ = User.objects.get_or_create(...)
    return JsonResponse({"message": "Login successful"})

# After (MongoDB):
from apps.db import users_collection, serialize_doc
from apps.users.mongo_services import UserService

@csrf_exempt
def google_login(request):
    # ... token verification ...
    result = UserService.create_user({
        "email": data["email"],
        "name": data["name"],
        "picture": data.get("picture", ""),
        "role": "buyer"
    })
    
    if result["success"]:
        request.session["user_id"] = result["user"]["_id"]
        return JsonResponse({"message": "Login successful"})
    else:
        return JsonResponse({"error": result["error"]}, status=400)
```

### Django Shell Usage
```bash
python manage.py shell
```

```python
# Import database modules
from apps.db import users_collection, products_collection, serialize_doc

# Test database operations
user = users_collection.find_by_email("test@example.com")
products = products_collection.search_products("handmade")

print(f"Found user: {user}")
print(f"Found {len(products)} products")
```

## 🚀 **Production Features**

### Connection Pooling
- **Max Pool Size**: 50 connections
- **Min Pool Size**: 5 connections
- **Idle Timeout**: 30 seconds
- **Retry Writes**: Enabled
- **Write Concern**: Majority

### Indexing Strategy
```python
# Users Collection:
- email (unique)
- created_at

# Products Collection:
- seller_id
- created_at
- price (ascending)
- text index on name, description

# Orders Collection:
- user_id
- seller_id
- created_at
- status
```

### Error Handling
```python
from apps.db import DatabaseError, ValidationError

try:
    user_id = users_collection.create_user(user_data)
except ValidationError as e:
    print(f"Validation error: {e}")
except DatabaseError as e:
    print(f"Database error: {e}")
```

### Logging
```python
from apps.db import log_database_operation

# All operations are automatically logged
log_database_operation(
    operation="insert",
    collection="users",
    details={"user_id": user_id, "email": "user@example.com"}
)
```

## 📋 **Migration from Old System**

### Backward Compatibility
All old imports continue to work with deprecation warnings:

```python
# These still work but show warnings:
from apps.db.mongo.client import db, client
from apps.db.mongo.db_collections import users_collection
from apps.db.mongo.utils import serialize_doc
```

### Recommended New Imports
```python
# Use these instead:
from apps.db import db, client, users_collection, serialize_doc
```

## 🔧 **Configuration**

### Environment Setup
```env
# Required
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/dbname

# Optional
MONGO_DB_NAME=nirmatriDB
```

### Django Settings Integration
```python
# settings.py
import os
from apps.db import mongo_connection

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.dummy',
    }
}

# Initialize MongoDB connection
MONGO_URI = os.getenv('MONGO_URI')
if not MONGO_URI:
    raise ValueError("MONGO_URI environment variable is required")
```

---

This database layer is now **production-ready** with proper error handling, logging, indexing, and comprehensive testing! 🎉
