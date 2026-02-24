from .mongo_services import get_seller_by_email
from apps.db.mongo.utils import verify_password
from django.conf import settings
import jwt
from datetime import datetime, timedelta
from apps.db.mongo.db_collections import sellers_collection

def seller_login(email, password):

    seller = get_seller_by_email(email)

    if not seller:
        return None, "Seller not found"

    if not verify_password(password, seller["password"]):
        return None, "Invalid credentials"

    payload = {
        "seller_id": str(seller["_id"]),
        "exp": datetime.utcnow() + timedelta(days=7)
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    return {
        "token": token,
        "seller": {
            "id": str(seller["_id"]),
            "name": seller["name"],
            "email": seller["email"],
        }
    }, None


#login service


def seller_login_service(data):

    email = data.get("email")
    password = data.get("password")

    # ===== VALIDATION =====
    if not email or not password:
        return {"error": "Email and password required"}, 400

    seller = sellers_collection.find_one({"email": email})

    if not seller:
        return {"error": "Seller not found"}, 404

    # Password check (later bcrypt use karenge)
    if seller["password"] != password:
        return {"error": "Invalid password"}, 401

    # Admin approval check
    if seller.get("status") != "approved":
        return {
            "error": "Your account is not approved yet"
        }, 403

    return {
        "message": "Login successful",
        "seller": {
            "email": seller["email"],
            "full_name": seller["full_name"],
            "status": seller["status"]
        }
    }, 200
