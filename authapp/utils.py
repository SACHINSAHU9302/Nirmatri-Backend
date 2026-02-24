import secrets
import bcrypt
from datetime import datetime, timedelta
import jwt
from datetime import datetime, timedelta
from django.conf import settings

def create_jwt_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(days=7),
        "iat": datetime.utcnow(),
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    return token

# 🔑 Generate secure token
def generate_reset_token():
    return secrets.token_urlsafe(32)

# 🔐 Hash password
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

# ✅ Verify password (THIS MUST EXIST)
def check_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

# ⏰ Token expiry (15 minutes)
def token_expiry(minutes=15):
    return datetime.utcnow() + timedelta(minutes=minutes)


