"""
MongoDB Utility Functions
Shared helpers for validation, serialization, pagination and logging
"""

from typing import Dict, Any, List, Optional
from bson import ObjectId
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# ======================================================
# Custom Exceptions
# ======================================================

class DatabaseError(Exception):
    """Base database exception"""
    pass


class ValidationError(DatabaseError):
    """Raised when validation fails"""
    pass


# ======================================================
# ObjectId Helpers
# ======================================================

def validate_object_id(value: str) -> ObjectId:
    if not ObjectId.is_valid(value):
        raise ValidationError("Invalid ObjectId")
    return ObjectId(value)


def create_object_id(value: Optional[str] = None) -> ObjectId:
    return ObjectId(value) if value else ObjectId()


# ======================================================
# Serialization Helpers
# ======================================================

def serialize_doc(doc: Dict[str, Any]) -> Dict[str, Any]:
    if not doc:
        return doc

    doc = dict(doc)
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])

    # Convert datetime fields
    for key, value in doc.items():
        if isinstance(value, datetime):
            doc[key] = value.isoformat()

    return doc


def serialize_docs(docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [serialize_doc(doc) for doc in docs]


# ======================================================
# Data Sanitizers
# ======================================================

def sanitize_user_data(data: Dict[str, Any]) -> Dict[str, Any]:
    allowed_fields = {
        "email",
        "name",
        "picture",
        "role",
        "created_at",
        "updated_at",
    }
    return {k: v for k, v in data.items() if k in allowed_fields}


def sanitize_product_data(data: Dict[str, Any]) -> Dict[str, Any]:
    allowed_fields = {
        "name",
        "description",
        "price",
        "stock",
        "seller_id",
        "category",
        "images",
        "status",
        "created_at",
        "updated_at",
    }
    return {k: v for k, v in data.items() if k in allowed_fields}


# ======================================================
# Query Helpers
# ======================================================

def build_filter_from_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build MongoDB filter dict from query params
    Example: ?status=active&seller_id=123
    """
    filters = {}
    for key, value in params.items():
        if value is None or value == "":
            continue
        filters[key] = value
    return filters


def paginate_query(
    query: List[Dict[str, Any]],
    page: int = 1,
    limit: int = 10,
) -> Dict[str, Any]:
    page = max(page, 1)
    limit = max(limit, 1)

    start = (page - 1) * limit
    end = start + limit

    return {
        "page": page,
        "limit": limit,
        "total": len(query),
        "results": query[start:end],
    }


# ======================================================
# Logging
# ======================================================

def log_database_operation(
    operation: str,
    collection: str,
    payload: Optional[Dict[str, Any]] = None,
) -> None:
    logger.info(
        f"[DB] Operation={operation} Collection={collection} Payload={payload}"
    )
