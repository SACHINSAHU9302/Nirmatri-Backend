import bcrypt
import jwt
from datetime import datetime, timedelta
from django.conf import settings


# ================= VERIFY PASSWORD =================
def verify_password(plain_password, hashed_password):
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )
    except Exception:
        return False


# ================= CREATE JWT TOKEN =================
def create_jwt_token(user_id):
    payload = {
        "user_id": str(user_id),
        "exp": datetime.utcnow() + timedelta(days=7),   # expire in 7 days
        "iat": datetime.utcnow(),
        "type": "access"
    }

    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm="HS256"
    )

    # PyJWT >= 2 returns string, but ensure always string
    if isinstance(token, bytes):
        token = token.decode("utf-8")

    return token

def decode_jwt_token(token):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"]
        )
        return payload

    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}