"""
MongoDB Data Models and Schemas
Production-ready data models with validation and type hints
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass

from .utils import (
    sanitize_user_data,
    sanitize_product_data,
    ValidationError,
)

# ======================================================
# User Model
# ======================================================

@dataclass
class UserModel:
    email: str
    name: str
    picture: Optional[str] = None
    role: str = "buyer"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def validate(self) -> None:
        if not self.email or "@" not in self.email:
            raise ValidationError("Valid email is required")

        if not self.name or len(self.name.strip()) < 2:
            raise ValidationError("Name must be at least 2 characters")

        if self.role not in {"buyer", "seller", "admin"}:
            raise ValidationError("Invalid role")

    def to_dict(self) -> Dict[str, Any]:
        self.validate()

        now = datetime.utcnow()

        data = {
            "email": self.email.lower().strip(),
            "name": self.name.strip(),
            "picture": self.picture,
            "role": self.role,
            "created_at": self.created_at or now,
            "updated_at": self.updated_at or now,
        }

        return sanitize_user_data(data)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserModel":
        return cls(
            email=data.get("email", ""),
            name=data.get("name", ""),
            picture=data.get("picture"),
            role=data.get("role", "buyer"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )


# ======================================================
# Product Model
# ======================================================

@dataclass
class ProductModel:
    name: str
    description: str
    price: float
    stock: int
    seller_id: str
    category: Optional[str] = None
    images: Optional[List[str]] = None
    status: str = "active"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def validate(self) -> None:
        if not self.name or len(self.name.strip()) < 3:
            raise ValidationError("Product name must be at least 3 characters")

        if not self.description or len(self.description.strip()) < 10:
            raise ValidationError("Description must be at least 10 characters")

        if self.price <= 0:
            raise ValidationError("Price must be greater than 0")

        if self.stock < 0:
            raise ValidationError("Stock cannot be negative")

        if not self.seller_id:
            raise ValidationError("Seller ID is required")

        if self.status not in {"active", "inactive", "deleted"}:
            raise ValidationError("Invalid product status")

    def to_dict(self) -> Dict[str, Any]:
        self.validate()

        now = datetime.utcnow()

        data = {
            "name": self.name.strip(),
            "description": self.description.strip(),
            "price": float(self.price),
            "stock": int(self.stock),
            "seller_id": self.seller_id,
            "category": self.category,
            "images": self.images or [],
            "status": self.status,
            "created_at": self.created_at or now,
            "updated_at": self.updated_at or now,
        }

        return sanitize_product_data(data)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProductModel":
        return cls(
            name=data.get("name", ""),
            description=data.get("description", ""),
            price=float(data.get("price", 0)),
            stock=int(data.get("stock", 0)),
            seller_id=data.get("seller_id", ""),
            category=data.get("category"),
            images=data.get("images", []),
            status=data.get("status", "active"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )


# ======================================================
# Order Model
# ======================================================

@dataclass
class OrderModel:
    user_id: str
    product_ids: List[str]
    total_amount: float
    status: str = "pending"
    seller_id: Optional[str] = None
    shipping_address: Optional[Dict[str, Any]] = None
    payment_status: str = "pending"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def validate(self) -> None:
        if not self.user_id:
            raise ValidationError("User ID is required")

        if not self.product_ids:
            raise ValidationError("At least one product is required")

        if self.total_amount <= 0:
            raise ValidationError("Total amount must be greater than 0")

        if self.status not in {
            "pending",
            "confirmed",
            "shipped",
            "delivered",
            "cancelled",
        }:
            raise ValidationError("Invalid order status")

        if self.payment_status not in {
            "pending",
            "paid",
            "failed",
            "refunded",
        }:
            raise ValidationError("Invalid payment status")

    def to_dict(self) -> Dict[str, Any]:
        self.validate()

        now = datetime.utcnow()

        return {
            "user_id": self.user_id,
            "product_ids": self.product_ids,
            "total_amount": float(self.total_amount),
            "status": self.status,
            "seller_id": self.seller_id,
            "shipping_address": self.shipping_address,
            "payment_status": self.payment_status,
            "created_at": self.created_at or now,
            "updated_at": self.updated_at or now,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OrderModel":
        return cls(
            user_id=data.get("user_id", ""),
            product_ids=data.get("product_ids", []),
            total_amount=float(data.get("total_amount", 0)),
            status=data.get("status", "pending"),
            seller_id=data.get("seller_id"),
            shipping_address=data.get("shipping_address"),
            payment_status=data.get("payment_status", "pending"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )


# ======================================================
# Schema Reference (Documentation + Validation)
# ======================================================

DATABASE_SCHEMAS = {
    "users": {
        "_id": "ObjectId",
        "email": "string (unique)",
        "name": "string",
        "picture": "string (optional)",
        "role": "buyer | seller | admin",
        "created_at": "datetime",
        "updated_at": "datetime",
    },
    "products": {
        "_id": "ObjectId",
        "name": "string",
        "description": "string",
        "price": "number",
        "stock": "integer",
        "seller_id": "ObjectId",
        "category": "string",
        "images": "array",
        "status": "active | inactive | deleted",
        "created_at": "datetime",
        "updated_at": "datetime",
    },
    "orders": {
        "_id": "ObjectId",
        "user_id": "ObjectId",
        "product_ids": "array",
        "total_amount": "number",
        "status": "pending | confirmed | shipped | delivered | cancelled",
        "payment_status": "pending | paid | failed | refunded",
        "created_at": "datetime",
        "updated_at": "datetime",
    },
}


def get_collection_schema(name: str) -> Optional[Dict[str, str]]:
    return DATABASE_SCHEMAS.get(name)


def validate_document_schema(collection: str, document: Dict[str, Any]) -> bool:
    schema = get_collection_schema(collection)
    if not schema:
        return True

    required = {
        "users": {"email", "name"},
        "products": {"name", "description", "price", "stock", "seller_id"},
        "orders": {"user_id", "product_ids", "total_amount"},
    }.get(collection, set())

    for field in required:
        if field not in document:
            raise ValidationError(
                f"Required field '{field}' missing from {collection}"
            )

    return True
