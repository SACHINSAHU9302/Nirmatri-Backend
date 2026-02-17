import secrets
import bcrypt
from datetime import datetime, timedelta

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
